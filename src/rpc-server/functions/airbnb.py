from xmlrpc.client import Fault
import psycopg2
import csv
import os

from models.database import Database
from lxml import etree
from xml.sax.saxutils import escape


def index():
    database = Database()
    result = database.selectAll(
        "SELECT id, file_name, xml, created_on, updated_on FROM imported_documents WHERE deleted_on IS NULL")
    database.disconnect()
    return result


def delete(filename):
    database = Database()
    result = database.softdelete(
        "imported_documents", f"file_name LIKE '{filename}' AND deleted_on IS NULL")
    database.disconnect()

    if result == 0:
        raise Fault(1, f"Failed to delete document '{filename}'!")

    return True


def insert(filename, data):
    temp_csv = "_temp.csv"

    try:
        file = open(temp_csv, "wb")
        file.write(data.data)
        file.close()
    except OSError:
        raise Fault(1, "Server error!")

    try:
        file = open(temp_csv)

        parser = Parser()
        xml = parser.parse(file)

        database = Database()
    except (OSError, Exception) as _:
        os.remove(temp_csv)
        print(_)
        raise Fault(1, "Server error!")

    if not parser.validate(xml):
        file.close()
        os.remove(temp_csv)
        raise Fault(3, "Generated XML is not valid!")

    try:
        database.connect()
    except Exception as _:
        file.close()
        os.remove(temp_csv)
        raise Fault(2, "Failed to connect to database!")

    try:
        database.insert(
            "INSERT INTO public.imported_documents (file_name, xml) VALUES (%s, %s)", (filename, xml))
        return True
    except psycopg2.IntegrityError as _:
        raise Fault(3, "Filename already exists on database!")
    except psycopg2.Error as _:
        raise Fault(1, "Server error!")
    finally:
        database.disconnect()
        file.close()
        os.remove(temp_csv)


class Parser:
    def __init__(self):
        self.schema = etree.XMLSchema(etree.parse("./schemas/airbnb.xsd"))

    def parse(self, file):
        reader = csv.reader(file)

        neighbourAreas = self.uniqueAreas(file)

        string = '<?xml version="1.0" ?>\n<root>'

        # Neighbourhood Areas
        string += '\n<areas>\n'
        for index, group in enumerate(neighbourAreas):
            string += f"""\t<area id="{index}" name="{group}" />\n"""
        string += '</areas>'

        # Airbnbs
        string += '\n<airbnbs>'
        next(reader)
        for row in reader:
            for i, item in enumerate(row):
                row[i] = escape(item)
            string += self.toXML(row, neighbourAreas.index(row[5]))

        string += '\n</airbnbs>'
        string += '\n</root>'

        file.seek(0)
        return string

    def parseToFile(self, file, destination):
        xml_file = open(destination, "w")
        xml = self.parse(file)

        if self.validate(xml) == False:
            xml_file.close()
            return

        xml_file.write(xml)
        xml_file.close()

    def toXML(self, row, area):
        data = {
            "id": row[0],
            "name": row[1],
            "host": {
                "id": row[2],
                "name": row[4],
                "verified": row[3]
            },
            "address": {
                "house_number": "",
                "road": "",
                "neighbourhood": row[6],
                "area": area,
                "coordinates": {
                    "latitude": row[7],
                    "longitude": row[8]
                }
            }
        }

        return f"""\n\t<airbnb id="{data['id']}">
                            <name>{data['name']}</name>
                            <host id="{data['host']['id']}">
                                <name>{data['host']['name']}</name>
                                <verified>{data['host']['verified']}</verified>
                            </host>
                            <address>
                                <house_number>{data['address']['house_number']}</house_number>
                                <road>{data['address']['road']}</road>
                                <neighbourhood>{data['address']['neighbourhood']}</neighbourhood>
                                <area ref="{data['address']['area']}" />
                                <coordinates>
                                    <latitude>{data['address']['coordinates']['latitude']}</latitude>
                                    <longitude>{data['address']['coordinates']['longitude']}</longitude>
                                </coordinates>
                            </address>
                        </airbnb>"""

    def validate(self, xml: str):
        try:
            xml_doc = etree.fromstring(xml)
            result = self.schema.validate(xml_doc)
            return result
        except:
            return False

    def uniqueAreas(self, file):
        reader = csv.reader(file)

        array = []
        next(reader)
        for row in reader:
            area = escape(row[5])
            if area not in array:
                array.append(area)

        file.seek(0)
        return array
