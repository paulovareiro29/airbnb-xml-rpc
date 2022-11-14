from models.database import Database


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


def fetchTypes():
    """Returns all the types in each file"""
    database = Database()

    results = database.selectAll(
        "SELECT file_name, (xpath('//types/type/@name', xml)) as output FROM imported_documents WHERE deleted_on IS NULL")

    database.disconnect()
    return formatSimpleResult(results)


def countAirbnbs():
    """Returns the number of airbnbs per file in database"""
    database = Database()

    results = database.selectAll(
        "SELECT file_name, (xpath('count(//airbnbs/airbnb)', xml)) as output FROM imported_documents WHERE deleted_on IS NULL")

    database.disconnect()
    return formatSimpleResult(results)


def countByArea(area):
    """Returns how many airbnbs exists by area in each file"""
    database = Database()

    results = database.selectAll(
        f"SELECT file_name, (xpath('count(//airbnbs/airbnb/address/area[@ref=/root/areas/area[@name=\"{area}\"]/@id])', xml)) as output FROM imported_documents WHERE deleted_on IS NULL")

    database.disconnect()
    return formatSimpleResult(results)


def countByType(type):
    """Returns how many airbnbs exists by type in each file"""
    database = Database()

    results = database.selectAll(
        f"SELECT file_name, (xpath('count(//airbnbs/airbnb/type[@ref=/root/types/type[@name=\"{type}\"]/@id])', xml)) as output FROM imported_documents WHERE deleted_on IS NULL")

    database.disconnect()
    return formatSimpleResult(results)


def fetchByPriceLowerThen(price):
    """Returns all the airbnbs which price is lower then"""
    database = Database()

    results = database.selectAll(
        f"SELECT file_name, (xpath('//airbnbs/airbnb[price < {price}]/name/text()', xml)) as output FROM imported_documents WHERE deleted_on IS NULL")

    database.disconnect()
    return formatSimpleResult(results)


def fetchByPriceHigherThen(price):
    """Returns all the airbnbs which price is higher then"""
    database = Database()

    results = database.selectAll(
        f"SELECT file_name, (xpath('//airbnbs/airbnb[price > {price}]/name/text()', xml)) as output FROM imported_documents WHERE deleted_on IS NULL")

    database.disconnect()
    return formatSimpleResult(results)
