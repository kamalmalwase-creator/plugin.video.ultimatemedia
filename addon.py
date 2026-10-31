import sys
import urllib.parse
import xbmcgui
import xbmcplugin

HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

categories = [
    ("Movies", "movies"),
    ("Web Series", "series"),
    ("Live TV", "livetv"),
    ("Sports", "sports"),
    ("IPTV", "iptv"),
    ("Favorites", "favorites")
]

def add_item(name, category):
    url = BASE_URL + "?" + urllib.parse.urlencode({
        "category": category
    })

    item = xbmcgui.ListItem(label=name)

    xbmcplugin.addDirectoryItem(
        HANDLE, url, item, True
    )

def main_menu():
    for name, category in categories:
        add_item(name, category)

    xbmcplugin.endOfDirectory(HANDLE)

def main():
    params = urllib.parse.parse_qs(
        sys.argv[2][1:]
    )

    category = params.get("category", [None])[0]

    if category is None:
        main_menu()

    elif category == "iptv":
        from resources.lib import iptv
        iptv.load_playlist()

    else:
        xbmcgui.Dialog().ok(
            "Ultimate Media Hub",
            category.title() + " section is under development."
        )
        xbmcplugin.endOfDirectory(HANDLE)

main()
