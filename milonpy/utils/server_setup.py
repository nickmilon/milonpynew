#!/bin/bash
'''     
        Server Setup some dirty code to automate server setup in debian.
        Needs sudo priviledges 
        Warning use it very carefully at your own risk
        Warning !!! prg_inst_path will be erased if specified
        usage push it first
            gcutil --project=twgnosi push nm02  /_prgs/git/nmcode/appls/src/automation/server_setup.py  server_setup.py
'''
__author__ = "Nick Milon"
__copyright__ = "Copyright 2011"
__credits__ = []
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Nick Milon"
__email__ = "nickmilon@gmail.com"
__status__ = "Development"

#@todo:  break it down to 2 one public and one private
 
import argparse 
import subprocess 
import socket
import re,sys,os
import time
import glob
import platform 


# platform.dist() ('debian', '7.0', '')
#===============================================================================
# rs.add({_id: 3, host: "nm-14:27017", priority: 10})
#===============================================================================

def cmdToLst(cmdStr):return cmdStr.split() 
 
      
parser = argparse.ArgumentParser(description="set up server") 
parser.add_argument('dowhat', choices=['all', 'none', 'installmongo', 'confmongo', 'prgs','copydbs','disks'])
#group = parser.add_mutually_exclusive_group()
parser.add_argument("-q", "--quite", action="store_true",help='cancel command output when posible')
parser.add_argument("-y", "--yes", action="store_true",help='autoanswer to prompts when posible')
parser.add_argument("-g", "--gce", action="store_true", default=True,help='is t')
#parser.add_argument("-cpmdbH", "--copymongodbs", action="store_true",default=False,help='copy databases host')

parser.add_argument("-a", "--all", action="store_true")
#parser.add_argument("x", type=int, help="the base")
#parser.add_argument("y", type=int, help="the exponent")
#args = parser.parse_args()
#answer = args.x**args.y
  

 
 
# 
 
class SetUpServer(object):   
    def __init__(self,prg_inst_path=None,instName="_myinst",verbose=1,interactive=False,autoSetUp=False,**kwargs):
        self.sys_info={} 
        self.sys_info['is_debian'] = platform.dist()[0]=='debian' 
        self.prg_inst_path= prg_inst_path
        self.instName=instName
        self.hostIpInternal=socket.gethostbyname(socket.gethostname())
        self.hostname=socket.gethostname()
        self.verbose=verbose
        self.interactive=interactive
        self.setUpRepositories()
        self.aptgetOptions="q" if self.verbose <=2  else ""
        self.aptgetOptions = self.aptgetOptions if self.interactive else self.aptgetOptions + "y"  
        if self.aptgetOptions:self.aptgetOptions="-"+ self.aptgetOptions 
        self.kwargs=kwargs
        self.history=[]
        if autoSetUp:self.setupAll() 
        # sudo pip install virtualenv 
     
    def python_packages_ver_check(self):
        self.cmdExec("sudo python -m pip freeze | cut -d = -f 1 | xargs -n 1 pip search | grep -B2 'LATEST:'")
    def appendToFile(self,filepath,a_str,prepend="\n",append="\n"): 
        with open(filepath, 'a') as fl: return fl.write(prepend + a_str + append)
    def setUpRepositories(self):
        ''' overide this in sub classes '''
        return NotImplemented
    def setupAll(self):
        ''' overide this in sub classes'''
        return NotImplemented
    def cmdExec(self,cmdStr,shell=False):
        cmd= cmdStr if shell else cmdStr.split() 
        try:
            res=subprocess.call(cmd,shell=shell)
            rt = [True,cmdStr,res]
        except Exception, e:
            rt = [False,cmdStr,str(e)]
        if self.verbose >1: print "%s\n%s\n" %("- - -"*20,str(rt))
        self.history.append(rt)
        return rt
    def showHistory(self):
        print "* " * 20,"server history"
        for r in self.history:print str(r)
        print "* " * 20
    def clearHistory(self):
        self.history=[]
    def installFromRepos(self,packagesStr,updateRepos=True):
        if updateRepos: self.cmdExec("apt-get update")  
        res=self.cmdExec("apt-get install %s %s" %(packagesStr,self.aptgetOptions) )
        return res
    def installFromPip(self,packagesStr):
        return  self.cmdExec("pip install %s" %(packagesStr))
    def isPythonPackageInstalled(self, package):
        try:
            import package 
        except ImportError:
            return True 
    def instFromPipGitHub(self,repository,package,branch):
        return  self.cmdExec("pip install git+https://github.com/%s/%s.git@s" %(repository,package,branch))    
    def setUpstartConf(self,serviceName,initStr,start=False):
        initStr=re.sub(r'^ *','',initStr, flags=re.MULTILINE) #trim blancs from start put \t for intentation
        try:
            with open("/etc/init/"+serviceName+".conf", 'w') as fl:  fl.write(initStr)
            self.history.append([True,'created upstart conf for service'+serviceName,0])
        except Exception, e:
            self.history.append([False,'failed to create upstart conf for service'+serviceName +' '+str(e),1])
        if start:self.cmdExec('sudo start ' + serviceName)
    def setInitdConf(self,serviceName,initStr,start=False ,startOnReboot=True):
        initStr=re.sub(r'^ *','',initStr, flags=re.MULTILINE) #trim blancs from start put \t for intentation
        try:
            with open("/etc/init.d/"+serviceName, 'w') as fl:  fl.write(initStr)
            self.cmdExec("chmod +x /etc/init.d/"+serviceName)
            self.history.append([True,'created init.d for service'+serviceName,0])
        except Exception, e:
            self.history.append([False,'failed to create init.d conf for service'+serviceName +' '+str(e),1])
        if start:self.cmdExec('sudo start ' + serviceName)
        if startOnReboot:self.cmdExec('sudo update-rc.d ' + serviceName +' start 30 2 3 4 5 . stop 70 0 1 6 .')
    
    def setPythonPath(self, PythonPathLst): 
        PythonPathLst=[self.prg_inst_path +i for i in PythonPathLst]
        for i in PythonPathLst: sys.path.append(i) #so it is imediatelly available  
        with open("/usr/lib/python2.7/dist-packages/"+self.instName+".pth", 'w') as fl:  fl.write("\n".join(PythonPathLst))  
 
