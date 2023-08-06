#!/usr/bin/env python3
# CLI for grading a single submission from the zip file
import argparse
import json
import pathlib
import shutil
import tempfile
import zipfile

import pandas as pd

import gradescope_auto_py as gap


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(
        description='grades a single submission, displays results as table.'
                    '(see doc at: https://github.com/matthigger/gradescope_auto_py/)')
    parser.add_argument('-z', '--zip', dest='file_zip',
                        help='autograder zip file')
    parser.add_argument('-s', '--submit', dest='submit',
                        help='submitted file (or folder)')
    parser.add_argument('-j', '--json', dest='file_json', default=None,
                        help='filename to write json output (gradescope format)')
    parser.add_argument('-c', '--csv', dest='file_csv', default=None,
                        help='filename to write csv output')
    parser.add_argument('-q', '--quiet', dest='quiet', default=False,
                        help='silences output')
    args = parser.parse_args(*args, **kwargs)

    # setup autograder zip
    folder = pathlib.Path(tempfile.TemporaryDirectory().name)
    folder_src = folder / 'src'
    with zipfile.ZipFile(args.file_zip, 'r') as zip_ref:
        zip_ref.extractall(folder_src)

    # if submit is a single file, copy into its own folder
    folder_submit = pathlib.Path(args.submit)
    if not folder_submit.is_dir():
        # if an individual file is passed (rather than folder) move to tmp dir
        folder_submit = folder / 'submit'
        folder_submit.mkdir(parents=True)
        file_src = pathlib.Path(args.submit)
        shutil.copyfile(file_src, folder_submit / file_src.name)

    # grade
    grader_config = gap.GraderConfig.from_json(folder_src / 'config.json')
    grader = grader_config.grade(folder_submit=folder_submit,
                                 folder_source=folder_src)

    json_dict = grader.get_json()
    df = pd.DataFrame(json_dict['tests']).set_index('name')

    if not args.quiet:
        # print markdown table
        print(json_dict['output'])
        print(df.to_markdown())

    if args.file_csv is not None:
        # print csv file
        df.to_csv(args.file_csv)

    if args.file_json is not None:
        with open(args.file_json, 'w') as f:
            json.dump(json_dict, f, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()
