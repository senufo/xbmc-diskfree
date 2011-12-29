# -*- coding: utf-8 -*-
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

#Verifie que xbmc tourne
while (not xbmc.abortRequested):
    #Attente avant de  tester l'espace sur le disque
    #intervalle = int(float(Addon.getSetting('time')) * 60.0)
    intervalle = 60
    if start_time and (time.time() - start_time) < intervalle:
        time.sleep(.5)
        #SHOW_UPDATE     = Addon.getSetting('show_update') == "true"
        SHOW_UPDATE     = "true"
        if ImgBoxDisk:
            # optional show le temps qu'il reste avant la prochaine MAJ
            try:
                if SHOW_UPDATE:
                    up = int(intervalle) - (time.time() - start_time)
                    #locstr = Addon.getLocalizedString(615)  #Update in %i second
                    locstr = "Update in %i second"
                    #print "MSG up = %s " % msg
                    label = "%s[CR]" %  msg + locstr % up
                else: #Il faut rafraichir l'affichage
                    #print "MSG = %s " % msg
                    label = '%s' % msg
                #MsgBoxDisk.setLabel( msg )
                ImgBoxDisk.setImage(filename)
                #else: MsgBoxDisk.setLabel( '' )
            except Exception, e:
                print str(e)

        HomeNotVisible = xbmc.getCondVisibility( "!Window.IsVisible(10000)" )
        if HomeNotVisible:
            #oop! on est plus sur le home
            re_added_control = True
        elif re_added_control and not HomeNotVisible:
            #MsgBoxDisk = xbmcgui.ControlLabel( x, y, width, height, '', font, color )
            ImgBoxDisk = xbmcgui.ControlImage(x, y, width, height, filename)
            # add control label and set default label
            #homeWin.addControl( MsgBoxDisk )
            homeWin.addControl( ImgBoxDisk )
            # get control id
            #MsgBoxDiskId = MsgBoxDisk.getId()
            ImgBoxDiskId = ImgBoxDisk.getId()
            re_added_control = False
            # reload addon setting possible change
            Addon = xbmcaddon.Addon( __scriptid__ )

        # continue le while sans faire le reste
        continue

    homeWin = xbmcgui.Window(WINDOW_HOME)

    #xbmc.executebuiltin( "SetProperty(username,'eeee',10000)" )
    if ImgBoxDiskId:
        try: 
            #MsgBoxDisk = homeWin.getControl( MsgBoxDiskId )
            ImgBoxDisk = homeWin.getControl( ImgBoxDiskId )
        except: 
            #MsgBoxId = None
            ImgBoxId = None
    if ImgBoxDiskId is None:
        #MsgBoxDisk = xbmcgui.ControlLabel( x, y, width, height, '', font, color )
        ImgBoxDisk = xbmcgui.ControlImage( x, y+30, width, height, filename)
        #homeWin.addControl( MsgBoxDisk )
        homeWin.addControl( ImgBoxDisk )
        # get control id
        #MsgBoxDiskId = MsgBoxDisk.getId()
        ImgBoxDiskId = ImgBoxDisk.getId()
    locstr = Addon.getLocalizedString(616) #Mise a jour
    #MsgBoxDisk.setLabel( locstr % ' ' )
    #ImgBoxDisk.setImage(filename)

    #On vide le message
    msg = ''

    #On recupere les parametres des disques
    #time = time.time()
    freespace = freespace_disk('/home/')
    totalspace = totalspace_disk('/home')
    diskfree = ('%iGB') % (((freespace / 1024) / 1024) / 1024)
    freespace = (((freespace / 1024) / 1024) / 1024)
    totalspace = (((totalspace / 1024) / 1024) / 1024)
    percent = totalspace and (totalspace - freespace) * 1.0 / totalspace or 0.0
    print "f = %s, t = %s Pou = %s " % (freespace,totalspace,percent)
    msg = "f = %s, t = %s Pou = %s " % (freespace,totalspace,percent) 

    
    #initialise start time
    start_time = time.time()
    time.sleep( .5 )


