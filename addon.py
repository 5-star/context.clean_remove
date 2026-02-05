# -*- coding: utf-8 -*-
import os
import glob
import json
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
from urllib.parse import quote, unquote

addon = xbmcaddon.Addon()
language = addon.getLocalizedString
path=xbmc.getInfoLabel('ListItem.Path')

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

def deleteDirectory(directory):
	# In file browser open the parent folder.
	if directory == xbmc.getInfoLabel('Container.FolderPath'):
		xbmc.executebuiltin("Action(Back)")

	xbmcvfs.rmdir(directory, force=True)
	xbmc.log(u'Clean Remove deleted folder ' + directory, level = xbmc.LOGINFO)

def deleteFiles(file_name):
	file_name = os.path.splitext(file_name)[0] # File name without extension.
	# Delete parent folder if it name same as file name.
	if os.path.basename(os.path.dirname(path)) == file_name:
		deleteDirectory(path)
	else:
		# Remove files which names start same as video file name.
		pattern = os.path.join(path, glob.escape(file_name) + '*')
		files = glob.glob(pattern)
		for file in files:
			xbmcvfs.delete(file)
			xbmc.log(u'Clean Remove deleted file ' + file, level = xbmc.LOGINFO)

		# Remove empty folder.
		if addon.getSetting('remove_empty_folder') == "true":
			try:
				if len(os.listdir(path)) == 0:
					deleteDirectory(path)
			except FileNotFoundError:
				xbmc.log(u"Clean Remove ERROR: Folder %s' does not exist!" % path, level = xbmc.LOGERROR)

def cleanRemove():
	global path
	if path == 'favourites://':
		path = unquote(xbmc.getInfoLabel('ListItem.FileNameAndPath')).split('"')[1]
		favourite=kodiJsonRequest({"jsonrpc": "2.0", "method": "Files.GetFileDetails", "params": { "file": path, "media": "video"}, "id": 1 })
		# favourite is none unless file exist.
		if favourite:
			favourite=favourite.get("filedetails", {})
		else:
			xbmcgui.Dialog().notification(heading = "File does not exist!", message = path.replace(",",";"), icon = xbmcgui.NOTIFICATION_ERROR, time = 10000)
			xbmc.log(u'Clean Remove ERROR: File does not exist! ' + path, level = xbmc.LOGFATAL)
			exit()

		file_name = os.path.basename(path)
		path = os.path.dirname(path) + os.sep
	else:
		file_name = xbmc.getInfoLabel('ListItem.FileName')
		favourite = None

	file_name_and_path = xbmc.getInfoLabel('ListItem.FileNameAndPath')

	# Remove files or folder.
	if file_name:
		xbmc.log(u'Clean Remove deleting file ' + file_name, level = xbmc.LOGDEBUG)
		deleteFiles(file_name)
	elif file_name_and_path:
		path=file_name_and_path
		xbmc.log(u'Clean Remove deleting file name and path ' + path, level = xbmc.LOGDEBUG)
		deleteDirectory(path)
	else:
		xbmc.log(u'Clean Remove deleting path ' + path, level = xbmc.LOGDEBUG)
		deleteDirectory(path)

	# Remove from kodi library.
	if xbmc.getInfoLabel('Container.Content') == 'files':
		xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + language(30005) + ')')
	else:
		if favourite:
			id = int(favourite["id"])
		else:
			id = int(xbmc.getInfoLabel('ListItem.DBID'))

		if id < 0: id = int(xbmc.getInfoLabel('ListItem.Top250'));
		if id > 0:
			if favourite:
				media_type = favourite["type"]
			else:
				media_type = xbmc.getInfoLabel('ListItem.DBTYPE')

			if media_type == 'movie':
				kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMovie', 'params': {'movieid': int(id)}, 'id': 1})
				xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + language(30002) + ')')
				xbmc.log(u'Remove movie from library ' + xbmc.getInfoLabel('ListItem.Label').replace(",",";"), level = xbmc.LOGINFO)

			elif media_type == 'episode':
				tv_show_id = xbmc.getInfoLabel('ListItem.TVShowDBID')
				tvshow_details = kodiJsonRequest({ "jsonrpc": "2.0", "method": "VideoLibrary.GetTVShowDetails", "params": { "tvshowid": int(tv_show_id), "properties": ["episode"] }, "id": 1 })
				tvshow_details = tvshow_details.get("tvshowdetails", {})
				episodes_count = tvshow_details["episode"]
				tvshow_name = tvshow_details["label"]

				# With last episode in library remove TV Show.
				if addon.getSetting('remove_empty_folder') == "true" and episodes_count == 1:
					xbmc.executebuiltin("Action(Back)")
					# Deletes TV Show folder if only one episode is scraped.
					#deleteDirectory(path)
					kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveTVShow', 'params': {'tvshowid': int(tv_show_id)}, 'id': 1})
					xbmc.executebuiltin('Notification(' + tvshow_name.replace(",",";") + ',' + language(30009) + ')')
					xbmc.log(u'Remove TV show from library ' + tvshow_name.replace(",",";"), level = xbmc.LOGINFO)
				else:
					kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveEpisode', 'params': {'episodeid': int(id)}, 'id': 1})
					xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + language(30003) + ')')
					xbmc.log(u'Remove episode from library ' + xbmc.getInfoLabel('ListItem.Label').replace(",",";"), level = xbmc.LOGINFO)

			elif media_type=='musicvideo':
				kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMusicVideo', 'params': {'musicvideoid': int(id)}, 'id': 1})
				xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + language(30004) + ')')
				xbmc.log(u'Remove music video from library ' + xbmc.getInfoLabel('ListItem.Label').replace(",",";"), level = xbmc.LOGINFO)

			elif media_type=='tvshow':
				kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveTVShow', 'params': {'tvshowid': int(id)}, 'id': 1})
				xbmc.executebuiltin('Notification(' + xbmc.getInfoLabel('ListItem.Label').replace(",",";") + ',' + language(30009) + ')')
				xbmc.log(u'Remove TV show from library ' + xbmc.getInfoLabel('ListItem.Label').replace(",",";"), level = xbmc.LOGINFO)

if addon.getSetting('confirm') == "true":
	if xbmcgui.Dialog().yesno(language(30006), xbmc.getInfoLabel('ListItem.Label')):
		cleanRemove()
else:
	cleanRemove()

xbmc.executebuiltin('Container.Refresh')