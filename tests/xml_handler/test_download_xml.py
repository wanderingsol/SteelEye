from xml_handler.download_xml import DownloadXml


def test_downloader(url, file_type, download_to):
    dwn = DownloadXml(url, file_type, download_to)
    expected_local_files = {
        '/Users/avinashrao/PycharmProjects/SteelEye/SteelEye/SteelEye/tests/tmp/DLTINS_20200108_03of03.zip',
        '/Users/avinashrao/PycharmProjects/SteelEye/SteelEye/SteelEye/tests/tmp/DLTINS_20200108_02of03.zip',
        '/Users/avinashrao/PycharmProjects/SteelEye/SteelEye/SteelEye/tests/tmp/DLTINS_20200108_01of03.zip'

    }

    actual_local_files = set(dwn.run())

    expected_files = {
        'DLTINS_20200108_03of03.zip': 'http://firds.esma.europa.eu/firds/DLTINS_20200108_03of03.zip',
        'DLTINS_20200108_02of03.zip': 'http://firds.esma.europa.eu/firds/DLTINS_20200108_02of03.zip',
        'DLTINS_20200108_01of03.zip': 'http://firds.esma.europa.eu/firds/DLTINS_20200108_01of03.zip'
    }
    assert expected_files == dwn.file_names, "Not all files downloaded"
    assert expected_local_files == actual_local_files, "Not all files stored"
