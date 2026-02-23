# -*- coding: utf-8 -*-
import os
import glob
import json
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
from urllib.parse import quote, unquote
import sqlite3
import re

addon=xbmcaddon.Addon()
language=addon.getLocalizedString
path=xbmc.getInfoLabel('ListItem.Path')

def kodiJsonRequest(params):
	data=json.dumps(params)
	request=xbmc.executeJSONRPC(data)
	try:
		response=json.loads(request)
	except UnicodeDecodeError:
		response=json.loads(request.decode('utf-8', 'ignore'))
	try:
		if 'result' in response:
			return response['result']
		return None
	except KeyError:
		logger.warn("[%s] %s" % (params['method'], response['error']['message']))
		return None

def deleteThumbnails(path):
	textures13_path=os.path.join(xbmcvfs.translatePath('special://database/'), 'Textures13.db')
	textures13_connection=sqlite3.connect(textures13_path, timeout=5)
	textures13_cursor=textures13_connection.cursor()
	url="image://video@"+re.sub(r'%[0-9A-F]{2}', lambda m: m.group(0).lower(), quote(path, safe="!()")).replace("~", "%7e")+"%"
	path=path+"%"
	textures13_cursor.execute("SELECT cachedurl FROM texture WHERE url LIKE ? OR url LIKE ?", (path, url))
	thumbnails=textures13_cursor.fetchall()
	if thumbnails:
		thumbnails_path=xbmcvfs.translatePath('special://thumbnails/')
		for thumbnail in thumbnails:
			xbmc.log(u'Clean Remove thumbnail %s' % thumbnail[0], level=xbmc.LOGINFO)
			thumbnail=os.path.join(thumbnails_path, thumbnail[0])
			xbmcvfs.delete(thumbnail)

		# Remove from Textures13.db
		with textures13_connection:
			textures13_connection.execute("DELETE FROM texture WHERE url LIKE ? OR url LIKE ?", (path, url))
			textures13_connection.execute("DELETE FROM path WHERE url LIKE ? OR url LIKE ?", (path, url))
			textures13_connection.commit()
	else:
		xbmc.log(u'Clean Remove did not find any thumbnail FROM texture WHERE url LIKE %s OR url LIKE %s' % (path, url), level=xbmc.LOGERROR)
	textures13_connection.close()

def deleteDirectory(directory):
	# In file browser open the parent folder.
	if directory==xbmc.getInfoLabel('Container.FolderPath'):
		xbmc.executebuiltin("Action(Back)")

	deleteThumbnails(directory)
	xbmcvfs.rmdir(directory, force=True)
	xbmc.log(u'Clean Remove %s' % directory, level=xbmc.LOGINFO)

def deleteFiles(file_name):
	file_name=os.path.splitext(file_name)[0] # File name without extension.
	# Delete parent folder if it name same as file name.
	if os.path.basename(os.path.dirname(path))==file_name:
		deleteDirectory(path)
	else:
		# Remove files which names start same as video file name.
		files=os.path.join(path, file_name)
		deleteThumbnails(files)
		files=glob.escape(files)
		files=glob.glob(files+"*")
		if files:
			for file in files:
				xbmcvfs.delete(file)
				xbmc.log(u'Clean Remove %s' % file, level=xbmc.LOGINFO)

		# Remove empty folder.
		if addon.getSetting('remove_empty_folder')=="true":
			try:
				if len(os.listdir(path))==0:
					deleteDirectory(path)
			except FileNotFoundError:
				xbmcgui.Dialog().notification(heading="Folder does not exist!", message=path.replace(",",";"), icon=xbmcgui.NOTIFICATION_ERROR, time=10000)
				xbmc.log(u"Clean Remove ERROR: Folder %s does not exist!" % path, level=xbmc.LOGERROR)

