#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################

#######################################################
'''
module: html_gen
Created:Apr 10, 2012
author: nickmilon
Description:    html generator                        
'''
#######################################################
 
from  ..utils import basic as utlbs                                              #@UnresolvedImport
# from utilities import basic as utlbs  #use this when runing from pydev
doctype_html4=u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
doctype_html5=u'<!doctype html>'
doctype_XHTML=u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
doctype_current=doctype_html5

 
class attrs(object):
    __slots__ = ['contents']  
    def __init__(self, attrs=''):
        self.contents=''
        if isinstance(attrs, dict): 
            for it in attrs:  
                self[it]=attrs[it]  
        elif isinstance(attrs,list):
            for it in attrs:
                self[it[0]]=it[1] 
        else:
            self.contents=attrs
    def __setitem__(self, attr, val):  
        del self[attr]
        self.contents = "%s%s%s%s%s%s%s" % (self.contents,'' if self.contents == '' else ' ',  attr ,  '=' ,  "\"" ,  val ,  "\"") 
        return val
    def getAttrLst(self, attr):
        rt=self[attr]
        if rt !='':return rt.split(' ')
        else:return [] 
    def hasSubAttr(self, attr, subAttr):
        return subAttr in self.getAttrLst(attr)
    def append(self, attr, val):
        res=self[attr]
        if res =='':
            self[attr]=val
        else:
            if val !='':self[attr]= res  + ' ' + val
    def __getitem__ (self,attr):
        return self.strAttr(attr)[len(attr)+2:-1] 
    def setFlag(self,flgVal):
        flgVal=" "+flgVal
        if self.contents.find(flgVal)==-1: self.contents += flgVal #New in  V2
    def strAttr(self, attr, start=0):
        st=str(self.contents)
        idxSt=st.find(attr +'=' , start) 
        if idxSt == 0 or idxSt > 0 and st[idxSt - 1]==' ':
            idxEnd = st.find('\"', idxSt+len(attr)+2) 
            if idxEnd >- 1:return st[idxSt:idxEnd+1]
            else: return ''
        elif idxSt >0:
            return self.strAttr(attr, idxSt+1)
        else:
            return ''
    def __delitem__ (self, attr):
        st = self.strAttr(attr)
        if st !='':self.contents = self.contents.replace(st, '').strip() 
    def __str__  (self): return self.contents.__str__() 
    def __call__ (self): return self.contents.__str__()
class tag(object):          #normal closing tag ie: <tag>xxx</tag>
    __slots__ =  ['_name','contents', 'attributes', '_expand', '_nonclosing']
    _cnstEOL=u'\n'
    _nonclosing=False
    #_nonclosing=['meta', 'link', 'col' , 'img',  'input']
    def __init__(self, contents='', attributes='', name=None): 
        if isinstance(attributes,attrs):
            self.attributes = attributes 
        else:   
            self.attributes = attrs(attributes)
        self.contents = u''
        self._name = self.__class__.__name__ if name is None else name 
        self._expand='\t' 
        self.insertContents(contents)
    def validateContents(self, conts):
        return True
    #          if isinstance(conts, basestring):      return True 
    #          elif isinstance(conts, (list, tuple)): return all([isinstance(it, tag) for it in conts]) 
    #          else:                                  return False 
    def validationError(self,conts):
        raise Exception ('Err On Tag Validation: ',type(self), conts) 
    def insertContents(self, contents,before=None):  #TOFIX: 1 level lists only also sometimes before does npt work if contents have to be evaluated?
        if isinstance(contents, str):contents = unicode(contents,  'utf-8')   
        if self.validateContents(contents):
            if self.contents != '' and not isinstance(self.contents, list):self.contents = [self.contents]
            if isinstance(self.contents, list):
                if before is None:
                    if isinstance(contents, list):self.contents.extend(contents)
                    else:self.contents.append(contents)
                else:
                    if isinstance(contents, list):
                        for it in reversed(contents):
                            self.contents.insert(before, it)
                    else:self.contents.insert(before, contents)  
            else:self.contents = contents 
        else:
            self.validationError (contents)  
        return contents
    def __setitem__(self,i, val):
        self.contents[i]=val
        return val
    def __getitem__(self,i): 
        return self.contents[i]
    def getByAttr(self,attr,val,repl=None,insertIfNF=False):
        #TODO: works for 1st level make it recursive
        for ix,item  in enumerate(self.contents):
            if isinstance(item,tag) and item.attrGet(attr) == val:
                if repl is not None:
                    self.contents[ix]=repl
                return ix,item
        if insertIfNF and repl is not None:self.insertContents(repl)        
        return None,None
    def attrGetClass(self):           return self.attrGet('class')
    def attrIsOfClass(self, subAttr): return self.attributes.hasSubAttr('class', subAttr)
    def attrGetId(self):              return self.attrGet('id')
    def attrSetClass(self, val):      return self.attrSet('class', val)
    def attrSetId(self, val):         return self.attrSet('id', val)
    def attrSetStyle(self, val):      return self.attrSet('style', val)
    def attrSetRole(self, val):       return self.attrSet('role', val)
    def attrSet(self, attr, val):     self.attributes[attr]=val  
    def attrGet(self, attr):          return self.attributes[attr]
    def attrGetTitle(self):           return self.attrGet('title')
    def attrSetTitle(self, val):      return self.attrSet('title', val)
    def attrGetName(self):            return self.attrGet('name')
    def attrSetName(self, val):       return self.attrSet('name', val)  
    def attrDel(self, attr):          del self.attributes[attr]
    def attrAppend(self, attr, val):  self.attributes.append(attr,val) 
    def attrAppendClass(self, val):   self.attributes.append('class',val)
    def attrAppendCnt(self, cnt, ststr='nm-'):  self.attrAppendClass('%s%s%02d %s%s' %(ststr,'cnt', cnt, ststr,'even' if cnt % 2 == 0 else 'odd') )
