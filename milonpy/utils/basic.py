#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################
''' 
author: nickmilon
Description:    some basic variables and functions. This module is kept lightweight with a small footprint 
                and has no dependencies whatsoever (except standard python library)  
''' 
####################################### constants
FMT_HTTP_DATE = "%a, %d %b %Y %H:%M:%S GMT"
FMT_rfc2822_DATE_FMT="%a, %d %b %Y %H:%M:%S +0000"
FMT_dtGen="%y%m%d %H:%M:%S" #generic dt format
FMT_tGen="%H:%M:%S" #generic dt format
FMT_dtst="%y%m%d%H%M%S%f%V%u" #compressed  include date time miliseconds weekday weeknumber  see http://www.tutorialspoint.com/python/time_strftime.htm
####################################### file operations simple writes not unicode which needs codecs.open("xxxxxx", 'w', 'utf-8')
def global_keys():
    return sorted([i for i in globals().keys()])
def fl_write(path, contents,writeOrAppend="w"):
    with open(path, writeOrAppend) as fl: return fl.write(contents) 
def fl_readlines(path):
    with open( path) as fin:return fin.readlines() 
def fl_read(path):
    with open(path, "r") as fin:return fin.read()  
def fl_read_or_str(contents, fileExtentions=['.html', '.js']):
    if isinstance(contents, basestring):
        if any ([contents.endswith (x) for x in fileExtentions]): 
            return [fl_read(contents), True]
        else:return [contents, False]  
    elif isinstance(contents, file):
        return [contents.read() , False]  
    else:return '', False
############################################# string operations
def str_clip(s, maxLen,elipsisStr=u"\u2026"):
    return s if len(s) <= maxLen else s[:maxLen-len(elipsisStr)]+elipsisStr 
############################################# lists operations   
def lst_sort(lst,el=0,reverse=False):
    lst.sort(key=lambda x: x[el],reverse=reverse) 
def lst_transpose(lists=None, default=None):
    if lists is None:lists=[]
    return map(lambda *row: [elem or default for elem in row], *lists)   
def lst_break(bigList, maxLen):
    """returns  a list of lists  of maxLen""" 
    return [ bigList[i*maxLen:i*maxLen+maxLen] for i in xrange(len(bigList)/maxLen+int((len(bigList) % maxLen)>0) ) ]    
def lst_div(lst, numOfSubLists, pad=None):
    rt = [lst[start : start + numOfSubLists] for start in range(0, len(lst), numOfSubLists)]
    if pad is not None :
        rem = len(lst) % numOfSubLists
        rt[-1].extend ([pad] * rem) 
    return rt
def lst_removeEmpty(l):
    for it in l[:]: 
        if isinstance(it, list): 
            if len(it) == 0 :
                l.remove (it) 
            else:   
                lst_removeEmpty(it) 
    return l        
def lst_remove1Level0(l):
    for li in l: 
        if  isinstance(li, list):
            if len(li)==1 and isinstance(li[0], basestring): 
                l[l.index(li)]=li[0] 
            else: 
                lst_remove1Level0(li)    
def lst_type_lcd (lst): 
    """least common denominator of types in lst returns [need conversion(True or False) , least common type] or None if no convertible type"""
    if len(lst) == 1:                                            return [False, type(lst[0])] 
    elif all([type(it)==type(lst[0])  for it in lst[1:]]):       return [False, type(lst[0])]
    else : 
        for tpc in [(long, int), (float, long, int), (unicode, str)]:
            if all([isinstance(it, tpc) for it in lst]):return [True, tpc[0]]
    return None 
def lst_itemise(item,rt=[],incltypes=(str,unicode)):
    "must be called with empty rt=[]"
    if isinstance(item,dict):item=item.values()
    if isinstance(item,(list,tuple)):
        for it in item:lst_itemise(it,rt,incltypes)    
    elif isinstance(item,incltypes):rt.append(item)    
    return rt 
def lst_find(a_list,a_value):
    """emulates string.find behaviour returns position of value in list or -1 if not found"""
    try:return a_list.index(a_value)
    except ValueError:return -1
def lst_all_eq(a_list):
    ''' returns True if all list items are equal, list should NOT be empty 
        fastest solution for small size lists 
    ''' 
    return a_list.count(a_list[0]) == len(a_list)
def lst_itemms_apply(funct,lst):
    ''' destructive, reconstructs lst appliing function funct to all non list items of list 
        i.e : lst_itemms_apply(lambda x: round(x,4), a_list)
    '''
    for cnt,item in enumerate(lst):
        if isinstance(item, (list, tuple)):
            lst_itemms_apply(funct,item)
        else:
            lst[cnt]=funct(item)
            print item     
    return lst
def lst_extend(listOfLists):
    rt=[] 
    for i in listOfLists:rt.extend(i)
    return rt 
###################################################################### Datetime
def FloatSeconds(dt):
    ''' increase accuracy of datatime.second'''
    return dt.second+ (dt.microsecond/999999.0)
