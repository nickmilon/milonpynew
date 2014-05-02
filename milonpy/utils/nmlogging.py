#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################
'''
module: utilities.loggingNM
Created:Nov 17, 2012
author: milon
Description:                           
'''
#######################################################
import logging,time
from logging.handlers import TimedRotatingFileHandler
from basic import color_txt   

class ColoredFormatter(logging.Formatter): 
    def format(self, record): #@ReservedAssignment
        levelno = record.levelno 
        if(levelno >= 50):  color = (1,31)  # red dark       # CRITICAL / FATAL
        elif(levelno >= 40):color = (0,31)  # red            # ERROR 
        elif(levelno >= 30):color = (1,33)  # yellow         # WARNING 
        elif(levelno >= 20):color = (0,32)  # green          # INFO 
        elif(levelno >= 10):color = (1,35)  # pink           # DEBUG 
        else:               color = (0,)    # normal         # NOTSET and anything else 
        return color_txt(color, logging.Formatter.format(self, record)) 
 
def nmlogger(loggerName="log",levelConsol=logging.DEBUG,levelFile=logging.DEBUG,filename="~/log_"+__name__,verbose=1,when='midnight',interval=1,backupCount=7):
    """ http://docs.python.org/2/howto/logging-cookbook.html#
    """  
    
    logger = logging.getLogger(loggerName)
    logger.setLevel(min(levelConsol if levelConsol else 100,levelFile if levelFile else 100) )
    frmt=u"{'dt':'%(asctime)s','ln':'%(name)s' ,'lv':'%(levelname)-8s','msg':'%(message)s'"
    if verbose >1:frmt+="\n\t\t\t,'Func': '%(funcName)-10s','line':%(lineno)4d, 'module':'%(module)s', 'file':'%(filename)s'"  
    if verbose >2:frmt+="\n\t\t\t,'Process':['%(processName)s', %(process)d], 'thread':['%(threadName)s', %(thread)d], 'ms':%(relativeCreated)d"
    frmt+="}"
    if levelFile:
        formatter = logging.Formatter(frmt.replace(" ","")) 
        formatter.converter=time.gmtime
        #hf = logging.FileHandler('log_'+__name__ + ".log") 
        hf=TimedRotatingFileHandler(filename, when=when, interval=interval, backupCount=backupCount, encoding='utf-8', delay=False, utc=True)
        hf.setFormatter(formatter)  
        hf.setLevel(levelFile)
        logger.addHandler(hf)
    if levelConsol:
        frmtC=frmt.translate(dict((ord(c), u'') for c in u"'{},"))
        formatterC = ColoredFormatter(frmtC)
        formatterC.converter=time.gmtime
        hs =logging.StreamHandler()
        hs.setLevel(levelConsol)
        hs.setFormatter(formatterC)
        logger.addHandler(hs)
    return logger
                
    #logging.basicConfig(filename=__name__+".log", level=logging.DEBUG)