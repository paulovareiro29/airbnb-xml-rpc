from lxml import etree
import urllib.request as request


def fetchCenterPoint(query):
    try:
        safeQuery = query.replace(' ', '+')
        with request.urlopen(f"https://nominatim.openstreetmap.org/search?q={safeQuery}&format=xml") as response:
            xml = etree.fromstring(response.read())

            lat = xml.xpath("/searchresults/place[1]/@lat")
            lon = xml.xpath("/searchresults/place[1]/@lon")

            return (lat[0], lon[0])
    except:
        return ("", "")