class SetUpServerGCE(SetUpServer):    
    ''' GCEsetup
    '''
    def __init__(self,prg_inst_path=None,**kwargs):         
        super(SetUpServerGCE, self).__init__(prg_inst_path=prg_inst_path,**kwargs)
        self.hostIpExternal=socket.gethostbyname('metadata.google.internal')
        self.hostIpInternal=socket.gethostbyname(socket.gethostname())
        self.hasEphemeralDisk =  len(glob.glob('/dev/disk/by-id/*Ephemeral*')) > 1
        self.setEphemeralMountPoint() 
        self.hasPersistenDisk = len(glob.glob('/dev/disk/by-id/*-pers*')) > 0
        self.setPersistedMountPoint()
    def setEphemeralMountPoint(self,ephemeralMountPoint='/mnt/ephemeral_d01'):
        if  self.hasEphemeralDisk:
            self.ephemeralMountPoint=ephemeralMountPoint
        else:
            self.ephemeralMountPoint=None
        return  self.ephemeralMountPoint
    def setPersistedMountPoint(self,MountPoint='/mnt/pers_d01'):
        if  self.hasPersistenDisk:
            self.persistentMountPoint=MountPoint
        else:
            self.persistentMountPoint=None
        return  self.persistentMountPoint    
    def setupAll(self):
        super(SetUpServerGCE, self).setupAll()
        self.prepareDisks()
        self.setSwapFile()
        self.sethosts() 
    def setHost(self, ip, name):
        self.appendToFile("/etc/hosts", '193.92.180.166 milonhp') 
        
    def prepareDisks(self):
        print "preparing disks",glob.glob('/dev/disk/by-id/*-pers*')
        if self.hasEphemeralDisk:
            print "preparing-mounting Ephemeral disk"
            self.cmdExec("mkdir " +self.ephemeralMountPoint)
            self.cmdExec(' /usr/share/google/safe_format_and_mount -m "mkfs.ext4 -F" /dev/disk/by-id/google-ephemeral-disk-0 '+ self.ephemeralMountPoint ,shell=True)        
        if self.hasPersistenDisk:
            print "preparing-mounting persistent disk"
            self.cmdExec("mkdir " +self.persistentMountPoint)
            pdname=glob.glob('/dev/disk/by-id/*-pers-*')[0]
            self.cmdExec(' /usr/share/google/safe_format_and_mount -m "mkfs.ext4 -F" '+pdname+ ' '+ self.persistentMountPoint,shell=True) 
            automountStr="\n"+pdname+ ' '+self.persistentMountPoint+ " ext4 defaults 0 1" #persistent disks are not autmounted on rebout 
            with open("/etc/fstab", 'a') as fl: return fl.write(automountStr) 
           
 
 
def main():
    print 'command ',str(args) 
    if GL_SYS_INFO['is_GCE']: 
        print "google compute engine server"
        server=setUpMyGCEServer() 
    else: 
        print "Non google compute engine server"
        server=SetUpServer() 

    if args.dowhat=='all': server.setupAll() 
    elif args.dowhat=='installmongo':server.instMongodb()
    elif args.dowhat=='confmongo':server.confMongo()  
    elif args.dowhat=='prgs': server.setupMyPrgs()
    elif args.dowhat=='copydbs': server.copyMongoDatabases() 
    elif args.dowhat=='disks': server.prepareDisks()
    elif args.dowhat=='none':pass 
    return server.history
 
     
if __name__ == "__main__": 
    main() 
