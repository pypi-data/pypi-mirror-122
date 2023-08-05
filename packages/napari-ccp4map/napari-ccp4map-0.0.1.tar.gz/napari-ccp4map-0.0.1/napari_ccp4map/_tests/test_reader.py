from napari_ccp4map import napari_get_reader
from pathlib import Path

def test_get_reader_pass():
    reader = napari_get_reader("fake.file")
    assert reader is None
