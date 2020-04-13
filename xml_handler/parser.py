from lxml import etree


class DataExtractor(object):
    def __init__(self, start_tag, end_tag):
        self.text = []
        self.row = list()
        self.store = False
        self.start_tag = start_tag
        self.end_tag = end_tag

    def start(self, tag, attrib):
        if self.start_tag in tag:
            self.store = True

    def end(self, tag):
        if tag.strip().endswith(self.end_tag):
            self.store = False
            self.text.append(",".join(self.row))
            self.row = list()

    def data(self, data):
        if self.store:
            self.row.append(data)

    def close(self):
        return self.text


class FileNameExtractor(object):
    def __init__(self, file_type):
        self.links = set()
        self.store_link = False
        self.store_file_type = False
        self.file_type = None
        self.download_link = None
        self.search_file_type = file_type

    def start(self, tag, attrib):
        self.store_link = attrib.get('name') == 'download_link'
        self.store_file_type = attrib.get('name') == 'file_type'

    def end(self, tag):
        if tag.strip() == 'doc':
            if self.file_type == self.search_file_type and self.download_link:
                self.links.add(self.download_link)

    def data(self, data):
        if data.strip() and self.store_link:
            self.download_link = data.strip()

        if data.strip() and self.store_file_type:
            self.file_type = data.strip()

    def close(self):
        return self.links


class Extractor(object):
    def __init__(self, parser_class, *parser_args):
        self.parser_class = parser_class(*parser_args)
        self.parser = etree.XMLParser(target=self.parser_class)

    def extract_from_string(self, data_string):
        return etree.XML(data_string, self.parser)

    def extract_from_io(self, io_object):
        pass

    def extract_from_file(self, file_path):
        return etree.parse(file_path, self.parser)

    @classmethod
    def extract_iteratively(cls, start_tag, end_tag, file_path):
        data = []
        row = []

        context = etree.iterparse(file_path, events=('start',))
        store = False
        for event, elem in context:
            if elem.tag.endswith(start_tag):
                store = True

            if elem.text and store:
                row.append(elem.text)

            if elem.tag.endswith(end_tag):
                if row:
                    data.append(row)
                row = []
                store = False
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        del context
        return data


# [print(ea) for ea in Extractor.extract_iteratively("FinInstrmGnlAttrbts", "Issr", '/Users/avinashrao/Downloads/DLTINS_20200108_01of03.xml')]

