import sys
import urllib.parse
import xbmcgui
import xbmcplugin

HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

categories = [
("🎬 Movies", "movies"),
("📺 Web Series", "series"),
("📡 Live TV", "livetv"),
("⚽ Sports", "sports"),
("🌐 IPTV", "iptv"),
("⭐ Favorites", "favorites")
]

def add_item(name, category):
url = BASE_URL + "?" + urllib.parse.urlencode({
"category": category
})

item = xbmcgui.ListItem(label=name)

xbmcplugin.addDirectoryItem(
    handle=HANDLE,
    url=url,
    listitem=item,
    isFolder=True
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
else:
    xbmcgui.Dialog().ok(
        "Ultimate Media Hub",
        category.title() + " section selected. "
        "Authorized source will be configured next."
    )
    xbmcplugin.endOfDirectory(HANDLE)

main()
