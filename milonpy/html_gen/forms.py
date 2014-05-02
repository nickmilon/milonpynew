#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################
'''
module: html.page
Created:Apr 12, 2012
author: milon
Description:                           
'''
#######################################################
#from tags import * #!!!@UnusedWildImport
#import tags
#from .tags import *
from tags import  * #@UnusedWildImport
class form(tag):
    __slots__ =  []  
    def __init__(self, contents='', attributes='',  method="post", action=False):
        tag.__init__(self,contents, attributes) 
        if method:self.attrSetMethod (method)
        if action:self.attrSetAction (action)
    def attrSetMethod(self, val):        return self.attrSet('method', val)          
    def attrGetAction(self):             return self.attrGet('action')
    def attrSetAction(self, val):        return self.attrSet('action', val)
    def setNoValidate(self):self.attributes.setFlag("novalidate") 
        #if self.contents.find('novalidate')==-1:self.insertContents("novalidate",-1) 
    class label(tag): 
        def __init__(self, contents='', attributes='',  _for=''):
            tag.__init__(self,contents, attributes)   
            self.attrSetFor(_for ) 
        def attrGetFor(self):       return self.attrGet('for')
        def attrSetFor(self, val):  return self.attrSet('for', val)

    class radio_list(tag_dummy):
        def __init__(self,name="gr1",valList=[],required=False):
            tag_dummy.__init__(self)
            # align='align=\"xx\"'.replace("xx",align)
            for ix, item in enumerate(valList):
                idvl="frm-%s-%d" %(name,ix)
                inp=input(value=item[0],type="radio",required=True,name=name)
                inp.attrSetId(id)
                self.insertContents(span([inp,form.label(item[1],"",idvl)])) 
            #TODO: needs fixing why we don not inherit from formfied?
            #self.insertContents(NMhtml.span(item[1]))
            #if value:self.attrSet('value', value)  
            #return [ input(align, value=i,type="radio",name=name) for i in valList ]       
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
    class textarea(form_tag):
        _nonclosing=False 
        def __init__(self, attributes='', type='text', value=False,name=False,placeholder=False,required=False,rows="10",cols="60"): #@ReservedAssignment
            form.form_tag.__init__(self,"", attributes,value,name,placeholder,required) 
            #if value:self.attrSet('value', value) 
            if rows:self.attrSet('rows', rows)
            if cols:self.attrSet('cols', cols)      
    class input(form_tag): #@ReservedAssignment
        def __init__(self, contents='', attributes='', type='text', value=False,name=False,placeholder=False,required=False): #@ReservedAssignment
            form.form_tag.__init__(self,contents, attributes,value,name,placeholder,required) 
            #if value:self.attrSet('value', value) 
            self.attrSet('type', type) 
        def attrGetMin(self):       return self.attrGet('min')
        def attrSetMin(self, val):  return self.attrSet('min', val)   
        def attrGetMax(self):       return self.attrGet('max')
        def attrSetMax(self, val):  return self.attrSet('max', val) 
        def attrGetStep(self):      return self.attrGet('step')
        def attrSetStep(self, val): return self.attrSet('step', val)
    class option(form_tag):
        __slots__ =  []  
        _nonclosing=False
        def __init__(self, contents='', attributes='',  value=False, selected=False):
            form.form_tag.__init__(self,contents, attributes) 
            if value:self.attrSet('value', value)
            if selected:self.attrSet('selected', 'selected')
    class select(tag):
        __slots__ =  []   
        def __init__(self, optionslst=[], attributes='',selected=None,multiple=None,size=None):
            tag.__init__(self,"", attributes)  
            if multiple is not None:self.attrSet('multiple', "multiple")
            if multiple is not None:self.attrSet('size', size)
            for cnt,opt in enumerate(optionslst): 
                optSel=True if selected is not None and selected == opt[0] else False 
                curOption=form.option(opt[1],"",opt[0],selected=optSel)
                curOption.attrAppendCnt(cnt+1) 
                self.insertContents(curOption)                
    class button(form_tag):
        __slots__ =  [] 
        _nonclosing=False 
        def __init__(self, contents='', attributes='',  OnClick=False):
            form.form_tag.__init__(self,contents, attributes) 
            if OnClick:self.attrSet('OnClick', OnClick) 
