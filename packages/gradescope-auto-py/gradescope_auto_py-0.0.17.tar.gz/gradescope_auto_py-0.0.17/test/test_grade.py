import pathlib
import tempfile

import gradescope_auto_py as gap
from gradescope_auto_py.grade import main


def test_main():
    folder_hw0 = pathlib.Path(gap.__file__).parents[1] / 'test' / 'ex' / 'hw0'
    file_zip = folder_hw0 / 'hw0_auto.zip'
    submit = folder_hw0 / 'case_typical' / 'hw0_stud.py'

    file_json = pathlib.Path(tempfile.NamedTemporaryFile(suffix='.json').name)
    file_csv = pathlib.Path(tempfile.NamedTemporaryFile(suffix='.csv').name)

    # passing with single file
    main(f'-z {file_zip} -s {submit} -j {file_json} -c {file_csv}'.split())

    assert file_csv.exists()
    assert file_json.exists()
    file_csv.unlink()
    file_json.unlink()

    # passing with folder
    submit = folder_hw0 / 'case_typical'
    file_json = pathlib.Path(tempfile.NamedTemporaryFile(suffix='.json').name)
    file_csv = pathlib.Path(tempfile.NamedTemporaryFile(suffix='.csv').name)
    main(f'-z {file_zip} -s {submit} -j {file_json} -c {file_csv}'.split())

    assert file_csv.exists()
    assert file_json.exists()
    file_csv.unlink()
    file_json.unlink()
