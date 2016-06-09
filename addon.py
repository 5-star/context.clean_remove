import os
import glob
import sys
import json
import xbmc
import xbmcgui
import xbmcaddon

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


def trataMovie():
    for fl in glob.glob(path + "*.*"): os.remove(fl)
    try: os.rmdir(path)
    except: logger.warn('not empty, keep folder')
    kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMovie', 'params': {'movieid': int(id)}, 'id': 1})
    xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30002))

def trataEpisode():
    base = os.path.splitext(xbmc.getInfoLabel('ListItem.FileName'))[0]
    kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveEpisode', 'params': {'episodeid': int(id)}, 'id': 1})
    for fl in glob.glob(path + base + "*.*"): os.remove(fl)
    try: os.rmdir(path)
    except: logger.warn('not empty, keep folder')
    xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30003))

def trataMusicVideos():
    base = os.path.splitext(xbmc.getInfoLabel('ListItem.FileName'))[0]
    kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMusicVideo', 'params': {'musicvideoid': int(id)}, 'id': 1})
    for fl in glob.glob(path + base + "*.*"): os.remove(fl)
    try: os.rmdir(path)
    except: logger.warn('not empty, keep folder')
    xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30004))

def trataVideos():
    base = os.path.splitext(xbmc.getInfoLabel('ListItem.FileName'))[0]
    for fl in glob.glob(path + base + "*.*"): os.remove(fl)
    xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30005))

def trata():
    id=xbmc.getInfoLabel('ListItem.DBID')
    if id=='-1':
        id=xbmc.getInfoLabel('ListItem.title')
    path=xbmc.getInfoLabel('ListItem.Path').replace('smb:','')
    if xbmcgui.Dialog().yesno(lang(30006),xbmc.getInfoLabel('ListItem.Label')):
        if xbmc.getInfoLabel('Container.Content')=='movies': trataMovie()
        if xbmc.getInfoLabel('Container.Content')=='episodes': trataEpisode()
        if xbmc.getInfoLabel('Container.Content')=='musicvideos': trataMusicVideos()
        if xbmc.getInfoLabel('Container.Content')=='files': trataVideos()
 
if __name__ == '__main__':
    xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30005))
    if xbmc.getInfoLabel('ListItem.FileName')!="":
        trata()
