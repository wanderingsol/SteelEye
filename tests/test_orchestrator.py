import os
from orchestrator import Orchestrator


def test_orchestrate(url, start_tag, end_tag, file_type, download_to, sample_file_path):
    orch = Orchestrator(url, file_type, download_to, downloaded_files=[sample_file_path])
    orch.orchestrate(start_tag, end_tag)
    xml_path = sample_file_path.replace("zip", "xml")
    csv_path = sample_file_path.replace("zip", "csv")

    assert os.path.exists(xml_path), "Did not unzip the file!"
    assert os.path.exists(csv_path), "Did not extract data from file!"

    expected = {
        'BE0000348574', 'BE0000348574', 'BE0000348574', 'BE0000348574', 'BE0000348574', 'BE0000348574', 'BE0000348574',
        'BE0002466416', 'BE0002466416', 'BE0002592708', 'BE0002592708', 'BE0002638196'}

    actual = set()
    with open(csv_path, 'r') as fh:
        for line in fh.readlines():
            actual.add(line.split(",")[0])

    assert expected == actual, "Parser not run successfully, miss extracting values"
