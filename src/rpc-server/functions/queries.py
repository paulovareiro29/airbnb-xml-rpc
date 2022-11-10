from models.database import Database

# TODO


def formatSimpleResult(result):
    array = []
    for row in result:
        filename = row[0]
        result = row[1][1:-1]
        array.append((filename, result))

    return array


def fetchAirbnbs():
    """Returns all the airbnbs"""
    database = Database()

    results = database.selectAll(
        "SELECT file_name,  (xpath('//airbnbs/airbnb/name/text()', xml)) as output FROM imported_documents WHERE deleted_on IS NULL")

    database.disconnect()
    return formatSimpleResult(results)


def fetchAreas():
    """Returns all the areas in each file"""
    database = Database()

    results = database.selectAll(
        "SELECT file_name, (xpath('//areas/area/@name', xml)) as output FROM imported_documents WHERE deleted_on IS NULL")

    database.disconnect()
    return formatSimpleResult(results)


def countAirbnbs():
    """Returns the number of airbnbs per file in database"""
    database = Database()

    results = database.selectAll(
        "SELECT file_name, (xpath('count(//airbnbs/airbnb)', xml)) as output FROM imported_documents WHERE deleted_on IS NULL")

    database.disconnect()
    return formatSimpleResult(results)


def fetchByArea(area):
    """Returns all the areas in each file"""
    database = Database()

    results = database.selectAll(
        f"SELECT file_name, (xpath('//airbnbs/airbnb[address/area[@ref=//areas/area[@name=\"{area}\"]/@id]]/name/text()', xml)) as output FROM imported_documents WHERE deleted_on IS NULL")

    database.disconnect()
    return formatSimpleResult(results)