#    def attrSetFromList(self, atrLst):
#        for item in atrLst: self.attrSet(item[0],item[1])
    def setExpand(self, expandchrs):self._expand=expandchrs 
    #      def appendContents(self, contents):
    #          if self.contents != '' and not isinstance(self.contents, list):self.contents = [self.contents]
    #          if isinstance(contents, list):
    #             for it in contents:self.appendContents(it)
    #          else:
    #             self.contents.append(contents)  
    def name(self):return self._name
    def __len__(self): 
        if isinstance(self.contents, list):   return sum([len (item) for item in self.contents]) + 1  
        else: return 1
    def _toStrOpen(self):
        if doctype_current == doctype_XHTML:
            return '<'+ self.name() + ('' if str(self.attributes) =='' else ' ') + str(self.attributes) + ('>' if self.contents !='' else ' ')
        else:
            #$ org - return '<'+ self.name() + ('' if str(self.attributes) =='' else ' ') + str(self.attributes) + '>' # ('/>' if self.name() in self._nonclosing else '>')
            return '<'+ self.name() + ('' if str(self.attributes) =='' else ' ') + str(self.attributes) + (' ' if self._nonclosing else '>')  
            #return '<'+ self.name() + ('' if str(self.attributes) =='' else ' ') + str(self.attributes) +  ('/>' if self._nonclosing else '>')
            #return '<'+ self.name() + ('' if str(self.attributes) =='' else ' ') + str(self.attributes) +  '>'  
    def _toStrAttrs(self):return str(self.attributes)
    def _toStrContents(self, subcontents):
        if isinstance(subcontents, list):
            return ''.join([self._toStrContents(item) for item in subcontents])
        elif isinstance(subcontents,tag):
            return subcontents.toStr()
        else :
            return subcontents    
    def _toStrClose(self):
        if doctype_current == doctype_XHTML:
            return '</' + self.name() +  '>' if self.contents !='' else '/>'
        else: 
            if self._nonclosing:   # self.name() in self._nonclosing: 
                return '>'
            else:
                return '</' + self.name() +  '>' # if self.contents !='' else '>'  
    def toStr(self):
    #          if self._nonclosing:
    #             return "%s %s %s%s" %(self._toStrOpen() , self._toStrAttrs(), self._toStrContents(self.contents) ,  self._toStrClose()  )
    #          else:
    #            return "%s %s>%s%s" %(self._toStrOpen() , self._toStrAttrs(),    self._toStrContents(self.contents) ,  self._toStrClose()  )
          
        return self._toStrOpen() + self._toStrContents(self.contents)  + self._toStrClose() 
    def genStr(self, depth=0):
        def expand():return self._expand * depth
        if isinstance (self.contents, basestring):  
            yield "%s%s%s%s%s" % (expand(),self._toStrOpen(), self.contents.replace('\n', '\n'+expand()), self._toStrClose(), self._cnstEOL)
        if isinstance(self.contents,tag):
            yield expand() + self._toStrOpen()  + self._cnstEOL
            for val in self.contents.genStr(depth+1):
                yield val
            yield expand() + self._toStrClose() + self._cnstEOL
        elif isinstance(self.contents,list):
            yield  expand() + self._toStrOpen()  + self._cnstEOL
            for item in self.contents:  
                if isinstance(item, basestring):yield item
                else: 
                    for val in item.genStr(depth+1): 
                        yield val 
            yield  expand() + self._toStrClose() + self._cnstEOL
    #          elif isinstance(self.contents,GVtable):
    #            rtv='\n'+ str(self.contents)+'\n'
    #            yield "%s%s%s%s%s" % (expand(),self._toStrOpen(), rtv.replace('\n', '\n'+expand()), self._toStrClose(), self._cnstEOL)
    def genStrStr(self, depth=0):
        st=''
        for vl in self.genStr(depth):st += vl  
        return st     
    def strpp(self, st='', depth=0):
        def expand():return self._expand * depth
        st += expand() + self._toStrOpen() 
        if isinstance(self.contents,tag):
            st += self._cnstEOL
            st = self.contents.strpp(st,depth + 1) 
        elif isinstance(self.contents, list):
            st += self._cnstEOL
            for item in self.contents:
                st = item.strpp(st,depth + 1)
        else:
            st += self.contents
        if isinstance(self.contents, (list, tag)) :st += expand() 
        st ="%s%s%" %(st,  self._toStrClose() ,  self._cnstEOL)
        return st
    def genStrNT(self, depth=0,TagOpen=u'',TagClose=u', '  ,EOLStr=u'',expandStr=u''): 
        def expand():return expandStr *  depth
        if isinstance (self.contents, basestring):  
            yield "%s%s%s%s%s" % (expand(),TagOpen, self.contents.replace('\n', '\n'+expand()), TagClose, EOLStr)
        if isinstance(self.contents,tag):
            yield expand() + TagOpen + EOLStr
            for val in self.contents.genStrNT(depth+1, TagOpen, TagClose, EOLStr, expandStr):
                yield val
            yield expand() + TagClose + EOLStr
        elif isinstance(self.contents,list):
            yield  expand() + TagOpen + EOLStr
            for item in self.contents:  
                if isinstance(item, basestring):yield item
                else: 
                    for val in item.genStrNT(depth+1, TagOpen, TagClose, EOLStr, expandStr): 
                        yield val 
            yield  expand() + TagClose + EOLStr    
    def genStrNTStr(self, depth=0,TagOpen=u'',TagClose=u', '  ,EOLStr=u'',expandStr=u'' ):
        st=u''
        for vl in self.genStrNT(depth=0,TagOpen=u'',TagClose=u', '  ,EOLStr=u'',expandStr=u'' ):
            st += vl  
        return st  
