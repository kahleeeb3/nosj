import os
import subprocess

################################################################################
# TODO: Put the name of your executable here.
################################################################################
EXEC_NAME = 'nosj.py'

def check_valid(input_path):
    res = subprocess.run(['./'+EXEC_NAME, input_path], capture_output=True)

    if res.returncode != 0:
        return False

    if len(res.stderr) != 0:
        return False

    got = res.stdout
    with open(input_path.replace('.input', '.output'), 'rb') as handle:
        want = handle.read()
    if got != want:
        return False

    return True

def check_invalid(input_path):
    res = subprocess.run(['./'+EXEC_NAME, input_path], capture_output=True)

    if res.returncode != 66:
        return False

    if len(res.stderr) == 0:
        return False

    if not res.stderr.decode('ascii').startswith('ERROR -- '):
        return False

    return True

def main():
    errors = []

    spec_valid_filenames = os.listdir('./from-spec/valid/')
    for valid_filename in spec_valid_filenames:
        if not valid_filename.endswith('.input'):
            continue

        abs_path = os.path.abspath(os.path.join('from-spec', 'valid', valid_filename))
        if not check_valid(abs_path):
            errors.append('incorrect handling of valid file: '+abs_path)
        else:
            print('OK --', abs_path)

    spec_invalid_filenames = os.listdir('./from-spec/invalid/')
    for invalid_filename in spec_invalid_filenames:
        assert(invalid_filename.endswith('.input')), 'non-framework file: '+invalid_filename

        abs_path = os.path.abspath(os.path.join('from-spec', 'invalid', invalid_filename))
        if not check_invalid(abs_path):
            errors.append('incorrect handling of invalid file: '+abs_path)
        else:
            print('OK --', abs_path)

    for error in errors:
        print('ERROR --', error)

main()
