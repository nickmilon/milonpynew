#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################
'''
module: html.gen_ext
Created:Apr 10, 2012
author: milon
Description:        html tags extensions                     
'''
#######################################################
from tags import *  #@UnusedWildImport 
import forms

from scripts import script_ganalytics

app_oldIE_note="""[if lt IE 7]><p class=chromeframe>Your browser is <em>ancient!</em> <a href="http://browsehappy.com/">Upgrade to a different browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">install Google Chrome Frame</a> to experience this site.</p><![endif]"""






class html5(html):
    def __init__(self,lng="en",title='',description='',author='',robots="index,follow",iconPath="",stylesheets=[],**kwargs):
    #def __init__(self, **kargs):
        html.__init__(self,doctype_html5) 
        self.attrSet('lang', lng)
        #self.attrSet("ng-app","MyApp")
        self.metaSet("",[ ["charset","utf-8"]])
        self.metaSet("",[ ["http-equiv","X-UA-Compatible"],["content","IE=edge,chrome=1"]]) 
        if title: self.head.insertContents(self.head.title(title))
        if description:self.metaSet("","","description",description)
        self.metaSet("","","viewport","width=device-width") 
        if author:self.metaSet("","","author", author)   
        self.metaSet("","","robots", robots) 
        if iconPath:
            self.head.insertContents(self.head.link("","shortcut icon",iconPath+"favicon.ico"))
            self.head.insertContents(self.head.link("","apple-touch-icon",iconPath+"apple-touch-icon.png"))
            rt=self.head.insertContents(self.head.link("","icon",iconPath+"animated_favicon.gif"))
            rt.attrSet("type", "image/gif")    
        for item in stylesheets:self.head.insertContents(self.head.link("","stylesheet",item))    
     
        self.container=self.body.insertContents(div("",'id=\"container\"'))  
        self.header=self.container.insertContents(tag(name="header"))
        self.main=self.container.insertContents(div("",'id=\"main\" role=\"main\"'))
        self.footer=self.container.insertContents(tag(name="footer")) 
        return self
class html5BS(html5): 
    """ html5 bootsrap see http://twitter.github.com/bootstrap""" 
    def __init__(self,*args,**kwargs):  
        self.HTML=html5.__init__(self, **kwargs)  
        # bsCSS= self.head.link("","stylesheet","/recources/css/bootstrap.css")
        self.bsCSS= self.head.link("","stylesheet","/assets/css/bootstrap.css")
        ix,firstCSS=self.head.getByAttr('rel',"stylesheet") #@UnusedVariable
        if ix is None:
            self.head.insertContents(self.bsCSS)
        else:
            self.head.insertContents(self.bsCSS,max(0,ix)) #insert before first CSS
        rm=remark(app_oldIE_note)
        self.head.insertContents(style("body {padding-top: 60px;padding-bottom: 40px;}"))
        self.body.insertContents(rm,0)  
        tmp=self.body.insertContents(div("","id=\"jscode\""))
        tmp.insertContents(script("","//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js")) 
        tmp.insertContents(script("""window.jQuery || document.write('<script src="/recources/js/jquery-1.7.2.min.js"></script>')""" ))
        tmp.insertContents(script("","/assets/js/bootstrap.js ")) 
        #tmp.insertContents(script("","/assets/js/plugins.js "))   
        self.jsCode=tmp
