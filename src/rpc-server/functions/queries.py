from models.database import Database
from lxml import etree

# TODO


def filterAirbnbBy(field, value):
    database = Database()

    results = database.selectAll(
        "SELECT xml FROM imported_documents WHERE deleted_on IS NULL")

    for doc in results:
        element = etree.fromstring(doc[0])

        for el in element.xpath(f"//airbnb[.//{field}]"):
            print(el)

    return True
