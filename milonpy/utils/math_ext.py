#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################
'''
module: utilities.math_ext
Created:Aug 29, 2012
author: nickmilon
Description:                           
'''
#######################################################
import math
from milonpy.utils.basic import lst_all_eq
def ln(x):return math.log(x,math.e)
def frange(start,stop, step=1.0):
    ''' accepts float step'''
    while start < stop:
        yield start
        start +=step

def angle2d(x1, y1, x2, y2):
    theta1 = math.atan2(y1, x1)
    theta2 = math.atan2(y2, x2)
    dtheta = theta2 - theta1
    while dtheta > math.pi:
        dtheta -= 2.0 * math.pi
    while dtheta < -math.pi:
        dtheta += 2.0 * math.pi 
    return dtheta 
def ptInPolygon(pt,polygon):
    """
    See http://local.wasp.uwa.edu.au/~pbourke/geometry/insidepoly/  looks faster than other methods there although needs to import math
    polygon list of x,y lists,pt a point as a list/tuple of [x,y]
    if you have more demanding needs then check shapely library https://github.com/sgillies/shapely and also geojango 
    @attention:  works with polygons that have holes (donuts) - also does not acount for earth curvature
    """
    angle = 0.0
    n = len(polygon)
    for i, (h, v) in enumerate(polygon):
        p1 = (h - pt[0], v - pt[1]) 
        h, v = polygon[(i + 1) % n]
        p2 = (h - pt[0], v - pt[1])
        angle += angle2d(p1[0], p1[1], p2[0], p2[1]);
    if abs(angle) < math.pi:
        return False
    return True
pt_in_poly=ptInPolygon #@note:  till we refactor later
def rectToPoly(rect):
    return [rect[0], [rect[1][0],rect[0][1]],rect[1],[rect[0][0],rect[1][1]] ,rect[0] ] 
def rect_in_poly(rect,poly,tp='center'):
    if tp=='center': return pt_in_poly(rectangle_center(rect),poly)
    if tp=='touch': # aproximation just tests the if any edge or centerinside poly (it is NOT a proper Intersection Test) 
        polyRect=rect=rectToPoly(rect) 
        return any([pt_in_poly(i,poly) for i in polyRect]) or pt_in_poly(rectangle_center(rect),poly)
    if tp=='in': return pt_in_poly(rect[0],poly) and pt_in_poly(rect[1],poly)
    
def rectangle_center(rect):
    pbr=polygon_bind_rect(list(rect))
    return [ (pbr[1][0] -pbr[0][0])/2, (pbr[1][1] -pbr[0][1])/2 ]

   
def polygon_bind_rect(poly): 
    '''poly = list of long(x) lat(y)  pairs list
       not chhecked for crossing minus to plus boundaries
       flickrpoly=gi.find()[0]['val']['place']['shapedata']['polylines']['polyline'][0]['_content']
       returns BBox Corners LeftDown[x,y],RightUp[x,y]
    '''
    maxX,minX=float('-inf'),float('inf') 
    maxY,minY=maxX,minX
    for item in poly:
        #print 'item',item
        maxX=max(maxX,item[0])
        minX=min(minX,item[0])
        maxY=max(maxY,item[1])
        minY=min(minY,item[1])
    return [ [minX,minY],[maxX,maxY]] 
def revPoint(pntLst):
    for i in pntLst:
        if isinstance (i[0],list):
            return revPoint(i)
        else:
            i= i[::-1] 
    return pntLst
def bbox_to_poly(LD,RU):
    '''LeftDown[x,y],RightUp[x,y]''' 
    return [ LD, [RU[0],LD[1]],RU,[LD[0],RU[1]],LD]
def geojson_tsearchlist_fromPolys(p):
    '''twiiter search Locations list from list of polygons ''' 
    rt=[]
    for i in p:
        br=polygon_bind_rect(i)
        #br=sum(br, []) 
        br=[item for sublist in br for item in sublist] ##flaten list of lists
        rt.extend(br)
    return rt
    
def geojson_from_tsearchlist(tllst):
    '''Twiiter search Locations list twtslst as  [-122.398682,37.602944,-122.351818,37.642646 , ..., ....]
       returns a  geojson Polyggon  
    '''
    assert len(tllst) % 4 == 0  #
    polylist=[]
    for i in  frange(0,len(tllst), step=4): 
        LD=[tllst[i],tllst[i+1]]
        RU=[tllst[i+2],tllst[i+3]]
        polylist.append(bbox_to_poly(LD,RU))  
    return {'type':'Polygon','coordinates':polylist}
def geojson_fix(feature): 
    def fixPoly(p): 
        if len(p) >0: 
            if lst_all_eq(p): #fixes this type  
                feature['type']='Point'
                feature['coordinates']= feature['coordinates'][0][0] 
            elif p[0]!=p[-1]: #fixes not closed polygons like this {u'type': u'Polygon', u'coordinates': [[[19.3729582, 34.8020213], [19.3729582, 41.7485356], [29.6430578, 41.7485356], [29.6430578, 34.8020213]]]}
                p.append(p[0])
    if feature['type']=='Polygon':
        for pitem in feature['coordinates']:
            fixPoly(pitem)
    return feature    

def polygon_strips(poly,stepsX=10,stepsY=10,include='touch'):
    ''' include values=center if tile center inside polygon, touch if any of tile edges overlaps poly,inside=if tile enclosed in poly   
    ''' 
    pbr= polygon_bind_rect(poly)
    rangeX=pbr[1][0]-pbr[0][0]
    rangeY=pbr[1][1]-pbr[0][1]
    stepX=rangeX/stepsX
    stepY=rangeY/stepsY
    resStrips=[]
    print 'rangeX=',rangeX
    print 'rangeY=',rangeY
    print 'pbr=',pbr
    for y in frange(pbr[0][1],pbr[1][1],stepY):
        print "--" * 10
        print "y=",y
        tilesLst=[]
        for x in frange(pbr[0][0],pbr[1][0],stepX):
            tile=[[x,y],[x+stepX,y+stepY]]
            tileInPoly=rect_in_poly(tile,poly,include)
            #print "cur tileREv",tileInPoly,pt_in_poly(tile[0],poly),pt_in_poly(tile[1],poly) , [tile[0][::-1],tile[1][::-1] ]
            if tileInPoly: 
                tilesLst.extend(tile)  
        #print 'tilesLst', tilesLst 
        if len(tilesLst)>0: 
            #stripStart= [[tilesLst[0][0],[tilesLst[0][1]] 
            #stripEnd=   [[tilesLst[-1][1],[tilesLst[-1][1]]
            #print 'last TileRv-1',tilesLst[-1] 
            strip= polygon_bind_rect(tilesLst) #     [ tilesLst[0][0],tilesLst[-1][1] ]
            #strip= [ tilesLst[0][0],tilesLst[-1][1] ]
            srtiprev=[i[::-1] for i in strip]
            #strip=polygon_bind_rect(tilesLst)
            print 'strip=',strip ,'\nrev=',srtiprev
            resStrips.append(strip) 
    
    return resStrips 
    
    
    
    
    
    

