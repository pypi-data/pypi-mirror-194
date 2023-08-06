import json
import pathlib
import shutil
import subprocess
from copy import deepcopy

from .assert_for_pts import AssertForPoints
from .folder import to_temp_folder
from .grader import Grader
from .gradescope import file_run_auto, file_setup_sh


class GraderConfig:
    """ builds autograder zip, prepares files

    Attributes:
        afp_list (dict): keys are file names values are list of
            AssertForPoints
        file_run (str): file to run for autograding (often student submitted
            version of assignment).  If None, then unique submitted py file
            used
        file_supp_tup (tuple): supplementary files to be included in the
            autograder and copied adjacent to student submission
        folder_local (pathlib.Path): root folder of all supplementary files.
            the supplementary file path, as stored in the tuple, is replicated
            in gradescope's submitted folder
        file_submit_tup (tuple): files which must be submitted for the
            autograder to run
        s_requirements (str): contents of a requirements.txt file, necessary
            to run autograder
    """

    @classmethod
    def from_py(cls, file_afp=None, file_afp_tup=None, file_supp_tup=tuple(),
                folder_local=None, **kwargs):
        """ builds configuration from a template assignment

        Args:
            file_afp (str): a single .py file containing assert for points (
                either this xor file_afp_tup required)
            file_afp_tup (tuple):  see Attributes above
            file_supp_tup (tuple):  see Attributes above
            folder_local (str): see Attributes above

        Returns:
            grader_config (GraderConfig):
        """
        file_supp_tup = tuple(file_supp_tup)

        # handle file_afp vs file_afp_tup
        assert (file_afp is None) != (file_afp_tup is None), \
            'either file_afp xor file_afp_tup required'
        if file_afp_tup is None:
            file_afp_tup = file_afp,
        else:
            file_afp_tup = tuple(file_afp_tup)

        # default folder local
        if folder_local is None:
            folder_local = '.'
        folder_local = pathlib.Path(folder_local)

        # build file_afp_dict
        afp_list = list()
        for file in file_afp_tup:
            # get list of afp in this file
            file_local = folder_local / file
            afp_list += list(AssertForPoints.iter_assert_for_pts(file_local))

        assert len(afp_list) == len(set(afp_list)), \
            'non-unique assert-for-points detected'

        # get list of required modules to run autograder
        file_tup = tuple(folder_local / file
                         for file in file_supp_tup + file_afp_tup)
        with to_temp_folder(file_tup) as folder:
            # build requirements.txt
            process = subprocess.run(['pipreqs', folder])
            assert process.returncode == 0, 'problem building requirements.txt'

            # read in s_requirements
            file_require = folder / 'requirements.txt'
            with open(file_require, 'r') as f:
                s_requirements = f.read()

        return GraderConfig(afp_list=afp_list,
                            file_supp_tup=file_supp_tup,
                            s_requirements=s_requirements,
                            folder_local=folder_local, **kwargs)

    def __init__(self, afp_list, file_run=None, file_supp_tup=tuple(),
                 file_submit_tup=tuple(), s_requirements=None,
                 folder_local='.'):
        self.file_run = file_run
        if self.file_run is not None:
            self.file_run = str(self.file_run)
        self.afp_list = afp_list
        self.file_supp_tup = tuple(str(file) for file in file_supp_tup)
        self.file_submit_tup = tuple(str(file) for file in file_submit_tup)
        self.s_requirements = s_requirements
        self.folder_local = pathlib.Path(folder_local)

    def build_autograder(self, file_zip='auto.zip'):
        """ builds a gradescope autograder zip

        Args:
            file_zip (str): name of zip to create

        Returns:
            file_zip_out (pathlib.Path): zip file created
        """
        file_tup = (file_setup_sh, file_run_auto) + self.file_supp_tup
        folder = pathlib.Path(self.folder_local)
        file_tup = tuple(folder / file for file in file_tup)

        # ensure no syntax errors in autograder files
        py_file_tup = tuple(file for file in file_tup if file.suffix == '.py')
        error = Grader.find_syntax_error(file_list=py_file_tup)
        if error is not None:
            s = 'Syntax error found:'
            s = '\n'.join([s, str(error), error.text])
            raise AssertionError(s)

        file_str_dict = {'requirements.txt': self.s_requirements}
        with to_temp_folder(file_tup=file_tup,
                            file_str_dict=file_str_dict) as folder:
            # build config.json in folder
            self.to_json(folder / 'config.json')

            # zip it up
            file_zip = pathlib.Path(file_zip)
            shutil.make_archive(file_zip.with_suffix(''), 'zip', folder)

        return file_zip

    def grade(self, folder_submit='submission', folder_source='source'):
        """ preps & validates files, returns a grader ready to output json

        Args:
             folder_submit (str): submission folder
             folder_source (str): source folder (contains unzipped autograder,
                see build_autograder() for detail)

        Returns:
            grader (Grader): a grader object which has been run on submission
        """
        folder_submit = pathlib.Path(folder_submit)
        folder_source = pathlib.Path(folder_source)

        # initialize grader
        grader = Grader(afp_list=self.afp_list)

        # check if syntax error found in any py file in submission folder
        file_list = list(folder_submit.rglob('*.py'))
        error = Grader.find_syntax_error(file_list=file_list)

        if error:
            # print message about syntax error
            s = 'Syntax error found (no points awarded by autograder):'
            s = '\n'.join([s, str(error), error.text])
            grader.print(s)
            return grader

        for file in self.file_submit_tup:
            # ensure student has submitted files properly
            file = folder_submit / file
            if not file.exists():
                grader.print('grading stopped, resubmit with required file: '
                             f'{file.name}')
                return grader

        with to_temp_folder(folder_src=folder_submit) as _folder_submit:
            # copy supplement files into submit
            for file in self.file_supp_tup:
                file_src = folder_source / file
                file_dst = _folder_submit / file

                if file_dst.exists():
                    # student submitted file has same name as supplemental file
                    grader.print('grading stopped, submission conflicts with '
                                 f'supplemental file: {file}')
                    return grader

                shutil.copy(file_src, file_dst)

            # get file to run
            file_run = self.get_file_run(_folder_submit,
                                         print_fnc=grader.print)
            if file_run is None:
                return grader

            # run autograder
            grader.grade(file_run=file_run, overwrite=True)

        return grader

    def get_file_run(self, folder_submit, print_fnc=None):
        """ gets file to run, attempts from config, else uses unique py

        Args:
            folder_submit (Path): submission folder
            print_fnc (fnc): accepts a string, will be shown to student

        Returns:
            file_run (Path): .py file to run
        """
        if print_fnc is None:
            print_fnc = print

        if self.file_run is None:
            # file run is unique .py file submitted
            set_py = set(folder_submit.glob('*.py'))

            # file run can not be supplemental (if desired, specify explicitly)
            set_py -= set(folder_submit / file for file in self.file_supp_tup)

            if len(set_py) == 1:
                # unique file found
                return set_py.pop()
            else:
                # no unique .py file submitted
                print_fnc(f'invalid submission, no unique .py given')
                return None

        # a particular file is expected
        file_run = folder_submit / self.file_run
        if file_run.exists():
            # expected file_run found
            return file_run
        else:
            # expected file_run not found
            print_fnc(f'file to be run not found: {self.file_run}')
            return None

    def to_json(self, file):
        """ writes config to txt file (string of each assert on each line)

        Args:
            file (str): file to write configuration to
        """
        d = deepcopy(self.__dict__)
        # afps are serialized as strings, we rebuild them as afp objects
        d['afp_list'] = [afp.s for afp in d['afp_list']]

        # Path not serializable
        d['folder_local'] = str(d['folder_local'])

        with open(file, 'w') as f:
            json.dump(d, f, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, file):
        """ reads GraderConfig from txt file

        Args:
            file (str): file to write configuration to
        """
        # load json
        with open(file) as f:
            d = json.load(f)

        # afps are serialized as strings, we rebuild them as afp objects
        d['afp_list'] = [AssertForPoints(s=s) for s in d['afp_list']]

        # path not serializable
        if 'folder_local' in d:
            d['folder_local'] = pathlib.Path(d['folder_local'])

        return GraderConfig(**d)
