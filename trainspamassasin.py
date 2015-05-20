#!/usr/bin/env python 

import os
import re

path='/var/vmail'
defaultimapfolders=5
            
def scanvirtualdir (str ):
    print "going"
    for dirs in os.listdir(str):
        if (os.path.isdir(dirs)):
	    print dirs
            found = re.search ('((\w)+(\.)(\w)+)+',dirs)
            if (found != None):
                print "is a domain", dirs
                scandomaindir (path + "/" + dirs)
    return

def scandomaindir(domaindir):
    print '***********Scanning domain dir %s ***************' % domaindir
    for dirs in os.listdir(domaindir):
        #print "Scaning %s" %dirs
        if (os.path.isdir(domaindir +"/" +dirs)):
            scanusermailbox(domaindir +"/" +dirs)
    return

def scanusermailbox(mailboxdir):
    print "scanning mailbox %s" % mailboxdir
    if isamailfolder(mailboxdir):
        if countimapfolders(mailboxdir)>defaultimapfolders:
            processmailfolder(mailboxdir)
    return

def countimapfolders(folder):
    toret=0
    for path,dirs,files in os.walk(folder,True,None,False):
        for d in dirs:
            iscurfolder=re.search ('\cur$',d)
            if iscurfolder:
                toret=toret+1
    return toret

def isamailfolder(folder):
    toret= False
    if os.path.isdir(folder+"/"+"cur") and os.path.isdir(folder+"/"+"new"):
        toret=True
    return toret

def processmailfolder(folder):
    if isamailfolder(folder):
        spam=re.search ('\.Junk$',folder)
        launchsalearn(folder+"/"+"cur",spam)
        for dirs in os.listdir(folder):
            processmailfolder(folder+"/"+dirs)
    return

def launchsalearn(folder,spam):
    prefix=" --ham "
    if spam:
        prefix=" --spam "
    print "executing %s in %s" % (prefix, folder)
    os.system("/usr/bin/sa-learn"+ prefix+ folder)
    return


print "stating"
scanvirtualdir(path)