#    def genStrNTContents(self):
#        st=u''
#        for vl in self.genStrNT(depth=0,TagOpen=u'',TagClose=u'XAX',EOLStr=u'',expandStr=u'' ):
#            st += vl  
#        st=re.sub("<br>|(XAX){1,100}",',',st)
#        return st[2:-1]   
    
    #      def gen(self):
    #          if isinstance(self.contents, list):
    #             for item in self.contents:
    #                 if isinstance(item , tag):
    #                    for it in item.gen():yield it
    #          else:
    #              if isinstance(self.contents, tag):
    #                  for it in item.gen():yield it 
    #              else:
    #                  yield self 
    def saveToFile(self, fname):
        fileOut = open(fname, 'w')
        fileOut.write(self.genStrStr()) 
        fileOut.close()
    def __add__(self, other):
        return self.genStrStr() + (other.genStrStr() if isinstance(other, tag) else other)
    __str__  =  genStrStr
    __call__ =  genStrStr   
    __repr__ =  toStr
class tag_ws(tag):pass      #tag with slots so can be used as dict also BUT never use  ['_name','contents', 'attributes', '_expand', '_nonclosing']
class tag_nc(tag):          #none closing tag   ie <tag_name a /> 
    __slots__ =  []
    _nonclosing=True
class div(tag):__slots__    =[]
class span(tag):__slots__   =[]
class p(tag):__slots__      =[] 
class h1(tag):__slots__     =[] 
class h2(tag):__slots__     =[]
class h3(tag):__slots__     =[] 
class h4(tag):__slots__     =[] 
class h5(tag):__slots__     =[]
class h6(tag):__slots__     =[]  
class a(tag):
    __slots__ =  []
    def __init__(self, contents='', attributes='', href=False, target=False, title=False):
        tag.__init__(self,contents, attributes) 
        if href:self.attrSetHref(href)
        if title: self.attrSetTitle(title)
        if target:self.attrSetTarget(target) 
    def attrGetHref(self):             return self.attrGet('href')
    def attrSetHref(self, val):        return self.attrSet('href', val) 
    def attrGetTarget(self):           return self.attrGet('target')
    def attrSetTarget(self, val):      return self.attrSet('target', val) 
