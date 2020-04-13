import os
from connectors.url_connector import UrlConnector
from xml_handler.parser import Extractor, FileNameExtractor


class DownloadXml(object):
    def __init__(self, url, file_type, download_to):
        self._connector = UrlConnector(url)
        self.extractor = Extractor(FileNameExtractor, file_type)
        self.content = None
        self.file_names = {}
        self.download_to = download_to

    def get_content(self):
        self.content = self._connector.get_url_text()

    def get_file_names_from_content(self):
        file_names = self.extractor.extract_from_string(self.content)
        for ea in file_names:
            name = ea.split("/")[-1]
            self.file_names[name] = ea

    def download_data(self):
        _files = []
        for file_name, url in self.file_names.items():
            if self._connector.is_downloadable(url):
                download_path = os.path.join(self.download_to, file_name)
                with open(download_path, 'wb') as fh:
                    for chunk in self._connector.download_data(url, chunk_size=8192):
                        fh.write(chunk)
                _files.append(download_path)
        return _files

    def run(self):
        self.get_content()
        self.get_file_names_from_content()
        return self.download_data()
