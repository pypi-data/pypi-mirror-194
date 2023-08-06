import ast
import pathlib
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

from gradescope_auto_py.assert_for_pts import AssertForPoints, NoPointsInAssert


class Grader:
    """ runs a py (or ipynb) file through autograder & formats out (gradescope)

    Attributes:
        afp_pts_dict (dict): keys are files AssertForPoints, values are points
            earned.  If value is None, afp has not been run yet
        stdout (str): stdout from student submission
        stderr (str): stderr from student submission
        s_output_list (list): a list of strings to be shown with json output
    """

    def __init__(self, afp_list):
        # init each assert for points to zero
        self.afp_pts_dict = {afp: None for afp in afp_list}
        self.stdout = ''
        self.stderr = ''
        self.s_output_list = list()
        self._has_been_run = False

    def grade(self, file_run, overwrite=False):
        """ grades submission (gets attributes: afp_pass_dict, stdout & stderr)

        Args:
            file_run (str): student submission for assignment
            overwrite (bool): toggles whether files in folder of file_run will be
                overwritten when grading (defaults to making new temp folder)
        """
        assert not self._has_been_run, '.grade() called twice on single grader'

        file_run = pathlib.Path(file_run).resolve()
        assert file_run.exists(), 'file_run not found'

        if overwrite:
            folder = file_run.parent
        else:
            # copy folder to new location (we'll modify .py files within it,
            # original should be unchanged)
            folder = pathlib.Path(tempfile.TemporaryDirectory().name)
            shutil.copytree(file_run.parent, folder)
            file_run = folder / file_run.name

        # prepare submission file to run
        token = None
        for file in folder.glob('**/*.py'):
            _, token = self.prep_file(file=file, file_out=file, token=token)

        # run submission & store stdout & stderr
        result = subprocess.run([sys.executable, file_run],
                                cwd=file_run.parent,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        # record output from stdout and stderr & parse for which asserts pass
        self.stdout = result.stdout.decode('utf-8')
        self.stderr = result.stderr.decode('utf-8')

        # record status of all asserts run
        self.parse_output(token=token)

    def parse_output(self, token):
        """ finds which AssertForPoints passes (or not) from stdout

        Args:
            token (str): token which marks output of AssertforPoints in stdout
                (see prep_file())
        """
        for match in re.finditer(f'.*{token} (True|False)', self.stdout):
            # parse assert for points & passes
            line = match.group(0)
            afp_s, s_passes = line.split(token)

            # parse s_passes
            if 'True' in s_passes:
                passes = True
            elif 'False' in s_passes:
                passes = False

            # record outcome
            afp = AssertForPoints(s=afp_s)
            if afp in self.afp_pts_dict:
                # assert is configured
                if self.afp_pts_dict[afp] is None:
                    # first time assert has been seen
                    self.afp_pts_dict[afp] = passes * afp.pts
                else:
                    # second time assert has been seen
                    self.print(f'duplicated {afp.s} (using max)')
                    self.afp_pts_dict[afp] = \
                        max(self.afp_pts_dict[afp], passes * afp.pts)
            else:
                # assert not configured
                self.print(f'unexpected assert: {afp.s}')

    @classmethod
    def find_syntax_error(cls, file=None, file_list=None):
        """ returns first syntax error found, otherwise returns False

        Args:
            file (str): submitted file
            file_list (list): list of files

        Returns:
            error: None if no syntax error, otherwise returns first syntax
                error found
        """
        assert (file is None) != (file_list is None), \
            'file xor file_list required'

        if file_list is not None:
            # run find_syntax_error on every file
            for file in file_list:
                error = cls.find_syntax_error(file=file)
                if error is not None:
                    # syntax error found, return it
                    return error
            return None

        with open(file, 'r') as f:
            s_file = f.read()

        try:
            ast.parse(s_file)
            # no syntax errors found
            return None
        except SyntaxError as error:
            return error

    @classmethod
    def prep_file(cls, file, token=None, file_out=None):
        """ loads file, replaces each assert-for-points with print

        every assert-for-points printed output has format:

        AssertForPoints.s {token} passes

        where passes is either True or False.  parse_output() reads and records
        such outputs

        Args:
            file (path): a student's py file submission
            token (str): some uniquely identifiable (and not easily guessed)
                string.  used to identify which asserts passed when file is run
            file_out (str): if passed, the prepped file is written to file_out

        Returns:
            s_file_prep (str): string of new python file (prepped)
            token (str): token used
        """
        if token is None:
            token = secrets.token_urlsafe()

        afp_found = set()

        # AssertTransformer converts asserts to grader._assert
        # https://docs.python.org/3/library/ast.html#ast.NodeTransformer
        class AssertTransformer(ast.NodeTransformer):
            def visit_Assert(self, node):
                try:
                    # assert for points, initialize object
                    afp = AssertForPoints(ast_assert=node)
                except NoPointsInAssert:
                    # assert statement, but not for points, leave unchanged
                    return node

                # record which afp were already run (from submission)
                afp_found.add(afp)

                return afp.get_print_ast(token=token)

        # parse file, convert all asserts
        with open(file, 'r') as f:
            s_file = f.read()

        assert 'grader_self' not in s_file, "'grader_self' in submission"

        # replace each assert-for-points with a print statement
        node_root = ast.parse(s_file)
        AssertTransformer().visit(node_root)
        s_file_prep = ast.unparse(node_root)

        # write output to file
        if file_out is not None:
            with open(file_out, 'w') as f:
                print(s_file_prep, file=f, end='')

        return s_file_prep, token

    def print(self, s):
        """ string will be shown in json output in gradescope interface

        Args
            s (str): string to output
        """
        self.s_output_list.append(s)

    def get_json(self):
        """ gets json in gradescope format

        https://gradescope-autograders.readthedocs.io/en/latest/specs/#output-format
        """
        s_output = '\n'.join(self.s_output_list + [self.stderr])

        # init json
        test_list = list()
        json_dict = {'tests': test_list,
                     'output': s_output}

        for afp, pts in self.afp_pts_dict.items():
            if pts is None:
                # test case never run
                msg = f'assert never run'
                _json_dict = afp.get_json_dict(output=msg,
                                               status='failed',
                                               score=0)
            else:
                _json_dict = afp.get_json_dict(score=pts)
            test_list.append(_json_dict)

        return json_dict
