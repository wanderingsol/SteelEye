import os
import pytest


def cleanup():
    base = os.path.join(os.path.dirname(__file__), "tmp")
    all_objects_path = [
        "sample.xml", "sample.csv", "DLTINS_20200108_03of03.zip", "DLTINS_20200108_02of03.zip",
        "DLTINS_20200108_01of03.zip"
    ]

    for ea in all_objects_path:
        obj_path = os.path.join(base, ea)
        if os.path.exists(obj_path):
            os.remove(obj_path)

def pytest_runtest_setup(item):
    cleanup()


def pytest_runtest_teardown(item):
    cleanup()


@pytest.fixture
def url():
    return "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2020-01-08T00:00:00Z+TO+2020-01-08T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"


@pytest.fixture
def file_type():
    return "DLTINS"


@pytest.fixture
def download_to():
    return os.path.join(os.path.dirname(__file__), "tmp")


@pytest.fixture
def start_tag():
    return "FinInstrmGnlAttrbts"


@pytest.fixture
def end_tag():
    return "Issr"


@pytest.fixture()
def sample_file_path():
    fp = os.path.join(os.path.dirname(__file__), "tmp", "sample.zip")
    return fp
