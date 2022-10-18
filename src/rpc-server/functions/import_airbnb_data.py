import csv
import os


def import_airbnb_data(file):
    temp_csv = "_temp.csv"

    try:
        handler = open(temp_csv, "wb")
        handler.write(file.data)
        handler.close()
    except OSError:
        return False

    try:
        handler = open(temp_csv)

        parser = AirbnbParser()
        parser.parseToFile(handler, "airbnb.xml")

        handler.close()
        os.remove(temp_csv)

    except OSError:
        os.remove(temp_csv)
        return False

    return True


class AirbnbParser:
    def __init__(self):
        self.temp = "_temp.csv"

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
        xml_file.write(self.parse(file))
        xml_file.close()

    def row_to_xml(self, row):
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
