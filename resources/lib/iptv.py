import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib.request
import sys

HANDLE = int(sys.argv[1])

def load_playlist():

    addon = xbmcaddon.Addon()
    playlist_url = addon.getSetting("m3u_url")

    if not playlist_url:
        xbmcgui.Dialog().ok(
            "Ultimate Media Hub",
            "Please add your M3U playlist URL in settings."
        )
        return

    try:
        response = urllib.request.urlopen(
            playlist_url, timeout=15
        )
        content = response.read().decode(
            "utf-8", errors="replace"
        )

        title = "Unknown Channel"

        for line in content.splitlines():

            line = line.strip()

            if line.startswith("#EXTINF"):
                title = line.split(",")[-1].strip()

            elif line and not line.startswith("#"):

                item = xbmcgui.ListItem(label=title)
                item.setPath(line)
                item.setProperty("IsPlayable", "true")

                xbmcplugin.addDirectoryItem(
                    HANDLE,
                    line,
                    item,
                    False
                )

        xbmcplugin.endOfDirectory(HANDLE)

    except Exception as error:
        xbmcgui.Dialog().ok(
            "Playlist Error",
            str(error)
        )
