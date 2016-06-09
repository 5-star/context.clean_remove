plugin.video.LR.clean_remove
----------------------------

A Kodi add-on to delete a movie or episode or video cleanly, without leaving behind orphan files.

I have been using this for quite a while without any problems, so I am sharing it for public use. USE IT AT YOUR OWN RISK.
It will work well only if you kept the default naming terminology and paths for fanart and subtitles. Please see below for more details.

WARNING!!!
Only use this addon if you have movie on separate folders, one movie per folder. When you delete one movie it will remove the movie from library and then delete the folder where the movie is, this way deleting all files related to that movie.
If you have all the movies in one single folder, deleting one movie will delete them all.

Deleting a tvshow episode will remove it from the library and then delete the episode file and related files withe the same 'root' name.
Example: Deleting an episode with a filename abc.mp4, will delete all files that start with 'abc' on the folder where the episode is.
This way it will delete abc.mp4, abc.nfo, abc-thumb.jpg and abc.srt.
If it was the last episode on the season and folder, it will delete the folder if it's empty.

Music Videos behaves just like the episodes, removing the music video from the library and then deleting the video file and any othr files with the same 'root' file name on the folder of the video.

For videos not in the library, it will just delete the video and related fanart and subtitles with the same 'root' name, just like the tvshow episodes.

Installation
------------

 - Download the add-on as a ZIP file from the top of this page
 - Open Kodi
 - Go to `System -> Settings -> Add-ons -> Install from zip file`
 - Restart Kodi and enjoy :)
 
Release history
---------------
  * 2016-06-10 v 1.0.1 Initial release
