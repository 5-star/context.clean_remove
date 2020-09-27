context.clean_remove
--------------------

A Kodi add-on to delete a movie or episode or video cleanly, without leaving behind orphan files.

The kodi "Remove from library" is a nice feature, but only deletes the movie being played. After I started using it, I noticed that I had to manually delete the fanart, the nfo and the subtitles. Or instead ending up with a disk full of unsused garbish.  
So I came upo with this clean remove, a library removal tool that removes the media and all related files.

I have been using this for quite a while without any problems, so I am sharing it for public use. USE IT AT YOUR OWN RISK.
It will work well only if you kept the default naming terminology and paths for fanart and subtitles. Please see below for more details.

WARNING!!!
Pay attention to the setting "Movies in separate folders". If this is true, when you delete one movie it will remove the movie from the library and then delete the folder where the movie is, this way deleting all files related to that movie.
If you have all the movies in one single folder and set the 'Movies in separate folders', deleting one movie will delete them all. Use this option only if you have movies on separate folders, one movie per folder. 

For all other media types (episodes, music videos and videos) this will only delete the fanart, nfo and subtitles related to the media being removed form the library. Everything else on the same folder is not touched.

Optionally, if it was the last episode on the season/folder, it will delete the folder if it's empty.

Files with the following extensions and the same name as the movie/episode are deleted:
".srt"
".pt.srt"
".en.srt"
".nfo"
".jpg"
"-poster.jpg"
"-fanart.jpg"
"-thumb.jpg"
"-banner.jpg"
"-thumb.jpg"

Installation
------------

 - Download the add-on as a ZIP file from the top of this page
 - Open Kodi
 - Go to `System -> Settings -> Add-ons -> Install from zip file`
 - Restart Kodi and enjoy :)
 
Release history
---------------
  * 6.0.0 Kodi 19
  * 1.0.2 Update to Kodi 18
  * 1.0.1 Initial release
