# -*- coding: utf-8 -*-
from xbmcgui import Window, WindowDialog
import xbmc, xbmcgui
import xbmcaddon
#python modules
import os, time, stat, re, copy
import statvfs

__author__     = "Senufo"
__scriptid__   = "service.diskfree"
__scriptname__ = "diskfree"

Addon          = xbmcaddon.Addon(__scriptid__)

__cwd__        = Addon.getAddonInfo('path')
__version__    = Addon.getAddonInfo('version')
__language__   = Addon.getLocalizedString

__profile__    = xbmc.translatePath(Addon.getAddonInfo('profile'))
__resource__   = xbmc.translatePath(os.path.join(__cwd__, 'resources',
                                                'lib'))
DEBUG_LOG = True
#Function Debug
def debug(msg):
    """
    print message if DEBUG_LOG == True
    """
    if DEBUG_LOG == True: print " [%s] : %s " % (__scriptid__, msg)


                                                 
#Position du texte
x = int(Addon.getSetting('x'))
y = int(Addon.getSetting('y'))
width = int(Addon.getSetting('width'))
height = int(Addon.getSetting('height'))
font = Addon.getSetting('font')
color = Addon.getSetting('color')
#ID de la fenetre HOME
WINDOW_HOME = 10000
#Variable pour statvfs
F_BSIZE   = 0           # Preferred file system block size
F_FRSIZE  = 1           # Fundamental file system block size
F_BLOCKS  = 2           # Total number of file system blocks (FRSIZE)
F_BFREE   = 3           # Total number of free blocks
F_BAVAIL  = 4           # Free blocks available to non-superuser
F_FILES   = 5           # Total number of file nodes
F_FFREE   = 6           # Total number of free file nodes
F_FAVAIL  = 7           # Free nodes available to non-superuser
F_FLAG    = 8           # Flags (see your local statvfs man page)
F_NAMEMAX = 9           # Maximum file name length

#sys.path.append (__resource__)
def freespace_disk(path):
    """
    freespace(path) -> integer
    Return the number of bytes available to the user on the file system
    pointed to by path.
    """
    try:
        s = os.statvfs(path)
        return s[F_BAVAIL] * long(s[F_BSIZE])
    except OSError, why:
        print('"%r: %s' % (path, why), DWARNING)
    return 0

def totalspace_disk(path):
    """
    totalspace(path) -> integer
    Return the number of total bytes available on the file system
    pointed to by path.
    """
    try:
        s = os.statvfs(path)
        return s[F_BLOCKS] * long(s[F_BSIZE])
    except OSError, why:
        print('"%r: %s' % (path, why), DWARNING)
    return 0

ImgBoxDisk = None
ImgBoxDisk = None
filename = xbmc.translatePath("special://profile/addon_data/service.diskfree/diskfree.png")
#filename = 'special://home/henri/.xbmc/scripts/test.png'
ImgBoxDiskId = None
ImgBoxDiskId = None
#start_time = time.time() 
start_time = 0 
re_added_control = False

#Recupère les arguments envoyés par le skin qui a lancé le script
for arg in sys.argv:

    param = str(arg).lower()
    debug("param = %s " % param)
    if 'disk=' in param:
        disk = param.replace('disk=', '')
#On récupère l'ID de la fenêtre de skin qui à lancer le script
okno = Window(xbmcgui.getCurrentWindowId())

#On recupere les parametres des disques
#time = time.time()
freespace = freespace_disk('/home/')
totalspace = totalspace_disk('/home')
diskfree = ('%iGB') % (((freespace / 1024) / 1024) / 1024)
freespace = (((freespace / 1024) / 1024) / 1024)
totalspace = (((totalspace / 1024) / 1024) / 1024)
percent = totalspace and (totalspace - freespace) * 1.0 / totalspace or 0.0
debug( "f = %s, t = %s Pou = %s " % (freespace,totalspace,percent))
okno.setProperty('DISK' , '%s Go' % freespace )
