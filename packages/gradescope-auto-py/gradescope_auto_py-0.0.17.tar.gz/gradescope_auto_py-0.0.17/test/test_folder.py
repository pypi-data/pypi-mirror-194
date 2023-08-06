from gradescope_auto_py.folder import *


def test_folder():
    file_str_dict = {'test.txt': 'contents of test.txt'}
    with to_temp_folder(file_str_dict=file_str_dict) as folder0:
        assert folder0.exists()
        assert (folder0 / 'test.txt').exists()
        with to_temp_folder(folder_src=folder0) as folder1:
            assert (folder1 / 'test.txt').exists()
        assert not folder1.exists()
    assert not folder0.exists()