######################################################################
class Bunch(object):
    "generic property saving object, atention __dic__ incluse self, i.e point = bunch(datum=y, squared=y*y, coord=x)"
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

def enum(**enums):
    return type('Enum', (), enums)
import types  
def dictRemoveValues(d,value=None): 
    tmp=[]
    for k,v in d.items():
        if v==value: tmp.append(k)
    for k in tmp:del d[k]    
    return d     
class dictDot(dict):
    """
    dictionary with dot notation
      del r.Aux['vrf'] (dot notation does not work on last key on commands like del update etc. ) 
    """
    def prnt(self):
        for k,v in self.items():print k,v
    def __getattr__(self, attr):
        item = self[attr]
        if type(item) == types.DictType: item = dictDot(item)
        #if isinstance(item,dict):item = dictDot(item)
        return item
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__
    
def to_dictDot(val):
    if isinstance(val, dict):return dictDot(val)
    elif isinstance(val,list):return [to_dictDot(i) for i in val]
    else:return val 
#class dictDotI18N(dictDot):
#    def __init__(self,LngsValid=True,lngDefault='en',*args,**kargs):
#        self.LngsValid=LngsValid
#        self.lngDefault=lngDefault
#        super(dictDotI18N, self).__init__(args,kargs) 
       
class dictDotNE(dict):
    "dictionary with dot notation No Error it returns None for a non existing key"
    def __getattr__(self, attr):
        item = self.get(attr, None)
        #if type(item) == types.DictType: item = dictDot(item)
        if isinstance(item,dict):item = dictDotNE(item)
        return item
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

class binFlg(object):
    #__slots__ =  ['flagsList' ]
    flagsList=None
    curVal=None
    def __init__(self,flagsList=None):
        if flagsList is None:flagsList=[]
        self.flagsList=flagsList  # uniqueList ?  
    def FlgGet(self, flgInt=None, ReturnType=3):
        if flgInt is None:flgInt =self.curVal
        else : self.curVal=flgInt
        rt=[]
        i=0
        flg=-1
        while flg < flgInt: 
            flg=1 << i 
            if flgInt & flg == flg: 
                if ReturnType ==1: rt.append(flg)
                elif ReturnType==2:rt.append(i)
                elif self.flagsList is not None : rt.append(self.flagsList[i])  
            i +=1  
        return rt
    def FlgSetFromNumbers(self, flgLst, orgVal=0): 
        for i in flgLst:
            orgVal=orgVal | 1 << i  
        self.curVal=orgVal
        return orgVal
    def FlgSetFromList(self, flgLst, orgVal=0):
        for i in flgLst: 
            val= self.flagsList.index(i) 
            orgVal = orgVal | 1 << val
        self.curVal=orgVal
        return orgVal      
    def FlgSetFromDic(self, dic, orgVal=0):
        flgLst=[]
        for k in self.flagsList:
            if dic.get(k,False): flgLst.append(k)
        return self.FlgSetFromList(flgLst, orgVal)        
    def FlgSetFromDic1(self, dic, orgVal=0):
        flgLst=[k for k in self.flagsList if dic.get(k,False)] 
        return self.FlgSetFromList(flgLst, orgVal)  
   
############################################# screen colors control
color_codes = dictDot({ 
    """ br=bright _dk=dark"""
    'black'     :(0,30),    'gray_br'   :(0,37), 
    'blue'      :(0,34),    'white'     :(1,37), 
    'green'     :(0,32),    'blue_br'   :(1,34), 
    'cyan'      :(0,36),    'green_br'  :(1,32), 
    'red'       :(0,31),    'cyan_br'   :(1,36), 
    'purple'    :(0,35),    'red_br'    :(1,31), 
    'yellow'    :(0,33),    'purple_br' :(1,35), 
    'gray_dk'   :(1,30),    'yellow_br' :(1,33), 
    'normal'    :(0,) 
                })
def color_code(color):
    """ 
    color is either a tuple as in color_codes.values or a string key to color_codes dictionary in which case color_codes should be also imported by modules accesing it
    """
    if not isinstance(color,tuple):color=color_codes[color]
    return "%d;%s" %(color[0],str(color[1]) if len(color)==2 else "")
def color_switch_txt(color):
    return u"\033[%sm" %color_code(color)
def color_txt(color="red",txt=""):
    return  u"%s%s\033[0m" %(color_switch_txt(color),txt) 
def color_print(color,txt): 
    """Print in color.""" 
    print color_txt(color,txt)

def color_switch_print(color):
    print color_switch_txt(color)  
def camel_from_str(s,ml=99,separator=' '): 
    """underscore to upperCamel string conversion ml=maximum length"""
    if s.startswith("_"):s=s[1:]
    return "".join([ i[0].upper()+i[1:ml] for i in s.split(separator)])

def camel_from_us(s,ml=99): 
    """underscore to upperCamel string conversion ml=maximum length"""
    if s.startswith("_"):s=s[1:]
    return camel_from_str(s,ml,'_')  

