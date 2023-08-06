# Gradescope Autograder for Python

## Installation

    $ pip install gradescope_auto_py

## Quick-start

1. Define an Assert-For-Points by adding a point value to any `assert` statements in a template copy of the assignment (e.g. [hw2.py](test/ex/hw2/hw2.py))

```python
assert get_area(radius=1) == pi, 'case0: area from r=1 (2 pts)'
```

2. Build an autograder in [gradescope's autograder format](https://gradescope-autograders.readthedocs.io/en/latest/specs/) by processing `hw2.py`:

```
$ python3 -m gradescope_auto_py -c hw2.py
```

(there are further options to this interface, run the command with `-h` to see their documentation)

3. Upload the `.zip` file generated to a gradescope "programming assignment".  Student submissions will be automatically graded upon submission.

## Running autograder locally

You can run the autograder locally to validate that it works as intended:

```
$ python3 -m gradescope_auto_py.grade -z auto.zip -s hw2.py
```

(there are further options to this interface, run the command with `-h` to see their documentation)

## Examples

See our [examples](test/ex) to observe autograder nuances (handling of student syntax / runtime errors, missing files, assert-for-points modified in student submission etc.)

## Notes
- You can control when a student sees output of every assert-for-points by
  specifying [a visibility setting](https://gradescope-autograders.readthedocs.io/en/latest/specs/#controlling-test-case-visibility)
  in the assert message:

```python
assert get_area(radius=1) == pi, 'case0: area from r=1 (2 pts after_due_date)'
```

- We automatically identify the modules to be installed on gradescope's interpreter via the template of assignment. Student submissions which import a module outside of these cannot be autograded (
  see [#4](https://github.com/matthigger/gradescope_auto_py/issues/4)), though you can add a few "extra" imports to ensure they're included (if known a priori).

## Advanced Usage
Our motivation is to make it as simple as possible go from an assignment solution to an autograder zip file.  You need only write the assert statements in the file, clarifying point values for each, and run the command above.

One of the drawbacks is that only the student's submitted code is run in the autograder:
- if a student modifies any test case or test case setup, they'll fail the test cases
- an instructor may not really "hide" any asserts from the students, regardless the gradescope visibility setting, so long as these commands must be in included in the student's submission
To avoid these issues, the hw1 [example](test/ex) is helpful.  Here, the instructor writes test cases in [test.py](test/ex/hw2/test.py) file which is copied and run next to the student's submission.  Doing so requires a few more options are clarified when building the autograder zip file:
- `-a test.py`: `test.py` should be added next to the student's submission:
- `-r test.py`: `test.py` should be the file run in the autograder (not the student's submission)
- `-v hw1.py`: `test.py` imports the student submission as `from hw1 import *`.  We should validate that a student's submission includes a file with this name

## See also

- [Otter-grader](https://otter-grader.readthedocs.io/en/latest/)
- [Gradescope-utils](https://github.com/gradescope/gradescope-utils)