def cleanRemove():
	global path
	if path=='favourites://':
		path=unquote(xbmc.getInfoLabel('ListItem.FileNameAndPath')).split('"')[1]
		favourite=kodiJsonRequest({"jsonrpc": "2.0", "method": "Files.GetFileDetails", "params": { "file": path, "media": "video"}, "id": 1 })
		# favourite is none unless file exist.
		if favourite:
			favourite=favourite.get("filedetails", {})
		else:
			xbmcgui.Dialog().notification(heading="File does not exist!", message=path.replace(",",";"), icon=xbmcgui.NOTIFICATION_ERROR, time=10000)
			xbmc.log(u"Clean Remove ERROR: File %s does not exist! " % path, level=xbmc.LOGFATAL)
			exit()

		file_name=os.path.basename(path)
		path=os.path.dirname(path)+os.sep
	else:
		file_name=xbmc.getInfoLabel('ListItem.FileName')
		favourite=None

	file_name_and_path=xbmc.getInfoLabel('ListItem.FileNameAndPath')

	if file_name:
		xbmc.log(u'Clean Remove deleting file: '+file_name, level=xbmc.LOGDEBUG)
		deleteFiles(file_name)
	elif file_name_and_path:
		path=file_name_and_path
		xbmc.log(u'Clean Remove deleting file name and path: '+path, level=xbmc.LOGDEBUG)
		deleteDirectory(path)
	else:
		xbmc.log(u'Clean Remove deleting path: '+path, level=xbmc.LOGDEBUG)
		deleteDirectory(path)

	if xbmc.getInfoLabel('Container.Content')=='files':
		if file_name:
			xbmc.executebuiltin('Notification('+xbmc.getInfoLabel('ListItem.Label').replace(",",";")+','+language(30005)+')')
		else:
			xbmc.executebuiltin('Notification('+os.path.basename(os.path.dirname(path)).replace(",",";")+','+language(30010)+')')
	else:
		if favourite:
			id=int(favourite["id"])
		else:
			id=int(xbmc.getInfoLabel('ListItem.DBID'))

		if id < 0: id=int(xbmc.getInfoLabel('ListItem.Top250'));
		if id > 0:
			if favourite:
				media_type=favourite["type"]
			else:
				media_type=xbmc.getInfoLabel('ListItem.DBTYPE')

			if media_type=='movie':
				kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMovie', 'params': {'movieid': int(id)}, 'id': 1})
				xbmc.executebuiltin('Notification('+xbmc.getInfoLabel('ListItem.Label').replace(",",";")+','+language(30002)+')')
				xbmc.log(u'Clean Remove movie from library '+xbmc.getInfoLabel('ListItem.Label'), level=xbmc.LOGINFO)
			elif media_type=='episode':
				kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveEpisode', 'params': {'episodeid': int(id)}, 'id': 1})
				xbmc.executebuiltin('Notification('+xbmc.getInfoLabel('ListItem.Label').replace(",",";")+','+language(30003)+')')
				xbmc.log(u'Clean Remove episode from library '+xbmc.getInfoLabel('ListItem.Label')., level=xbmc.LOGINFO)
			elif media_type=='musicvideo':
				kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveMusicVideo', 'params': {'musicvideoid': int(id)}, 'id': 1})
				xbmc.executebuiltin('Notification('+xbmc.getInfoLabel('ListItem.Label').replace(",",";")+','+language(30004)+')')
				xbmc.log(u'Clean Remove music video from library '+xbmc.getInfoLabel('ListItem.Label'), level=xbmc.LOGINFO)
			elif media_type=='tvshow':
				kodiJsonRequest({'jsonrpc': '2.0', 'method': 'VideoLibrary.RemoveTVShow', 'params': {'tvshowid': int(id)}, 'id': 1})
				xbmc.executebuiltin('Notification('+xbmc.getInfoLabel('ListItem.Label').replace(",",";")+','+language(30009)+')')
				xbmc.log(u'Clean Remove TV show from library '+xbmc.getInfoLabel('ListItem.Label'), level=xbmc.LOGINFO)

if addon.getSetting('confirm')=="true":
	if xbmcgui.Dialog().yesno(language(30006), xbmc.getInfoLabel('ListItem.Label')):
		cleanRemove()
else:
	cleanRemove()

xbmc.executebuiltin('Container.Refresh')
