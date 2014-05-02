#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################
'''
module: utilities.basic2
Created:Aug 21, 2012
author: nickmilon
Description:  Description: Simple utilities (2) and Vars - Very Limited IMPORTS HERE !                            
'''
#######################################################
from sys import stdout
from datetime import datetime , timedelta 
from basic import FMT_dtGen,FMT_tGen, color_txt ,color_switch_txt,dictDot 
from time import sleep ,time,mktime
import re
 
def re_is_sameLen(txt,rexp):return len(txt)==len(rexp.findall(txt))
def re_is_same(txt,rexp):return txt==u''.join(rexp.findall(txt))
def re_diff(txt,rexp):return ''.join(list(set([c for c in txt]) - set(rexp.findall(txt))))
#re_gr=re.compile(ur'[\u03AC-\u03CE]|[;\s]',            re.IGNORECASE| re.VERBOSE| re.UNICODE |re.MULTILINE) 
def time_seconds_since_epoch(dt=None):
    if dt is None:dt=datetime.utcnow()
    return mktime(dt.timetuple())+1e-6*dt.microsecond   
def autoRetry(exceptionOrTuple,retries=3,sleepSeconds=1, BackOfFactor=1,loggerFun=None): 
    """ exceptionOrTuple= exception or tuple of exceptions,BackOfFactor=factor to back off on each retry loggerFun i.e. logger.info """
    def wrapper(func):
        def fun_call(*args, **kwargs):
            tries = 0 
            while tries < retries:
                try:
                    return func(*args, **kwargs) 
                except exceptionOrTuple, e:   
                    tries += 1 
                    if loggerFun:loggerFun("exception [%s] e=[%s] handled tries :%d sleeping[%f]" % (exceptionOrTuple ,e,tries,sleepSeconds * tries * BackOfFactor) )
                    sleep(sleepSeconds * tries * BackOfFactor) #* tries) 
            raise   
        return fun_call 
    return wrapper 

def parseJSfunFromFile(filepath,functionName): 
    """
        helper function to get a js function string from a file containing js functions. Function must be named starting in first column and file must end with //eof// 
        lazyloads re 
    """ 
    with open( filepath) as fin: 
        r=re.search("(^.*?)(?P<fun>function\s+?%s.*?)(^fun|//eof//)" % functionName,fin.read(),re.MULTILINE|re.DOTALL)
        return r.group('fun').strip() if r else False

def stdout_switchColor(color): 
    stdout.write (color_switch_txt(color)) 
    
def stdout_write_flush(txt,stAfter="\r",color=None):
    if color:txt= color_txt(color,txt) 
    stdout.write("%s%s" %(txt,stAfter) ) 
    stdout.flush() 
  

class timeElapsed(object): 
    """ overwrite str_dtimes str_deltas to return "" to exclude this form output string
        @todo:   logging handler
    """
    def __init__(self, cnt_max=1,name_str=""):  
        self.name_str=name_str
        self.cnt_max= cnt_max
        self.dt_start=datetime.utcnow()
        self.dt_last=self.dt_start
        self.dt_current=self.dt_start
        self.cnt=0
        self.cnt_last=0
        self.cnt_last_dif=0
        self.perc_done=0.0
        self.time_remaining=0
        self.time_elapsed_since_start=timedelta(0)
        self.time_elapsed_since_last=timedelta(0)
        self.time_remaining =timedelta(0)
        self.units=['sec','min','hour']
        self.set_cnt_max(cnt_max) 
    def set_cnt_max(self,val): 
        self.cnt_max=val
        self.frmt_str="%s%d%s" %("%",len(str(val)),"d" ) 
    def set_auto_unit(self,velocity,unit_idx=0):
        if velocity < 1 and unit_idx < 2:
            velocity=velocity * 60
            unit_idx+=1
            return  self.set_auto_unit(velocity, unit_idx)
        else:
            return velocity, self.units[unit_idx] 
    def frmt_max(self,val):
        return  self.frmt_str % val
    def update(self,cur_val,getStr=True,):
        cur_val=float(cur_val)
        if cur_val > self.cnt_max:self.set_cnt_max(self.cnt_max+int(cur_val/10))
        self.dt_current=datetime.utcnow()
        self.time_elapsed_since_start = self.dt_current- self.dt_start
        self.time_elapsed_since_last=self.dt_current- self.dt_last
        self.cnt_last_dif=self.cnt_last-cur_val
        self.perc_done=cur_val/self.cnt_max 
        self.time_remaining =timedelta(seconds=int ( self.time_elapsed_since_start.total_seconds() * ( (1-self.perc_done)/self.perc_done)))
        self.cnt=cur_val
        self.v_start= self.cnt/self.time_elapsed_since_start.total_seconds()
        self.v_last= self.cnt_last_dif/self.time_elapsed_since_last.total_seconds()  
        self.dt_last=self.dt_current
        self.cnt_last=cur_val
        return self.toStr() if getStr else True
    def update_last(self,cur_val,getStr=True):
        self.cnt_max=cur_val
        return self.update(cur_val,getStr)
    def str_counters(self):
        return u"|%s of %s" %(self.frmt_max(self.cnt), self.frmt_max(self.cnt_max))   
    def str_dtimes(self):  
        return u"⌚ %s %s %s" % (self.dt_start.strftime(FMT_dtGen),self.dt_current.strftime(FMT_tGen), (self.dt_current+self.time_remaining).strftime(FMT_tGen))
    def str_tdeltas(self):
        return  u"⌛ %s %s %s" %(self._str_tdelta(self.time_elapsed_since_start),self._str_tdelta(self.time_elapsed_since_last), self._str_tdelta(self.time_remaining) )
    @staticmethod
    def _str_tdelta(tdelta):
        str_td=str(tdelta)
        tmp=str_td.find(".")
        if tmp !=-1 : str_td= str_td[:tmp]
        return u"%8s" %  str_td  
    def toStr(self): 
        return  u"[%s:%6.2f%%%s%s%s]" %(self.name_str,100* self.perc_done, self.str_counters(),
                                       self.str_tdeltas(),self.str_dtimes() )
