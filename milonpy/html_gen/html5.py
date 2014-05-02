'''
Created on Nov 26, 2013

@author: milon
'''
from tags import  *  #@UnusedWildImport 
from forms import *  #@UnusedWildImport 
#from scripts import script_ganalytics
doctype_current=doctype_html5
GL_DEBUG=True
GL_JQVERSION='2.0.3'
GL_ANGULARVERSION='1.2.2'
#//ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js

 
    
def script_JQ(as_str=False): 
    if GL_DEBUG:
        rt= [script("","/assets/js/jquery-%s.js"  %(GL_JQVERSION) )]    
    else: 
        rt= [
              script("","//ajax.googleapis.com/ajax/libs/jquery/%s/jquery.min.js" %(GL_JQVERSION) ),   
              script("""window.jQuery || document.write('<script src="/assets/js/jquery-%s.min.js"></script>')"""  %(GL_JQVERSION) )
            ]
    return "".join([str(i) for i in rt]) if as_str else rt

def script_BSJS(as_str=False): 
    if GL_DEBUG:
        rt= script("","/assets/js/bootstrap.js")    
    else: 
        rt= script("","/assets/js/bootstrap.min.js")  
    return str(rt) if as_str else rt   
def script_angular(as_str=False): 
    if GL_DEBUG:
        rt= script("","https://ajax.googleapis.com/ajax/libs/angularjs/%s/angular.js" %(GL_ANGULARVERSION))  
    else: 
        rt= script("","https://ajax.googleapis.com/ajax/libs/angularjs/%s/angular.min.js" %(GL_ANGULARVERSION)) 
    return str(rt) if as_str else rt      

class html5(html): 
    def __init__(self,lng="en",title='',description='',author='',robots="index,follow",iconPath="",**kwargs):
    #def __init__(self, **kargs):
        html.__init__(self,**kwargs) 
        self.attrSet('lang', lng)  
        self.metaSet("",[ ["charset","utf-8"]]) 
        if title: self.head.insertContents(self.head.title(title))
        if description:self.metaSet("","","description",description)
        self.metaSet("","","viewport","width=device-width, initial-scale=1.0")  
        if author:self.metaSet("","","author", author)   
        self.metaSet("","","robots", robots) 
        if iconPath:
            rel="apple-touch-icon-precomposed"
            if GL_DEBUG:self.head.insertContents(remark("Fav and touch icons ") )
            self.head.insertContents(self.head.link("",rel,iconPath+"apple-touch-icon-144-precomposed.png","144x144"))
            self.head.insertContents(self.head.link("",rel,iconPath+"apple-touch-icon-114-precomposed.png","114x114"))
            self.head.insertContents(self.head.link("",rel,iconPath+"apple-touch-icon-72-precomposed.png","72x72"))
            self.head.insertContents(self.head.link("","shortcut icon",iconPath+"favicon.png"))  
            self.head.insertContents(self.head.link("","apple-touch-icon",iconPath+"apple-touch-icon.png"))
            tmp=self.head.insertContents(self.head.link("","icon",iconPath+"animated_favicon.gif"))
            tmp.attrSet("type", "image/gif")
            if GL_DEBUG:self.head.insertContents(remark(" - " * 10))    
        self.divInfo=self.body.insertContents(div("",'id=\"nm-divinfo\"'))
        self.divInfo.insertContents(i("",'class=\"fa  fa-spinner fa-spin \"'))
        self.body_wrapper=self.body.insertContents(div("",'id=\"nm-body-wrapper\"'))  
        self.header=self.body_wrapper.insertContents(tag(name="div"))  #@1
        #@@self.main=self.body_wrapper.insertContents(div("",'id=\"nm-main\" role=\"main\"'))
         
        return self
################ 
class html5bs3(html5):
    """ html5 bootsrap see 
        http://twitter.github.com/bootstrap
        http://getbootstrap.com/ 
    """
    def __init__(self,angularApplName=None,BSjs=False,**kwargs):  
        self.html=html5.__init__(self,**kwargs)
        self.head.insertContents(self.head.link("","stylesheet","/static/css/bootstrap.css",id="ss-BS1"))  
        self.head.insertContents(self.head.link("","stylesheet","/static/css/tinfo.css",id="ss-BS2")) 
        self.head.insertContents(self.head.link("","stylesheet",'/static/css/nm-twtstream.css'))  
        self.head.insertContents(self.head.link("","stylesheet","/assets/css/font-awesome.min.css",id="ss-fa")) 
        #self.head.insertContents(self.head.link("","stylesheet","//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css",id="BS3")) 
         
         
        #self.head.insertContents(self.head.link("","stylesheet","/static/css/bootstrap_slate.css",id="BS2")) 
        if BSjs:
            self.head.insertContents(script_JQ())  
            self.head.insertContents(script_BSJS())        
        if angularApplName: 
            self.html.attrSet("ng-app",angularApplName) 
        self.header.attrSetClass("navbar navbar-inverse navbar-fixed-top")
        self.header.attrSetRole("navigation") 
          
        # ng-controller="HelloCntl"
        #self.BS_NB_container=self.header.insertContents(div("",'class=\"container\"' )) 
        #self.BS_NB_container_header=self.BS_NB_container.insertContents(div("",'class=\"navbar-header\"' ))
        
        #tmp2=tmp1.insertContents(sheader)
        #tmp2=tmp1.insertContents(forms.form.button ("signed={{user_signed}}", 'type=\"button\" class=\"navbar-toggle\"')) 
         
        #self.NB_container.insertContents("X X " * 1) 
    def button(self):
        pass
    