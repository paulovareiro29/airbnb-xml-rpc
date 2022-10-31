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
        handler = open(temp_csv, "wb")
        handler.write(data.data)
        handler.close()
    except OSError:
        raise Fault(1, "Server error!")

    try:
        handler = open(temp_csv)

        parser = AirbnbParser()
        xml = parser.parse(handler)

        database = Database()
    except (OSError, Exception) as _:
        os.remove(temp_csv)
        raise Fault(1, "Server error!")

    try:
        database.connect()
    except Exception as _:
        handler.close()
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
        handler.close()
        os.remove(temp_csv)


class AirbnbParser:
    def __init__(self):
        self.temp = "_temp.csv"
        self.schema = etree.XMLSchema(etree.parse("./schemas/airbnb.xsd"))

    def parse(self, file):
        csv_file = csv.reader(file)

        string = '<?xml version="1.0" ?>\n<airbnbs>'
        for row in csv_file:
            ''' Verification to remove the first row with the headers '''
            if row[0] == "id":
                continue
            string += self.row_to_xml(row)

        string += '\n</airbnbs>'
        return string

    def parseToFile(self, file, destination):
        xml_file = open(destination, "w")
        xml = self.parse(file)

        if self.validate(xml) == False:
            xml_file.close()
            return

        xml_file.write(xml)
        xml_file.close()

    def row_to_xml(self, row):
        for i, item in enumerate(row):
            row[i] = escape(item)

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
                "city": "",
                "country": "",
                "coordinates": {
                    "latitude": row[7],
                    "longitude": row[8]
                }
            }

        }

        return f"""\n    <airbnb id="{data['id']}">
                            <name>{data['name']}</name>
                            <host id="{data['host']['id']}">
                                <name>{data['host']['name']}</name>
                                <verified>{data['host']['verified']}</verified>
                            </host>
                            <address>
                                <house_number>{data['address']['house_number']}</house_number>
                                <road>{data['address']['road']}</road>
                                <city>{data['address']['city']}</city>
                                <country>{data['address']['country']}</country>
                                <coordinates>
                                    <latitude>{data['address']['coordinates']['latitude']}</latitude>
                                    <longitude>{data['address']['coordinates']['longitude']}</longitude>
                                </coordinates>
                            </address>
                        </airbnb>"""

    def validate(self, xml: str):
        xml_doc = etree.fromstring(xml)
        result = self.schema.validate(xml_doc)
        return result