class SubToEvent(object):
    ''' lightwaight Event handler modeled after Peter Thatcher's  http://www.valuedlessons.com/2008/04/events-in-python.html
           usage:
            watcher = SubToEvent()
            def log_docs(doc):print doc
            watcher += log_docs
            watcher += lambda x:str(x) 
            watcher.stop()
    '''
    def __init__(self,channelName=''):
        self.channelName=channelName
        self.handlers = set() 
    def handle(self, handler):
        self.handlers.add(handler)
        return self 
    def unhandle(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("No_such_handler")
        return self 
    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs) 
    def fireTopic(self,topic=None,verb=None,payload=None):
        self.fire ((self.channelName,topic,verb,payload)) 
    def getHandlerCount(self):
        return len(self.handlers) 
    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount

 
class multiOrderedDict(object):
    '''
        deletes can't be multi
    '''   
    def __init__(self,lst): 
        self.lstDic=lst
    def __getitem__ (self,key):
        return self._getOrSetDictItem(key)
    def __setitem__(self, key, val):
        return self._getOrSetDictItem(key,True,val) 
    def __delitem__ (self, key):
        return self._getOrSetDictItem(key,delete=True)
    def get(self,key,orVal=None):
        try:
            return self[key]
        except KeyError:
            return orVal 
    def keys(self):
        return[i[0] for i in self.lstDic if self.isKey(i[0])]
    def values(self):
        return [self[i] for i in self.keys()]
    
    def isKey(self,k):
        return True
    def _getOrSetDictItem (self,key,setVal=False,newVal=None,multi=False,delete=False):
        idx=[]
        for n,i in enumerate(self.lstDic):
            if i[0]==key and self.isKey(i[0]):
                idx.append(n) 
                if setVal:self.lstDic[n]=[i[0],newVal] 
                if not multi: break 
        if len(idx)>0:
            if delete:
                self.lstDic.pop(idx[0]) #can't be multi
                return None
            rt= [self.lstDic[i][1:] for i in idx ]
            if multi:
                return rt 
            else:
                return rt[0][0] 
        else:
            if setVal:
                self.lstDic.append([key,newVal])
                return newVal
            else:
                raise KeyError (key)
    def toDict(self):
        return dict(zip(self.keys(),self.values()))
    def toString(self):
        return str(self.toDict())
    __str__ =  toString   
class confFileDict(multiOrderedDict):
    def __init__(self,path,skipBlanks=True,skipRemarks=True):
        self.path=path
        with open(self.path) as fin:
            rlines=fin.readlines()
        if skipBlanks:rlines=[i for i in rlines if not i=='\n']
        if skipRemarks:rlines=[i for i in rlines if not i.startswith("#")] 
        lstDic=[ map(lambda x: x.strip(), i.split("=") ) for  i in rlines]
        super(confFileDict, self).__init__(lstDic)  
    def isKey(self,key):
        return key !='' and not key.startswith("#") 
    def toStr(self):
        s=''
        for i in self.lstDic:
            s+= "=".join(i)+'\n' 
        return s.rstrip() 
    def toFile(self,path=None):
        if not path:path=self.path
        with open(path, 'w') as fl:
            fl.write(self.toStr) 

def PrintTiming(func):
    """set up a decorator function for timing"""
    def wrapper(*args, **kargs):
        t1 = time.time()
        res = func(*args, **kargs)
        tel = time.time()-t1
        timeformated = time.strftime( "%H:%M:%S",time.gmtime(tel)) 
        print  '-'*5 + '%s took %0.3f ms' % (func.func_name + str(kargs) + str(args),   (tel)*1000.0)   + '|' + timeformated + '|'+ '-'*10 
        return res
    return wrapper