#############################################
def keys_lst_from_dict(dic, keysList=[],levelMax=-1,_level=0): 
    for key in dic.viewkeys():
        if isinstance (dic[key], dict):
            if levelMax <0 or _level+1  <= levelMax:  
                keysList[1].append(keys_lst_from_dict(dic[key],[key,[] ],levelMax,_level+1) ) 
        else:
            keysList[1].append(key) 
    return keysList  
def key_lst_to_str(lst,prevKey="",delimiter=" " , inclKeys=True,levelMax=0,_level=-1,_levelMaxFound=0):
    """ converts a multilevel hierachical keys list  of the form
        ["TOP", ['geometry', country','name','country_code',['attributes',['567718:targetable','162763:id']],
        'place_type','id','url','full_name',['AUX',['full_nameS','nameS',['aux2', ['key1','key2'] ] ] ] ] ]  
        to string
        i.e:  TOP TOP.geometry TOP.country TOP.name TOP.attributes TOP.attributes.567718:targetable TOP.attributes.162763:id TOP.place_type TOP.id TOP.url TOP.full_name TOP.AUX TOP.AUX.full_nameS TOP.AUX.nameS TOP.AUX.aux2 TOP.AUX.aux2.key1 TOP.AUX.aux2.key2
        using dot notation separating each element with 'delimiter' up to maximum depth level of 'levelMax' or to any level if 'levelMax is negative
        ig 'inclKeys=True includes top keys otherwise only leafs _level and _levelMaxFound are internal only parameters used by recusrive calls
        returns (result string, maximum depth found) 
        function is simplified not using funcy python staff as comprehensions so that can be ported easyly to JS  
    """ 
    _levelMaxFound=max(_level,_levelMaxFound) 
    if prevKey !="" :prevKey += '.'
    rtStr =""  
    if lst[0]:prevKey += lst[0]+"." 
    if  inclKeys:rtStr+= prevKey[:-1] #rstrip dot 
    for i in lst[1]: 
        if isinstance(i, basestring): 
            rtStr="%s%s%s%s" %(rtStr,delimiter,prevKey,i) # #rtstr + = "%s%s" %(delimiter,prevKey,lst[0] ) 
            #print "new [%s]{%s}" %(rtStr,i)
        else: 
            if levelMax <0 or _level+1  <= levelMax:
                rt=key_lst_to_str(i,prevKey[:-1],delimiter,inclKeys,levelMax,_level+1,_levelMaxFound)
                rtStr += delimiter + rt[0] 
                _levelMaxFound=max(rt[1],_levelMaxFound)  
    return rtStr.strip(delimiter),_levelMaxFound  #strip it any way just to be one safe side

class base62Coder(object):
    """unsigned integer coder codes to and from base 62
    """
    symbols='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    numeric_symbols = symbols[:10] 
    def __repr__(self):
        return "<base62Coder: (%s)>" % (self.symbols) 
    @staticmethod
    def _code(number, from_digits, to_digits):  
        x = 0
        len_from_digits= len(from_digits) 
        len_to_digits=len(to_digits)
        for ch in str(number): 
            x = x * len_from_digits + from_digits.index(ch)
        if x == 0:
            res = to_digits[0]
        else:
            res = ''
            while x > 0:
                digit = x % len_to_digits
                res = to_digits[digit] + res 
                x = int(x // len_to_digits)
        return res 
    @classmethod
    def encode(cls, number):
        return cls._code(number, cls.numeric_symbols, cls.symbols) 
    @classmethod
    def decode(cls, number): 
        return cls._code(number, cls.symbols, cls.numeric_symbols) 
base62=base62Coder()
class statsSeries(object):
    max=float("inf")    #1.7976931348623157e+308
    min=float("-inf")   #"2.2250738585072014e-308
    def __init__(self,sizeMax=60): 
        self.series=[] #@todo:  na ginei deque()
        self.sizeMax=sizeMax 
        self.avg=0 
    def addVal(self,val):
        self.series.append(val)
        if len (self.series) > self.sizeMax: self.series.pop(0) 
    def stats(self,n=None): 
        if n is None:n=len(self.series)
        #@todo return stats for many periods in one pass
        n=min(n,len(self.series)) 
        stats=dictDot({'min':self.max,'max':self.min,'avg':0,'sum':0})  
        for vl in self.series[-n:]: #last n
            stats.sum+=vl
            if vl<stats.min:stats.min=vl
            if vl>stats.max:stats.max=vl
        stats.avg=round(stats.sum/float(n),2)
        return stats    
    def statsDict(self,listOfIntervals=[15,60,1660]):
        listOfIntervalsStr=['k'+str(i) for i in listOfIntervals]  #@note:  strinfy keys for compatibility with mongo
        return dictDot( dict(zip(listOfIntervalsStr ,[self.stats(i) for i in listOfIntervals] )) )
    

def seconds_to_DHMS(seconds,asStr=True): 
    days = seconds // (3600 * 24)
    hours = (seconds // 3600) % 24
    minutes = (seconds // 60) % 60
    seconds = seconds % 60 
    if asStr:return "%02d-%02d:%02d:%02d" %(days,hours,minutes,seconds)  
    else:  return days, hours, minutes, seconds