class img(tag):
    __slots__ =  []
    _nonclosing=True
    def __init__(self, src=False, alt=False, title=False, height=False, width=False):
        tag.__init__(self) 
        if src:   self.attrSetSrc(src)
        if alt:   self.attrSetAlt(alt)
        if title: self.attrSetTitle(title)
        if height: self.attrSetHeight(height)
        if width: self.attrSetWidth(width)
    def attrGetSrc(self):             return self.attrGet('src')
    def attrSetSrc(self, val):        return self.attrSet('src', val)
    def attrGetAlt(self):             return self.attrGet('alt')
    def attrSetAlt(self, val):        return self.attrSet('alt', val)
    def attrGetHeight(self):          return self.attrGet('height')
    def attrSetHeight(self, val):     return self.attrSet('height', val)
    def attrGetWidth(self):           return self.attrGet('width')
    def attrSetWidth(self, val):      return self.attrSet('width', val) 
class i(tag):__slots__      =[] #italic text
class b(tag):__slots__      =[] #bold text
class big(tag):__slots__    =[] #biger text
class small(tag):__slots__  =[] #smaller text
class tt(tag):__slots__     =[] #teletype text
class sup(tag):__slots__    =[] 
class sub(tag):__slots__    =[]     
class abbr(tag):__slots__   =[]  
class acronym(tag):__slots__ =[] 
class style(tag):
    def __init__(self, contents='', attributes=''):
        tag.__init__(self,contents, attributes)  
        self.attrSet("type", "text/css")    

class mformat_geo(tag):        #geo microformat   
        __slots__ =  []
    #contents='', attributes='', name=None   
        def __init__(self,latitude, longitude, contents='', name='span'): 
            tag.__init__(self,contents, name=name)
            self.attrSetClass('geo')
            self.insertContents(span(latitude, 'class="latitude"'))
            self.insertContents(span(longitude, 'class="longitude"'))
class mformat_geo_abr(tag):    #abreviated geo microformat
        __slots__ =  []
    #contents='', attributes='', name=None   
        def __init__(self,latLng, contents=''): 
            tag.__init__(self,contents, name='abbr')
            self.attrSetClass('geo')
            self.attrSetTitle(latLng)  
class incl(tag):
    __slots__ =  []
    def __init__(self, contents=''):
        tag.__init__(self,utlbs.fl_read_or_str(contents)[0])  
    def _toStrOpen(self) :return u''
    def _toStrClose(self):return u''
class tag_dummy(tag):  
    __slots__ =  []
    def __init__(self, contents=''):
        tag.__init__(self,contents)   
    def _toStrOpen(self) :return u''
    def _toStrClose(self):return u''
 
class remark(tag):
    __slots__ =  [] 
    def _toStrOpen(self) :return '<!-- '
    def _toStrClose(self):return  ' -->'     
class ul(tag):
    __slots__ =  []
    class li(tag):__slots__ =  [] 
    def __init__(self, contents='', attributes=''): 
        tag.__init__(self,'',  attributes)
        #self.attrSetClass('nm-lev-00') 
        if contents !='':
            rt=lst_to_tag(contents, type(self), self.li) 
            if isinstance(rt, type(self)): 
                if isinstance(rt.contents, (basestring, tag)):self.contents=rt
                else:
                    for it in rt.contents: self.insertContents(it)
        else:
            self.contents=""  
    def validateContents(self, conts):
        if isinstance(conts, (basestring, tag)):      return True 
        elif isinstance(conts, (list, tuple)): return all([isinstance(it, (tag, basestring)) for it in conts]) 
        else:return False       