def totalsVertical(orgD,resD,funct,initFunc): 
    '''Apply funct to resD dict values by orgD values, creates keys in resD if do not exist
       usufull for vertical persentage and totals
       attention : it is ditractive replacing resD with results
       i.e: to incr resD values by OrgD values  resultAply(orgDict,resultsDict,lambda x,y:x+y, lambda x:0)
            to find perc of org : .resultAply(res,dorg[0].value,lambda x,y:100*y/x if x!=0 else None,None) 
    '''
    for  k in orgD.keys():
        if isinstance(orgD[k],dict):
            if resD.get(k):
                totalsVertical(orgD[k],resD[k],funct,initFunc)
            else:
                if initFunc:
                    resD[k]=totalsVertical(orgD[k],dictDot({}),funct,initFunc)
                else: continue   
        elif isinstance(orgD[k],(float,int)):       
            if  resD.get(k,False) is False : 
                if initFunc:
                    resD[k]=initFunc(orgD[k]) 
                else: 
                    continue   
            resD[k] = funct(orgD[k],resD[k])  
        else:
            if initFunc:resD[k]=orgD[k]
    return resD 
def totalsVertSimple(orgD,resD,funct):
    ''' simplified and faster version of totalsVertical assumes all key/values of orgD are present in resD 
    '''
    for k in orgD.keys():
        if isinstance(orgD[k],dict):totalsVertSimple(orgD[k],resD[k],funct)
        elif isinstance(orgD[k],(float,int)):orgD[k]=funct(orgD[k],resD[k])
    return orgD    
def totalsHorizontal(value,a_dict,funct=lambda x,y:100*x/y):
    for k in a_dict.keys():
        if isinstance(a_dict[k],dict):totalsHorizontal(value,a_dict[k])
        elif isinstance(a_dict[k],(float,int)):a_dict[k]=funct(a_dict[k],value)
    return a_dict       

class TextWrapper(object):  
    ''' http://jrgraphix.net/r/Unicode/ '''
    elipsis=u"\u2026" # "…"  
    numbers=u"₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎" 
    def __init__(self, maxLen=140,minLen=100, contChr=u'⎘',inclNumbers=True,strFlag=u'',strFirst=u'',strRest=u'',strAll=u''):  
        self.contChr=contChr
        self.inlNumbers=inclNumbers
        self.strFlag=strFlag
        self.strFirst=strFirst
        self.strRest=strRest
        self.strAll=strAll 
        self.maxLen=maxLen
        self.minLen=minLen 
    def compineStr(self,s,cnt,totalCnt=None):
        return "%s%s%s%s%s" %(self.strFlag,self.formatNumOfTotal(cnt+1,totalCnt) if self.inlNumbers else u'',  self.strAll, self.strFirst if cnt==0 else self.strRest,s)
    def splits(self,astr):  
        n=self.maxLen-1- len(self.contChr)
        minLen=self.minLen
        cnt=0
        s=self.compineStr(astr, cnt)
        while len(s) > n:
            cnt+=1  
            rf=s[0:n].rfind(u'\n',minLen)
            if rf == -1:rf=s[0:n].rfind(u'.',minLen)
            if rf == -1:rf=s[0:n].rfind(u' ',minLen)
            spltn = rf+1 if rf !=-1 else n 
            #print "(%3d) %3d %3d %3d [%s]" %(cnt, rf,n,spltn,s[0:n]) 
            rt=s[:spltn].rstrip()
            remainingStr=s[spltn:] 
            if self.contChr !=u'':
                if len(remainingStr)>1:rt+=self.contChr
                else:
                    rt+=remainingStr
                    remainingStr=u''
            yield rt 
            s=self.compineStr(remainingStr, cnt) if remainingStr !=u'' else u''
        yield s
    def formatNumOfTotal(self,cnt, totalCnt=None):
        return u"%s∕%s" %(self.formatNum(cnt),u'??' if totalCnt is None else self.formatNum(totalCnt)) #'∕' is not '/' but math '\u2215'
    def formatNum(self,num):
        header=map(int,str(num))
        rt=[self.numbers[i] for i in header]
        return ''.join(rt)
    def format(self,text):
        rt=[]
        for i in self.splits(text):
            if i !=u'':rt.append(i) 
        if self.inlNumbers:
            rt2=[]
            maxCnt=len(rt)
            for cnt,vl in enumerate(rt):
                old= self.formatNumOfTotal(cnt+1,None)
                new= u'' if maxCnt == 1 else  self.formatNumOfTotal(cnt+1,maxCnt)
                if new !=u'':new += u' '* (len(old)-len(new)) 
                rt2.append(vl.replace(old, new , 1))
            return rt2
        return rt  

         
##################       tests 
def test_timeElapsed(x): 
    et=timeElapsed(x,"foo") 
    for i in range(1,x):
        sleep(1)
        print et.update(i, True) 
    print et.update_last(i)
###################

 








    