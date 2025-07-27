# -*- coding: utf-8 -*-
import os
import glob
import sys
import json
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs

addon = xbmcaddon.Addon()
lang = addon.getLocalizedString
path=xbmc.getInfoLabel('ListItem.Path')
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

def deleteDir(dir):
	global path
	path = os.path.dirname(os.path.dirname(path))
	# In file browser open the parent folder.
	if dir==xbmc.getInfoLabel('Container.FolderPath'):
		xbmc.executebuiltin(f'Container.Update("{path}")')

	xbmcvfs.rmdir(dir, force=True)

def deleteFiles(video):
	global path
	filename = os.path.splitext(video)[0] # File name without extension.
	# Delete parent folder if it name same as file name.
	if os.path.basename(os.path.dirname(path)) == filename:
		deleteDir(path)
	else:
		# Remove files which names start same as video file name.
		pattern = os.path.join(path, filename + '*')
		files = glob.glob(pattern)
		for file in files:
			xbmcvfs.delete(file)

def dlt():
	video=xbmc.getInfoLabel('ListItem.FileName')
	if xbmcgui.Dialog().yesno(lang(30006),xbmc.getInfoLabel('ListItem.Label')):
		if xbmc.getInfoLabel('Container.Content')=='files':
			xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30005) + ')')
		else:
			id=int(xbmc.getInfoLabel('ListItem.DBID'))
			if id<0: id=int(xbmc.getInfoLabel('ListItem.Top250'));
			if id>0:
				dbtype = xbmc.getInfoLabel('ListItem.DBTYPE')
				if dbtype=='movie':
					kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMovie', 'params': {'movieid': int(id)}, 'id': 1})
					xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30002) + ')')
				elif dbtype=='episode':
					kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveEpisode', 'params': {'episodeid': int(id)}, 'id': 1})
					xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30003) + ')')
				elif dbtype=='musicvideo':
					kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMusicVideo', 'params': {'musicvideoid': int(id)}, 'id': 1})
					xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + lang(30004) + ')')

		if video!='':
			deleteFiles(video)
		else:
			deleteDir(xbmc.getInfoLabel('Container.ListItem.FileNameAndPath'))

		# Remove empty folder.
		if remove_empty == "true":
			if len(os.listdir(path))==0:
				deleteDir(path)

	xbmc.executebuiltin('Container.Refresh')

if __name__ == '__main__':
	dlt()
