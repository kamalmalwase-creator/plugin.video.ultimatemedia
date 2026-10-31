import sys
import urllib.parse
import urllib.request
import json
import xbmcgui
import xbmcplugin

HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]


def add_item(name, category):
    url = BASE_URL + "?" + urllib.parse.urlencode({"category": category})
    item = xbmcgui.ListItem(label=name)
    xbmcplugin.addDirectoryItem(HANDLE, url, item, True)


def main_menu():
    categories = [
        ("Movies", "movies"),
        ("Web Series", "series"),
        ("Live TV", "livetv"),
        ("Sports", "sports"),
        ("IPTV", "iptv"),
        ("Favorites", "favorites")
    ]

    for name, category in categories:
        add_item(name, category)

    xbmcplugin.endOfDirectory(HANDLE)


def load_movies():
    xbmcgui.Dialog().notification(
        "Ultimate Media Hub",
        "Loading free movies..."
    )

    query = urllib.parse.urlencode({
        "q": "mediatype:movies AND (collection:feature_films OR collection:classic_cartoons)",
        "fl[]": ["identifier", "title"],
        "rows": "30",
        "page": "1",
        "output": "json"
    }, doseq=True)

    url = "https://archive.org/advancedsearch.php?" + query

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "UltimateMediaHub/1.0"}
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        movies = data.get("response", {}).get("docs", [])

        if not movies:
            xbmcgui.Dialog().ok("Movies", "No movies found.")
            xbmcplugin.endOfDirectory(HANDLE)
            return

        for movie in movies:
            title = movie.get("title", "Unknown Movie")
            identifier = movie.get("identifier", "")

            if not identifier:
                continue

            movie_url = (
                "https://archive.org/details/"
                + urllib.parse.quote(identifier)
            )

            item = xbmcgui.ListItem(label=title)
            item.setInfo("video", {
                "title": title,
                "mediatype": "movie"
            })

            xbmcplugin.addDirectoryItem(
                HANDLE, movie_url, item, False
            )

        xbmcplugin.endOfDirectory(HANDLE)

    except Exception as error:
        xbmcgui.Dialog().ok(
            "Movies Error",
            str(error)
        )
        xbmcplugin.endOfDirectory(HANDLE)


def main():
    params = urllib.parse.parse_qs(
        urllib.parse.urlparse(sys.argv[2]).query
    )

    category = params.get("category", [None])[0]

    if category is None:
        main_menu()
    elif category == "movies":
        load_movies()
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
