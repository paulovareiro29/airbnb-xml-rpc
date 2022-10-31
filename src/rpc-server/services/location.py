from models.xpath import safeGetChildValue
from lxml import etree
import urllib.request as request


def fetchAddress(lat, lon):
    try:
        with request.urlopen(f"https://nominatim.openstreetmap.org/reverse?lat={row[7]}&lon={row[8]}") as response:
            xml = etree.fromstring(response.read())

            addressparts = xml.xpath("//addressparts")
            return {
                "house_number": safeGetChildValue(
                    addressparts[0], "house_number", ""),
                "road": safeGetChildValue(
                    addressparts[0], "road", ""),
                "city": safeGetChildValue(
                    addressparts[0], "city", ""),
                "contry": safeGetChildValue(
                    addressparts[0], "house_number", "")
            }

    except Exception as err:
        return None
