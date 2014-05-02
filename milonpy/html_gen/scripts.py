#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################
'''
module: web.html_scripts 
Created:Apr 12, 2012
author: nickmilon 
Description:             Miscelaneus scripts               
'''
#######################################################
from tags import script





class script_ganalytics(script):
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

class gjsapi(script):    	# google jsapi
    __slots__ =  []
    def __init__(self):
        script.__init__(self,src = "http://www.google.com/jsapi")
        self._name='script'
class gmaps_v3(script):    	# google maps Version 3
    __slots__ =  []
    def __init__(self):
        script.__init__(self,src = "http://maps.google.com/maps/api/js?sensor=false")
        self._name='script'
class singleton(script):
    __slots__ =  []
    def __init__(self,varName, **kargs):
        script.__init__(self)
        self._name='script'
        print kargs 
        varbls = ""
        for k in kargs.keys():
            val = "\"" + kargs[k] + "\"" if isinstance(kargs[k], basestring) else  str(kargs[k])
            varbls += "\t" + k + ": " + val  + ",\n" 
        varbls=varbls[:-2]+'\n'    
        self.contents="\n\tvar %s = {\n %s\t}\n" %(varName, varbls)  