class ol(ul):__slots__ =  [] 
class table(tag): 
    class caption(tag):__slots__ =  []
    class colgroup(tag):__slots__ =  []
    class thead(tag):__slots__ =  []
    class tbody(tag):__slots__ =  [] 
    class tr(tag):__slots__ =  []
    class td(tag):__slots__ =  []
    class th(tag):__slots__ =  []
    class tfoot(tag):__slots__ =  [] 
    class col(tag):
        __slots__ =  []
        _nonclosing=True
    tcaption=None 
    tcolgroup=None
    head=None 
    body=None 
    foot=None  
    def __init__(self, contentslst = [], attributes='',caption = False, headerlst = [], footerlst= [], tagColums=True, contentsStr=None):
        tag.__init__(self,'',  attributes) 
        if caption:self.insertCaption (caption)   
        if tagColums and contentslst:  
            self.tcolgroup=self.colgroup()  
            NumOfColumns = len (contentslst[0]) if isinstance(contentslst[0], list) else len(contentslst) 
            #for i in range (NumOfColumns):self.tcolgroup.insertContents (tag('', "class=\"nm-tcol" + str(i)  +"\"" , 'col')) 
            for i in range (NumOfColumns):self.tcolgroup.insertContents (self.col('', "class=\"nm-tcol" + str(i)  +"\"" )) 
            self.insertContents(self.tcolgroup)  
        if headerlst !=[] :  
            self.head=self.thead(self.trFromList(headerlst))
            self.insertContents(self.head) 
        if contentslst !=[]:  
            self.body=self.tbody(self.trFromList(contentslst)) 
            self.insertContents(self.body)
            self.attrAppendClass('nm-t-rows-' + str(len(contentslst)))
        elif isinstance (contentsStr, basestring): #incase we have a td tr str 
            self.body=self.tbody("%s%s%s" %(self._cnstEOL, contentsStr, self._cnstEOL) )
            self.insertContents(self.body)   
        if footerlst !=[]:
            self.foot=self.tfoot(self.trFromList(footerlst))
            self.insertContents (self.foot)
    def insertCaption(self, val='', atrs=''):
        self.tcaption = self.caption(val, atrs)
        self.insertContents(self.tcaption, 0)
    @classmethod
    def trFromList(cls, lst, row=0):
        def tdr(it):
            tr=cls.tr(it)
            tr.attrAppendCnt(row)
            return tr
            #return cls.tr(it, '%s%02d %s%s' %("class=\"nm-t-r",  row ,  'nm-t-even'  if row % 2 == 0 else 'nm-t-odd',  "\""))
        if isinstance(lst[0], list):
            return [cls.trFromList(item, lst.index(item)+1) for item in lst]
        else:return tdr([cls.td(it) for it in lst]) 
class dividerTable(table):
    def __init__(self, *args, **kargs):
        table.__init__(self, *args, **kargs) 
        self._name='table' 
        self.attrAppendClass('nm-dividerTbl')
        self.setwidths()
    def setwidths(self):
        self.attrAppend('width', '100%')
class noscript(tag):__slots__ =  []          
class script(tag):
    __slots__ =  []
    def __init__(self,  contents='', src=False):
        #if contents!='':contents=dummytag(contents) 
        tag.__init__(self, contents)  
        self.attrSet('type', 'text/javascript')
        self.attrSet('charset', 'utf-8')
        if src:self.attrSetSrc(src)  
    def attrSetSrc(self, src):self.attrSet('src',src)
    def insertContents(self, contents):  
        #super(type(self), self).insertContents(dummytag(contents)) 
        if contents !='' :
            if isinstance(contents, tag): return tag.insertContents(self, contents) 
            else:return tag.insertContents(self, tag_dummy(contents)) 
