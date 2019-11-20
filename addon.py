# -*- coding: utf-8 -*-
import os
import glob
import sys
import json
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import re

addon = xbmcaddon.Addon()
lang = addon.getLocalizedString

separate_movies = addon.getSetting('separate_movies')
remove_empty = addon.getSetting('remove_empty')

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
        filename = os.path.splitext(video)[0]
	filebase = path + filename
        xdir, xfil = xbmcvfs.listdir(path)
        for fl in xfil:
            if re.fullmatch(re.escape(filename) + "[a-z]{2}\.srt", fl):
	        xbmcvfs.delete(path + fl)
	deleteFile(filebase + ".srt")
	deleteFile(filebase + ".nfo")
	deleteFile(filebase + ".jpg")
	deleteFile(filebase + "-poster.jpg")
	deleteFile(filebase + "-fanart.jpg")
	deleteFile(filebase + "-thumb.jpg")
	deleteFile(filebase + "-banner.jpg")
	deleteFile(filebase + "-thumb.jpg")
	if remove_empty == "true":
		deleteDir(path)
			
def dltMovie(id, path, video):
	kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMovie', 'params': {'movieid': int(id)}, 'id': 1})
	if separate_movies == "true":
		xdir, xfil = xbmcvfs.listdir(path)
		for fl in xfil:
			xbmcvfs.delete(path + fl)
		deleteDir(path)
	else:
		deleteVideo(path, video)
	xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30002) + ')')

def dltEpisode(id, path, video):
	kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveEpisode', 'params': {'episodeid': int(id)}, 'id': 1})
	deleteVideo(path, video)
	xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30003) + ')')

def dltMusicVideos(id, path, video):
	kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMusicVideo', 'params': {'musicvideoid': int(id)}, 'id': 1})
	deleteVideo(path, video)
	xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30004) + ')')

def dltVideos(path, video):
	deleteVideo(path, video)
	xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30005) + ')')

def dlt():
	if xbmcgui.Dialog().yesno(lang(30006),xbmc.getInfoLabel('ListItem.Label')):
		path=xbmc.getInfoLabel('ListItem.Path')
		video = xbmc.getInfoLabel('ListItem.FileName')
		if xbmc.getInfoLabel('Container.Content')=='files':
			dltVideos(path, video)
		else:
			id=int(xbmc.getInfoLabel('ListItem.DBID'))
			if id<0: id=int(xbmc.getInfoLabel('ListItem.Top250'));
			if id>0:
				dbtype = xbmc.getInfoLabel('ListItem.DBTYPE')
				if dbtype=='movie': dltMovie(id, path, video)
				elif dbtype=='episode': dltEpisode(id, path, video)
				elif dbtype=='musicvideo': dltMusicVideos(id, path, video)
 
if __name__ == '__main__':
	dlt()
