import os
import zipfile
from xml_handler.parser import Extractor
from xml_handler.download_xml import DownloadXml
from connectors.aws_connector import AWSConnector


class Orchestrator(object):
    def __init__(self, download_url, file_type, download_to, downloaded_files=None):
        self.download_to = download_to
        self.downloader = DownloadXml(download_url, file_type, download_to)
        self.all_data_files = []
        self.downloaded_files = downloaded_files
        self.aws_connector = AWSConnector()

    def unzip_file(self, file_path):
        with zipfile.ZipFile(file_path, 'r') as zipped:
            file_names = zipped.namelist()
            zipped.extractall(self.download_to)
        return [os.path.join(self.download_to, ea) for ea in file_names]

    @staticmethod
    def extracted_data_to_csv(start_tag, end_tag, data_file, cols=None):
        data = Extractor.extract_iteratively(start_tag, end_tag, data_file)
        csv_file_path = f"{data_file.split('.')[0]}.csv"
        with open(csv_file_path, 'w') as fh:
            if cols:
                fh.write(f"{cols}\n")
            for ea in data:
                row = ",".join(ea)
                fh.write("%s\n" % row.encode('ascii', 'ignore').decode('ascii'))
                # fh.write(f"{str(ea.encode('utf-8'))}\n")
        return csv_file_path

    def orchestrate(self, start_tag, end_tag, cols=None, upload=False):
        data_files = []
        csv_files = []
        cols = ",".join(cols) if cols else None
        downloaded_files = self.downloaded_files or self.downloader.run()
        for file_path in downloaded_files:
            data_files.extend(self.unzip_file(file_path))

        for data_file in data_files:
            csv_files.append(
                self.extracted_data_to_csv(start_tag, end_tag, data_file, cols=cols)
            )

        if upload:
            for ea in csv_files:
                self.upload_to_aws(ea)

    def upload_to_aws(self, file_path):
        self.aws_connector.upload_file_to_bucket(file_path)
