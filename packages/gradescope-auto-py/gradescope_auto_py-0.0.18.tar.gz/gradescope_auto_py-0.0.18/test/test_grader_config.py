import hashlib
import pathlib
import tempfile

import gradescope_auto_py as gap
from gradescope_auto_py.grader_config import GraderConfig
from test_grader import json_assert_eq

ex_folder = pathlib.Path(gap.__file__).parents[1] / 'test' / 'ex'

grader_config_list = [GraderConfig.from_py(folder_local=ex_folder / 'hw0',
                                           file_afp='hw0.py',
                                           file_run='hw0_stud.py'),
                      GraderConfig.from_py(folder_local=ex_folder / 'hw1',
                                           file_afp_tup=('hw1.py', 'test.py'),
                                           file_submit_tup=('hw1.py',),
                                           file_supp_tup=('test.py',),
                                           file_run='test.py'),
                      GraderConfig.from_py(folder_local=ex_folder / 'hw2',
                                           file_afp='hw2.py',
                                           file_supp_tup=('nothing.py', ))]


def test_grade():
    """ grades every case in every hw, checks that results.json are valid """
    for grader_config in grader_config_list:
        folder = pathlib.Path(grader_config.folder_local)
        for case_folder in sorted(folder.glob('case*')):
            grader = grader_config.grade(folder_submit=case_folder,
                                         folder_source=folder)

            json_assert_eq(json_dict=grader.get_json(),
                           file_json_expected=case_folder / 'results.json')


def all_files_equal(file_tup):
    """ compares a tuple of files, True if all files are identical """
    # https://stackoverflow.com/questions/31027268/pythonfunction-that-compares-two-zip-files-one-located-in-ftp-dir-the-other
    hash_tup = tuple(hashlib.sha256(open(file, 'rb').read()).digest()
                     for file in file_tup)
    return all(hash_tup[0] == hash for hash in hash_tup[2:])


def test_grader_config():
    # test __init__ & from_py()
    hw0_folder = ex_folder / 'hw0'
    grader_config = GraderConfig.from_py(folder_local=hw0_folder,
                                         file_afp='hw0.py',
                                         file_run='hw0_stud.py')

    # test make_autograder()
    file_zip = tempfile.NamedTemporaryFile(suffix='auto.zip').name
    grader_config.build_autograder(file_zip=file_zip)
    assert all_files_equal(file_tup=(file_zip, hw0_folder / 'hw0_auto.zip'))

    # swaps install specific hw0_folder for 'hw0_folder' (makes json load /
    # save expectation standard across installations)
    grader_config.folder_local = pathlib.Path('hw0_folder_placeholder')

    # test from_json()
    file_config_json = hw0_folder / 'hw0_grader_config.json'
    grader_config_exp = GraderConfig.from_json(file_config_json)
    assert grader_config.__dict__ == grader_config_exp.__dict__

    # test to_json()
    file = tempfile.NamedTemporaryFile(suffix='.json').name
    grader_config.to_json(file=file)
    grader_config2 = GraderConfig.from_json(file=file)
    assert grader_config2.__dict__ == grader_config.__dict__
