#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################
'''
module:  
Created:Apr 11, 2012
author: nickmilon
Description:          RSS Feed generator                  
'''
#######################################################
from tags import tag, tag_nc
 
class rss(tag): 
    """ http://www.rssboard.org/rss-specification 
        time tm.strftime(NMutl.rfc2822_DATE_FMT, tm.gmtime()) 
    """
    (isMRSS, isDC, isGeo)=(False, False, False)
    class channel(tag):
        class title(tag): __slots__ =  []  
        class link(tag): __slots__ =  []
        class description(tag): __slots__ =  []     
        # ------------------------------------------------------  optional   
        class language(tag):        __slots__ =  [] 
        class copyright(tag):       __slots__ =  [] #@ReservedAssignment
        class managingEditor(tag):  __slots__ =  [] 
        class webMaster(tag):       __slots__ =  [] 
        class pubDate(tag):         __slots__ =  [] 
        class lastBuildDate(tag):   __slots__ =  [] 
        class category(tag):        __slots__ =  [] 
        class generator(tag):       __slots__ =  [] 
        class docs(tag):            __slots__ =  [] 
        class ttl(tag):             __slots__ =  [] 
        
        class rating(tag):          __slots__ =  []
        class textInput(tag):       __slots__ =  []
        class skipHours(tag):       __slots__ =  []
        class skipDays(tag):        __slots__ =  []
        class image(tag):        
            class url(tag):         __slots__ =  []
            class title(tag):       __slots__ = []
            class link(tag):        __slots__ = []
            def __init__(self,url,  title, link): 
                tag.__init__(self)  
                self._url=self.insertContents(self.url(url))
                self._title=self.insertContents(self.title(title))
                self._link=self.insertContents(self.link(link)) 
        def addItem(self, title=None, link=None, description=None,pubDate=None,  guid=None):
            return self.insertContents(self.item(title, link, description,pubDate,  guid))
        class item(tag): 
            class title(tag): __slots__ =  []
            class link(tag): __slots__ =  [] 
            class guid(tag): __slots__ =  [] 
            class pubDate(tag): __slots__ =  [] 
            class description(tag): __slots__ =  [] 
            class author(tag): __slots__ =  []
            class category(tag): __slots__ =  []
            class comments(tag): __slots__ =  []
            class source(tag): __slots__ =  []
            class enclosure(tag_nc):   
                def __init__(self,  **kargs): #url,length,type
                    tag_nc.__init__(self)  
                    for k in kargs.keys():self.attrSet(k, kargs[k]) 
            class dc_creator(tag_nc): 
                def __init__(self, creator): 
                    tag_nc.__init__(self, creator,  name='dc:creator')  
            class georss_point(tag):  
                def __init__(self, boundingbox): 
                    tag.__init__(self,  boundingbox , name='georss:point')          
            class media_content(tag):
                #"""http://www.rssboard.org/media-rss"""
                def __init__(self, **kargs ): 
                    tag.__init__(self, name='media:content') 
                    for k in kargs.keys(): 
                        self.attrSet(k, kargs[k]) 
                def setFields(self, title, description):
                    self.insertContents(tag(title,'',  name='media:title'))
                    self.insertContents(tag(description, name='media:description'))
            class media_thumbnail(tag_nc): 
                def __init__(self,  **kargs): 
                    tag_nc.__init__(self, name='media:thumbnail')
                    for k in kargs.keys():self.attrSet(k, kargs[k])  
            def __init__(self, title, link=None, description=None,pubDate=None,  guid=None): 
                tag.__init__(self)  
                if guid is None:guid=link  
                self._title=None if title is None else self.insertContents(self.title(title)) 
                self._link= None if link is None else self.insertContents(self.link(link)) 
                self._guid=None if guid is None else self.insertContents(self.guid(guid)) 
                self._pubDate=None if pubDate is None else self.insertContents(self.pubDate(pubDate)) 
                self._description=None if description is None else self.insertContents(self.description(description))  
        def __init__(self, title, link, description):
            tag.__init__(self) 
            #$self.insertContents(tag_nc( '','href=\"'+link+ '\"' +' type=\"application/rss+xml\" rel=\"self\"' ,  'atom:link'))
            self._title=self.insertContents(self.title(title))
            self._link=self.insertContents(self.link(link))
            self._description=self.insertContents(self.description(description))
    def __init__(self, channelTitle, channelLink, channelDescription, version="2.0", isMRSS=False, isDC=False, isGeo=False): 
        tag.__init__(self)  
        self.attrSet('version', version)
        (self.isMRSS, self.isDC, self.isGeo)=(isMRSS, isDC, isGeo)   
        self.isDC=isDC
        if isMRSS: self.attrSet( 'xmlns:media',  "http://search.yahoo.com/mrss/") 
        if isDC: self.attrSet('xmlns:dc',"http://purl.org/dc/elements/1.1/")  
        if isGeo:self.attrSet('xmlns:georss', "http://www.georss.org/georss")
        #----------------------------------------------------------------------------------------  
        self._channel=self.insertContents(self.channel(channelTitle, channelLink,  channelDescription))  
    def _toStrOpen(self):
        return  u'<?xml version="1.0" encoding="UTF-8"?>\n' + tag._toStrOpen(self)  