#    def setJS(self,fileUpload=False):
#        tmp=self.jscode 
#        if fileUpload:
#            tmp.insertContents(script("","//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js")) 
#            tmp.insertContents(script("""window.jQuery || document.write('<script src="/recources/js/jquery-1.7.2.min.js"><\/script>')""" )) 
    def setContainer(self,parentEl,contents="",fluid=True):
        tmp=parentEl.insertContents(div(contents))
        tmp.attrSetClass("container-fluid" if fluid else "container" )      
        return tmp
    def setRow(self,parentEl,contents="",fluid=True):
        tmp=parentEl.insertContents(div(contents))
        tmp.attrSetClass("row-fluid" if fluid else "row" )      
        return tmp
    def setRowContents(self,parentRow,contents="",span=1,offset=0,fluid=True):
        tmp=div(contents)
        tmp.attrSetClass("span"+str(span))
        if fluid and offset > 0 :
            tmp1=parentRow.insertContents(div("",'class=\"dummy-offset\"'))
            tmp1.attrAppendClass("span" +str(offset)) 
        else:
            tmp.attrAppendClass("offset"+ str(offset))
        parentRow.insertContents(tmp)  
        return tmp    
    def setTab(self,ID, contLst,activeTabNum=0): 
        """contLst = [[tabHeader,tabIcon,tabContents]...]"""
        tb=tag_ws("",'class=\"tabbable\"',name="div")
        tb.attrSetId(ID)
        tb.tabs= tb.insertContents(ul("",'class=\"nav nav-tabs\"'))   
        tb.cont = tb.insertContents(div("",'class=\"tab-content\"'))
        
        for ix,item in enumerate(contLst):
            tab=tb.tabs.insertContents(ul.li())
            if ix==0:tab.attrSetClass("active")
            tmp=tab.insertContents(a("",'data-toggle=\"tab\"',"#"+ID+str(ix+1)) ) 
            
            if item[1]:
                tmpi=tmp.insertContents(i())
                tmpi.attrSetClass(item[1])
            tmp.insertContents(item[0])    
            #tmp=tab.insertContents(a([i("",'class=\"icon-book\"'), item[0]],'data-toggle=\"tab\"',"#"+ID+str(ix+1)) )  
            #"",'class=/"icon-book"'
            pane=tb.cont.insertContents(div(item[2],'class=\"tab-pane\"'))
            if ix==activeTabNum:
                tab.attrSetClass("active")
                pane.attrAppendClass("active") 
            pane.attrSetId(ID+str(ix+1))     
        return tb    
    def NavBar(self,titleLinkLst,linksLst,fluid=True,inclSignIn=True):    
        NB=tag_ws("",'class=\"navbar navbar-fixed-top\"',name="div")  #
        NB.inner=NB.insertContents(div("",'class=\"navbar-inner\"' )) 
        NB.inner.attrSetId("nbinner")  
        NB.inner.attrSet("ng-controller","HelloCntl")  
        NB.container=self.setContainer(NB.inner,a("",'class=\"btn btn-navbar\" data-toggle=\"collapse\" data-target=\".nav-collapse\"' ), fluid) 
        NB.btna=NB.container.insertContents(a("",'class=\"btn btn-navbar\" data-toggle=\"collapse\" data-target=\".nav-collapse\"' ))
        for item in linksLst: NB.btna.insertContents(span("",'class=\"icon-bar\"')) #@UnusedVariable
        NB.container.insertContents(a(titleLinkLst [0],'class=\"brand\"',titleLinkLst[1])) 
        if inclSignIn:
            NB.BUTTON_GROUP=NB.container.insertContents(div("",'class=\"btn-group pull-right\"'))
            #NB.BUTTON_GROUP.attrSet("ng-controller","HelloCntl") 
            #contents='', attributes='',  OnClick=False 
             
            siwt=img(src='/static/img/sign-in-with-twitter-link.png',
                       alt='sign in with twitter', title="sign in with twitter", height=False, width=False)
            siwt=a(siwt,href="../oauth/start/alopeki/a_session/", target=False, title=False)
            tmp=NB.BUTTON_GROUP.insertContents(forms.form.button ("signed={{user_signed}}", 'type=\"button\" class=\"btn btn-default\"')) 
            tmp=NB.BUTTON_GROUP.insertContents(forms.form.button (siwt, 'type=\"button\" class=\"btn btn-default\"')) 
            tmp.attrSet('ng-hide',"user_signed")
            tmp=NB.BUTTON_GROUP.insertContents(forms.form.button ("@{{session_username}} ", 'type=\"button\" class=\"btn btn-default\"'))
            tmp.attrSet('ng-show',"user_signed") 
            tmp=NB.BUTTON_GROUP.insertContents(forms.form.button ("swap", 'type=\"button\" class=\"btn btn-default\"')) 
            tmp.attrSet('ng-click','swap()' )
            #mp2=NB.BUTTON_GROUP.insertContents(a(i("",'class=\"icon-cog\"'),'class=\"btn dropdown-toggle\" data-toggle=\"dropdown\"'))
            tmp2=NB.BUTTON_GROUP.insertContents(ul("",'class=\"dropdown-menu\"')) 
            #tmp2.insertContents(span("",'class=\"caret\"')) .glyphicon .glyphicon-cog
            tmp=tmp2.insertContents(ul.li(a("Sign out","","#")))  
            tmp.attrSet('ng-click','user_unsign()')
            tmp.attrSet('ng-show',"user_signed")
            
            tmp2.insertContents(ul.li("",'class=\"divider\"')) 
            tmp2.insertContents(ul.li(a("Settings","","#")))
            #====================================================================
            #  #mdl=tmp1.insertContents(div ("","{{username}}"))
            #  #NB.BUTTONS=tmp1.insertContents(div("",'class=\"btn-group'))
            
            
            #  
            #  
            #  tmp2=NB.BUTTON_GROUP.insertContents(a([i("",'class=\"icon-user\"'),sit],'class=\"btn dropdown-toggle\" data-toggle=\"dropdown\"'))
            #  
            #  mp2=NB.BUTTON_GROUP.insertContents(a([i("",'class=\"icon-user\"'),sit],'class=\"btn dropdown-toggle\" data-toggle=\"dropdown\"'))
            #  tmp2.attrSetHref("#") #TODO:real link
            #  #NB.iconn_user=tmp2.insertContents(i("",'class=\"icon-user\"'))
            # 
            #  
            #  #tmp2.insertContents("{{username}}")
            #  tmp2.insertContents(span("",'class=\"caret\"'))
            #  tmp2=NB.BUTTON_GROUP.insertContents(ul("",'class=\"dropdown-menu\"')) 
            #  tmp2.insertContents(ul.li(a("Profile","","#")))
            #  tmp2.insertContents(ul.li("",'class=\"divider\"')) 
            #  #tmp2.insertContents(ul.li(a("Sign In","","#")))
            #  #tmp2.insertContents(ul.li(a("Sign Out","","#")))  
            #  NB.a_SignInLinks=tmp2
            #====================================================================
                                                         
        NB.nav=NB.container.insertContents(div("",'class=\"nav-collapse\"'))
        NB.navUL=NB.nav.insertContents(ul("",'class=\"nav\"'))
        #    self.navUL.attrSetClass("nav") #######edo
        NB.navUL.insertContents(ul.li("","class=\"divider-vertical\""))
        for ix,item in enumerate(linksLst):
            tmp=NB.navUL.insertContents(ul.li(a(item[0],"",item[1])))
            if ix==0:tmp.attrSetClass("active")
        NB.navUL.insertContents(ul.li("","class=\"divider-vertical\""))
        #NB.container.insertContents(remark('/.nav-collapse' )) 
        return NB 
 
    def set_up (self, ganalyticsAccount=None,inclIEcomp=True):
        if ganalyticsAccount:self.jsCode.insertContents(script_ganalytics(ganalyticsAccount)) 
        if inclIEcomp: self.head.insertContents(remark("[if lt IE 9]><script src=\"http://html5shim.googlecode.com/svn/trunk/html5.js\"></script><![endif]"))   
        return       