class urlset(tag):   ##=sitemap
    def __init__(self): 
        tag.__init__(self)  
        self.attrSet('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    def addUrl(self, loc,lastmod='', changefreq='weekly', priority='0.5' ):
        url=self.insertContents(tag(name='url'))
        url.insertContents(tag(loc, '', 'loc'))
        url.insertContents(tag(lastmod, '', 'lastmod'))
        url.insertContents(tag(changefreq, '', 'changefreq'))
        url.insertContents(tag(priority, '', 'priority'))
    def _toStrOpen(self):
        return  '<?xml version="1.0" encoding="UTF-8"?>\n' + tag._toStrOpen(self)  
class CDATA(tag):
    __slots__ =  []
    def _toStrOpen(self):
        return  u'[CDATA[' 
    def _toStrClose(self):
        return   u']]'     

######################################  helpfull functions

class html(tag): 
    doctype=""
    preHtml=""                       #whatever we want after doc declaration and html tag 
    class head(tag): 
        class meta(tag):
            __slots__ =  [] 
            _nonclosing=True 
            def __init__(self,contents="",attributes="", name="",content=""):  
                tag.__init__(self,contents,attributes)
                if name !="":
                    self.attrSetName(name)
                    self.attrSet('content', content) 
#                else:
#                    if description!="":self.attrSetDescription(description) 
#            def attrSetDescription(self, val): 
#                self.attrSetName('description')  
#                self.
        class link(tag):
            __slots__ =  [] 
            _nonclosing=True 
            def __init__(self,contents='',rel='',href='',sizes='',idAttr=None): 
                tag.__init__(self,contents)    
                if rel:self.attrSet('rel',rel)
                if href:self.attrSet('href',href) 
                if sizes:self.attrSet('sizes',sizes)
                if idAttr:self.attrSetId(idAttr)
        class title(tag) :
            _slots__ =  []
            def __init__(self,title=''): tag.__init__(self,title)
    class body(tag):
        __slots__ =  [] 
        def __init__(self): tag.__init__(self,name=u"body")     
    def __init__(self,doctype=doctype_html5):
        self.doctype=doctype 
        self.head=self.head()
        self.meta=self.head.insertContents(tag_dummy() )
        self.body=self.body()
        tag.__init__(self, [self.head, self.body], name=u'html') 
        #define name so is ready for child classes 
    def metaSet (self, contents="",attributes="", name="",content=""):
        return self.meta.insertContents(self.head.meta(contents,attributes, name,content))
    def _toStrOpen(self):
        return   self.doctype +'\n' + self.preHtml + tag._toStrOpen(self)
    
def h1_6(caption, level):
    return tag(caption, 'class=\"nm-hd\"',  name='h'+str(min(6,level)))
def lst_to_ul(arg, dowhat=lambda x: x, byme=False):
    def myUL(it):  
        return   tag(it , '', 'ul')   
    def ff (it):
        return ul.li(dowhat(it)) 
    if  isinstance(arg, list): 
        return  ul.li([ dowhat(arg[0]), myUL([ lst_to_ul(it, dowhat) if isinstance(it, list) else ul.li(dowhat(it))  for it in  arg[1]] ) ] ) 
    else:
        return  ul.li(dowhat(arg) )
def lst_to_tag(l, tag, attrs=''):
    for li in l: 
        if  isinstance(li, basestring): 
            l[l.index(li)] = tag(li, attrs)
        else: 
            lst_to_tag(li, tag, attrs)
def lst_to_tag2(item, listCls=div, itemCls=p, level=0):  
    if isinstance(item, (basestring, tag)): 
        return itemCls(item)
    elif isinstance(item, list): 
        ContLst=listCls()
        ContLst.attrSetClass("nm-lev-" + "%02d" % level)
        cnt=-1
        for it in item:
            cnt +=1
            vl=lst_to_tag2(it, listCls, itemCls, level+1)
            vl.attrAppendCnt(cnt) 
            ContLst.insertContents(vl)   
        return ContLst
def lst_to_tag3(item, listCls=ul, itemCls=ul.li, level=0, lastItem=False):  
    if isinstance(item, (basestring, tag)): 
        lastItem=itemCls(item)
        return lastItem
    elif isinstance(item, list): 
        if not lastItem: ContLst=listCls()
        else:ContLst=lastItem 
        for it in item: 
            vl=lst_to_tag3(it, listCls, itemCls, level+1, lastItem) 
            ContLst.insertContents(vl)   
        return ContLst
def lst_to_tag_bookmark(l, attrs='', baseUri=''):
    for li in l: 
        if  isinstance(li, basestring): 
            l[l.index(li)] = a(li,attrs, baseUri+"#"+li)
        else: 
            lst_to_tag_bookmark(li,  attrs)               
def lst_of_tags(item, cls=p):  
    if isinstance(item, list): 
        return  [lst_of_tags(it, cls) for it in item]
    else:
        return cls(item)
def item_to_ul_li(arg, dowhat=lambda x: x, byme=False):
    if isinstance(arg, list):  
        return tag([item_to_ul_li(it, dowhat, True)  for  it in arg ], '', 'ul' ) if byme else tag_dummy([item_to_ul_li(it, dowhat, True)  for  it in arg ] )
    else: 
        return (ul.li(dowhat(arg)))  