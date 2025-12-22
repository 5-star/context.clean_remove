# -*- coding: utf-8 -*-
import os
import glob
import json
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
from urllib.parse import unquote

addon = xbmcaddon.Addon()
language = addon.getLocalizedString
path=xbmc.getInfoLabel('ListItem.Path')
remove_empty_folder = addon.getSetting('remove_empty_folder')
confirm = addon.getSetting('confirm')

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
	# In file browser open the parent folder.
	if dir==xbmc.getInfoLabel('Container.FolderPath'):
		xbmc.executebuiltin("Action(Back)")

	xbmcvfs.rmdir(dir, force=True)

def deleteFiles(video):
	global path
	filename = os.path.splitext(video)[0] # File name without extension.
	# Delete parent folder if it name same as file name.
	if os.path.basename(os.path.dirname(path)) == filename:
		deleteDir(path)
	else:
		# Remove files which names start same as video file name.
		pattern = os.path.join(path, glob.escape(filename) + '*')
		files = glob.glob(pattern)
		for file in files:
			xbmcvfs.delete(file)
		# Remove empty folder.
		if remove_empty_folder == "true":
			if len(os.listdir(path))==0:
				deleteDir(path)

def cleanRemove():
	global path
	database_data=None
	if path=='favourites://':
		path=unquote(xbmc.getInfoLabel('ListItem.FileNameAndPath')).split('"')[1]
		database_data=kodiJsonRequest({"jsonrpc": "2.0", "method": "Files.GetFileDetails", "params": { "file": path, "media": "video"}, "id": 1 })
		database_data=database_data.get("filedetails", {})
		video=os.path.basename(path)
		path=os.path.dirname(path) + os.sep
	else:
		video=xbmc.getInfoLabel('ListItem.FileName')

	if xbmc.getInfoLabel('Container.Content')=='files':
		xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + language(30005) + ')')
	else:
		if not database_data:
			id=int(xbmc.getInfoLabel('ListItem.DBID'))
		else:
			id=int(database_data["id"])

		if id<0: id=int(xbmc.getInfoLabel('ListItem.Top250'));
		if id>0:
			if not database_data:
				dbtype = xbmc.getInfoLabel('ListItem.DBTYPE')
			else:
				dbtype=database_data["type"]

			if dbtype=='movie':
				kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMovie', 'params': {'movieid': int(id)}, 'id': 1})
				xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + language(30002) + ')')
			elif dbtype=='episode':
				kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveEpisode', 'params': {'episodeid': int(id)}, 'id': 1})
				xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + language(30003) + ')')
			elif dbtype=='musicvideo':
				kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMusicVideo', 'params': {'musicvideoid': int(id)}, 'id': 1})
				xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + language(30004) + ')')

	if video!='':
		deleteFiles(video) 
	else:
		deleteDir(xbmc.getInfoLabel('Container.ListItem.FileNameAndPath'))

	xbmc.executebuiltin('Container.Refresh')

if confirm == "true":
	if xbmcgui.Dialog().yesno(language(30006), xbmc.getInfoLabel('ListItem.Label')):
		cleanRemove()
else:
	cleanRemove()
