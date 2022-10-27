import csv
import os

from db.database import Database

from lxml import etree
from xml.sax.saxutils import escape


def import_airbnb_data(filename, data):
    temp_csv = "_temp.csv"

    try:
        handler = open(temp_csv, "wb")
        handler.write(data.data)
        handler.close()
    except OSError:
        return False

    try:
        handler = open(temp_csv)

        parser = AirbnbParser()
        xml = parser.parse(handler)

        database = Database()

        try:
            database.connect()

            database.insert(
                "INSERT INTO public.imported_documents (file_name, xml) VALUES (%s, %s)", (filename, xml))
            print("File imported to database!")

            database.disconnect()
            handler.close()
            os.remove(temp_csv)
            return True
        except Exception as error:
            print(f"Error importing file!: {error}")

            database.disconnect()
            handler.close()
            os.remove(temp_csv)
            return False

    except (OSError, Exception) as error:
        print(error)
        os.remove(temp_csv)
        return False


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

        return """\n    <airbnb id="%s">
        <name>%s</name>
        <host id="%s">
            <name>%s</name>
            <verified>%s</verified>
        </host>
        <location>
            <neighbourhood group="%s">%s</neighbourhood>
            <coordinates>
                <latitude>%s</latitude>
                <longitude>%s</longitude>
            </coordinates>
            <country>%s</country>
        </location>
    </airbnb>""" % (row[0], row[1], row[2], row[4], row[3], row[5], row[6], row[7], row[8], row[9])

    def validate(self, xml: str):
        xml_doc = etree.fromstring(xml)
        result = self.schema.validate(xml_doc)
        return result
