#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# see https://www.arin.net/knowledge/statistics/nro_extended_stats_format.pdf


import urllib2 
import re 
 
 
##$REM from nmlocal import remote 
from milonpy.utils.basic import fl_write, fl_readlines   
 
import os 

syncdir= os.path.expanduser('~')+'/RIR_allocations/' 
if not os.path.exists(syncdir):os.makedirs(syncdir) 
ftpserver='ripencc'
gl_rirs =rirs = ('arin','apnic','afrinic','lacnic','ripencc')  # afrinic',   only gives its own delegated  files 
 
def rirs_allocation_files():
    #ftp://ftp.ripe.net/pub/stats/arin/delegated-arin-latest
    #                                  delegated-arin-extended-latest
    return ['delegated-' + reg + 'extended-latest' for reg in rirs]
def ftpfilesPaths(fromrir=ftpserver):
    urlbase= rir(fromrir).URL_ftp_stats() 
    return [ [reg, urlbase + reg +"/delegated-"  +  reg + '-extended-latest'] for reg in rirs ] 
    
class rir(object):
    def __init__(self, rirname):
        self.fullname = rirname
    def __str__(self):return  (self.fullname)
    def domain(self):return  'ripe' if self.fullname == 'ripencc' else self.fullname  
    def URL_ftp_base(self):
        return ('ftp://ftp.' +  self.domain() + '.net')
    def URL_ftp_stats(self):return (self.URL_ftp_base() +  '/public/stats/') if self.fullname == 'apnic' else (self.URL_ftp_base() +  '/pub/stats/')
 
    
def allocationsGetFrpmFtp(fromrir=ftpserver):
    #try: 
        print "from rir=",fromrir
        if not fromrir in rirs:
            raise Exception, "nm: illegal rir server"
        #currir = rir(fromrir) 
        #cmd='wget -np --retr-symlinks -nd -r -A ' +','.join(rirs_allocation_files()) + ' -P  '+ syncdir   +  ' ' + currir.URL_ftp_stats() 
        #print "Cmd "* 10 , cmd 
        AlocFiles= ftpfilesPaths(fromrir) 
        for fl in AlocFiles:
            print "fl=",fl
            req = urllib2.Request(fl[1])
            response = urllib2.urlopen(req)
            the_page = response.read() 
            the_page= re.sub( r"""(?m)#.*?\n""", "", the_page)  # remove remark lines - apnic starts with those   
            path=syncdir+fl[0]+".last"
            if os.path.isfile(path): os.rename(path, path.split('.')[0]+'.prev')
            fl_write(path, the_page) 
    #except :
        return True
    #return True
def allocationsFindChanges():
    lstLast=[]
    lstPrev=[]
    for rir in gl_rirs: 
        print rir
        if os.path.isfile(syncdir+rir+".last"):lstLast.extend (fl_readlines(syncdir+rir+".last")[4:]) #   ( finLast.readlines()[4:])
        if os.path.isfile(syncdir+rir+".prev"):lstPrev.extend (fl_readlines(syncdir+rir+".prev")[4:]) 
    setPrev=set(lstPrev)
    setLast=set(lstLast) 
    rt=  [list(setPrev-setLast) ,list( setLast-setPrev)]
    fl_write(syncdir+'allocations.del', "".join(rt[0])) 
    fl_write(syncdir+'allocations.add', "".join(rt[1])) 
    return rt 

def ccCodes():
    allIpv4=[ item  for item in fl_readlines(syncdir+'allocations.original')      if item.find('ipv4')>-1 ]
    allCC=[item.split('|')[1] for item in allIpv4]
    return list(set(allCC))
    
def main():
    print "allocationsGetFrpmFtp"
    allocationsGetFrpmFtp()
    print "allocationsFindChanges"
    return allocationsFindChanges()

if __name__ == "__main__": 
    main()      
