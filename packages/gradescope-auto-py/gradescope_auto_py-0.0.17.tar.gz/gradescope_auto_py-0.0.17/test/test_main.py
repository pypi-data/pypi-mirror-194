import pathlib

import gradescope_auto_py as gap
from gradescope_auto_py.__main__ import main


def test_main():
    folder_hw0 = pathlib.Path(gap.__file__).parents[1] / 'test' / 'ex' / 'hw0'
    file_zip_out = pathlib.Path('tmp_hw0_auto.zip')

    # simple
    main(f'-c hw0.py -f {folder_hw0} -o {file_zip_out}'.split())

    # all options
    main(f'-c hw0.py -r hw0_stud.py -a hw0.py -f {folder_hw0} '
         f'-o {file_zip_out} -v hw0_stud.py'.split())

    file_zip_out.unlink()
