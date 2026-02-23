context.clean_remove
--------------------

A Kodi add-on to delete a movie, tv show, episode or video file cleanly, without leaving behind orphan files.

The kodi "Remove from library" is a nice feature, but only deletes the movie being played. After I started using it, I noticed that I had to manually delete the fanart, the nfo, subtitles, .actors, .trailers etc. Or instead ending up with a disk full of unused garbish.
So I came up with this clean remove, a library removal tool that removes the media and all related files.

I have been using this for quite a while without any problems, so I am sharing it for public use. USE IT AT YOUR OWN RISK.
It will work well only if you kept the default naming terminology and paths for fanart and subtitles.

For media types such as movies, episodes, music videos, and videos, this will remove files whose names begin same as the media file. Other files or folders in the same directory will remain unaffected. But if folder name match the file name then deletes folder.

Kodi does not provide any API / builtin or JSON-RPC method to remove favourite item. Firstly use "Clean remove" context menu item to remove files / folders and library entries, then remove empty favourite item using kodi context menu item "Remove".

Installation
------------
 - Download the add-on as a ZIP file from the top of this page
 - Open Kodi
 - Go to `System -> Settings -> Add-ons -> Install from zip file`
 - Restart Kodi and enjoy :)
 
Release history
---------------
  * 7.5.0 Add delete Thumbnails.
  * 7.4.0 Add delete TV Shows.
  * 7.3.0 Add delete form favourites.
  * 7.2.0 Fix lithuanian translation. Add confirm setting.
  * 7.1.0 Fix open the parent folder. Fix delete empty folder.
  * 7.0.0 Fix. Add Lithuanian translation.
  * 6.0.0 Kodi 19
  * 1.0.2 Update to Kodi 18
  * 1.0.1 Initial release
