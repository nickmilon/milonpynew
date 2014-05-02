#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################

'''
original Created on Mar 15, 2011
'''
import tags  as NMhtml
tagOld=NMhtml.tag
cssConditional="""
    <!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
    <!--[if lt IE 7 ]> <html class="no-js ie6" lang="en"> <![endif]-->
    <!--[if IE 7 ]>    <html class="no-js ie7" lang="en"> <![endif]-->
    <!--[if IE 8 ]>    <html class="no-js ie8" lang="en"> <![endif]-->
    <!--[if (gte IE 9)|!(IE)]><!--> <html class="no-js" lang="en"> <!--<![endif]--> 
            """
class tag(tagOld):
    def getByAttr(self,attr,val,repl=None,insertIfNF=False):
        #TODO: works for 1st level make it recursive
        for ix,item  in enumerate(self.contents):
            if isinstance(item,tag) and item.attrGet(attr) == val:
                if repl is not None:
                    self.contents[ix]=repl
                return item
        if insertIfNF and repl is not None:self.insertContents(repl)        
        return None
        #return [item for item in self.contents if isinstance(item,tag) and item.attrGet(attr) == val ]
         
#class tagBlank(tag):
#    __slots__ =  [] 
#    _nonclosing=True 
#    def __init__(self,contents='', attributes=''): tag.__init__(self,contents,attributes, name=u"")
class script_ganalytics(NMhtml.script):
    def __init__(self,account):
        contents="""var _gaq = _gaq || [];
          _gaq.push(['_setAccount', '$account$']);
          _gaq.push(['_trackPageview']); 
          (function() {
            var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
            ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(ga);
          })();"""
        super(script_ganalytics, self).__init__(contents.replace('$account$',account))
        self._name='script'   
class html(tag): 
    doctype=""
    preHtml="" #whatever we want after doc declaration and before html tag 
    class head(tag): 
        class meta(tag):
            __slots__ =  [] 
            _nonclosing=True 
            def __init__(self,contents="",attributes="",name="",description=""):  
                tag.__init__(self,contents,attributes)
                if name !="":self.attrSetName(name)
                if description!="":self.attrSetDescription(description) 
            def attrSetDescription(self, val): 
                self.attrSet('name','description')  
                return self.attrSet('content', val) 
        class link(tag):
            __slots__ =  [] 
            _nonclosing=True 
            def __init__(self,contents='',rel='',href=''): 
                tag.__init__(self,contents)    
                if rel!='':self.attrSet('rel',rel)
                if href!='':self.attrSet('href',href) 
        class title(tag) :
            _slots__ =  []
            def __init__(self,title=''): tag.__init__(self,title)
    class body(tag):
        __slots__ =  [] 
        def __init__(self): tag.__init__(self,name=u"body")     
    def __init__(self,doctype=5):
        if doctype==5:self.doctype="<!doctype html>"
        elif doctype==4:self.doctype= '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
        self.head=self.head()
        self.body=self.body()
        tag.__init__(self, [self.head, self.body], name='html') 
    def _toStrOpen(self):
        return   self.doctype +'\n' + self.preHtml + tag._toStrOpen(self)
    
class html5bp(html):
    #TODO:Scripts,media handheld 
    _relFavicon="shortcut icon" 
    _relTouchIcon="apple-touch-icon"    
    def __init__(self,title='',description='',author='',stylesheets=[]):
        html.__init__(self,5)
        self.preHtml=cssConditional
        self.head.insertContents(self.head.meta("",'charset=\"utf-8\"'))
        self.head.insertContents(self.head.meta("",'content-language=\"en\"')) 
        
        self.head.insertContents(self.head.meta("",'X-UA-Compatible=\"IE=edge,chrome=1\"'))
        if title!="":self.head.insertContents(self.head.title(title))
        self.head.insertContents(self.head.meta("","","description",description))
        self.head.insertContents(self.head.meta("","","author",author))
        self.head.insertContents(self.head.meta("",'viewport=\"width=device-width, initial-scale=1.0\"'))
        self.docSetFavicon("/favicon.ico")
        self.docSetTouchIcon("/apple-touch-icon.png")
        for item in stylesheets:self.head.insertContents(self.head.link("","stylesheet",item))
          
        self.container=self.body.insertContents(NMhtml.div("",'id=\"container\"'))  
        self.header=self.container.insertContents(tag(name="header"))
        self.main=self.container.insertContents(NMhtml.div("",'id=\"main\" role=\"main\"'))
        self.footer=self.container.insertContents(tag(name="footer"))
    def docSetFavicon(self,href): 
        self.head.getByAttr("rel",self._relFavicon,self.head.link("",self._relFavicon,href),True)
    def docSetTouchIcon(self,href):
        self.head.getByAttr("rel",self._relFavicon,self.head.link("",self._relTouchIcon,href),True)
            
