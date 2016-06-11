import os
import glob
import sys
import json
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import ctypes

addon = xbmcaddon.Addon()
lang = addon.getLocalizedString

def kodiJsonRequest(params):
    data = json.dumps(params)
    request = xbmc.executeJSONRPC(data)
    try:
        response = json.loads(request)
    except UnicodeDecodeError:
        response = json.loads(request.decode('utf-8', 'ignore'))
    try:
        if 'result' in response:
            return response['result']
        return None
    except KeyError:
        logger.warn("[%s] %s" % (params['method'], response['error']['message']))
        return None

def deleteFile(file):
    if xbmcvfs.exists(file):
        xbmcvfs.delete(file)

def deleteDir(dir):
    if xbmcvfs.exists(dir):
        files=xbmcvfs.listdir(dir)
        if len(files)==2:
            xbmcvfs.rmdir(dir)

def deleteVideo(path, video):
    deleteFile(path + video)
    filebase = path + os.path.splitext(video)[0]
    deleteFile(filebase + ".jpg")
    deleteFile(filebase + ".srt")
    deleteFile(filebase + ".nfo")
    deleteFile(filebase + "-poster.jpg")
    deleteFile(filebase + "-thumb.jpg")
    deleteDir(path)
			
def trataMovie(id, path, video):
    kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMovie', 'params': {'movieid': int(id)}, 'id': 1})
    for fl in xbmcvfs.listdir(path): xbmcvfs.remove(fl)
    deleteDir(path)
    xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30002) + ')')

def trataEpisode(id, path, video):
    kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveEpisode', 'params': {'episodeid': int(id)}, 'id': 1})
    deleteVideo(path, video)
    xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30003) + ')')

def trataMusicVideos(id, path, video):
    kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMusicVideo', 'params': {'musicvideoid': int(id)}, 'id': 1})
    deleteVideo(path, video)
    xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30004) + ')')

def trataVideos(path, video):
    deleteVideo(path, video)
    xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30005) + ')')

def trata():
    id=xbmc.getInfoLabel('ListItem.DBID')
    if id=='-1':
        id=xbmc.getInfoLabel('ListItem.title')
    if xbmcgui.Dialog().yesno(lang(30006),xbmc.getInfoLabel('ListItem.Label')):
        path=xbmc.getInfoLabel('ListItem.Path')
        video = xbmc.getInfoLabel('ListItem.FileName')
        if xbmc.getInfoLabel('Container.Content')=='movies': trataMovie(id, path, video)
        if xbmc.getInfoLabel('Container.Content')=='episodes': trataEpisode(id, path, video)
        if xbmc.getInfoLabel('Container.Content')=='musicvideos': trataMusicVideos(id, path, video)
        if xbmc.getInfoLabel('Container.Content')=='files': trataVideos(path, video)
 
if __name__ == '__main__':
    #ctypes.windll.user32.MessageBoxA(0, addon.getAddonInfo('path'), "Your title", 1)
    if xbmc.getInfoLabel('ListItem.FileName')!="":
        trata()