class html5Twt(html5bp):
    def __init__(self,title='',description='',author='',stylesheets=[]):
        super(html5Twt, self).__init__(self,title='',description='',author='',stylesheets=[])
        self.header.insertContents(script_ganalytics("UA-10439541-3"))
##################################### html5 forms
class label(tag): 
    def __init__(self, contents='', attributes='',  _for=''):
        tag.__init__(self,contents, attributes)   
        self.attrSetFor(_for ) 
    def attrGetFor(self):       return self.attrGet('for')
    def attrSetFor(self, val):  return self.attrSet('for', val) 
class form_tag(tag):
    _nonclosing=True
    def __init__(self, contents='', attributes='',  value=False,name=False,placeholder=False,required=False):
        tag.__init__(self,contents, attributes) 
        if value:self.attrSetValue (value) 
        if name:self.attrSet('name', name) 
        if placeholder:self.attrSetPlaceholder(placeholder)
        if required:self.setRequired()
    def setRequired(self): 
        if self.contents.find('required')==-1:self.insertContents("required",-1) 
    def attrGetValue(self):             return self.attrGet('value')
    def attrSetValue(self, val):        return self.attrSet('value', val)   
    def attrGetPlaceholder(self):       return self.attrGet('placeholder')
    def attrSetPlaceholder(self, val):  return self.attrSet('placeholder', val)      
                      
class input(form_tag): #@ReservedAssignment
    def __init__(self, contents='', attributes='', type='text', value=False,name=False,placeholder=False,required=False): #@ReservedAssignment
        form_tag.__init__(self,contents, attributes,value,name,placeholder,required) 
        #if value:self.attrSet('value', value) 
        self.attrSet('type', type) 
    def attrGetMin(self):       return self.attrGet('min')
    def attrSetMin(self, val):  return self.attrSet('min', val)   
    def attrGetMax(self):       return self.attrGet('max')
    def attrSetMax(self, val):  return self.attrSet('max', val) 
    def attrGetStep(self):      return self.attrGet('step')
    def attrSetStep(self, val): return self.attrSet('step', val) 
class textarea(form_tag):
    _nonclosing=False 
    def __init__(self, attributes='', type='text', value=False,name=False,placeholder=False,required=False,rows="10",cols="60"): #@ReservedAssignment
        form_tag.__init__(self,"", attributes,value,name,placeholder,required) 
        #if value:self.attrSet('value', value) 
        if rows:self.attrSet('rows', rows)
        if cols:self.attrSet('cols', cols) 
     
class radioList(NMhtml.tag_dummy):
    def __init__(self,name="gr1",valList=[],required=False):
        NMhtml.tag_dummy.__init__(self)
        # align='align=\"xx\"'.replace("xx",align)
        for ix, item in enumerate(valList):
            idvl="frm-%s-%d" %(name,ix)
            inp=input(value=item[0],type="radio",required=True,name=name)
            inp.attrSetId(id)
            self.insertContents(NMhtml.span([inp,label(item[1],"",idvl)]))
            
            #self.insertContents(NMhtml.span(item[1]))
        #if value:self.attrSet('value', value) 
  
    #return [ input(align, value=i,type="radio",name=name) for i in valList ]           
class select(tag):
    __slots__ =  []  
    def __init__(self, optionslst=[], attributes='',selected=None,multiple=None,size=None):
        tag.__init__(self,"", attributes)  
        if multiple is not None:self.attrSet('multiple', "multiple")
        if multiple is not None:self.attrSet('size', size)
        for cnt,opt in enumerate(optionslst): 
            optSel=True if selected is not None and selected == opt[0] else False 
            curOption=option(opt[1],"",opt[0],selected=optSel)
            curOption.attrAppendCnt(cnt+1) 
            self.insertContents(curOption)     
                        
class option(form_tag):
    __slots__ =  []  
    _nonclosing=False
    def __init__(self, contents='', attributes='',  value=False, selected=False):
        form_tag.__init__(self,contents, attributes) 
        if value:self.attrSet('value', value)
        if selected:self.attrSet('selected', 'selected') 
class button(form_tag):
    __slots__ =  []  
    def __init__(self, contents='', attributes='',  OnClick=False):
        form.form_tag.__init__(self,contents, attributes) 
        if OnClick:self.attrSet('OnClick', OnClick)           
class form(tag):
    __slots__ =  []  
    def __init__(self, contents='', attributes='',  method="post", action=False):
        tag.__init__(self,contents, attributes) 
        if method:self.attrSetMethod (method)
        if action:self.attrSetAction (action)
    def attrSetMethod(self, val):        return self.attrSet('method', val)          
    def attrGetAction(self):             return self.attrGet('action')
    def attrSetAction(self, val):        return self.attrSet('action', val)
    def setNovalidate(self):self.attributes.setFlag("novalidate") 
        #if self.contents.find('novalidate')==-1:self.insertContents("novalidate",-1) 
 
def formItemDiv(title,formElem): 
    return NMhtml.div([title,formElem],'class=\"nm-frm-item\"') 