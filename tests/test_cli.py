import subprocess
import sys
from pathlib import Path
import pytest

def test_example_and_no_overwrite(tmp_path):
    out=tmp_path/'example'
    command=[sys.executable,'-m','athena_cohortbridge','example','--output',str(out)]
    subprocess.run(command,check=True,capture_output=True)
    assert (out/'result.json').is_file()
    second=subprocess.run(command,capture_output=True)
    assert second.returncode!=0


def test_invalid_input_does_not_leave_output_directory(tmp_path):
    source=tmp_path/'invalid.csv';source.write_text('invalid\n1\n')
    out=tmp_path/'out'
    result=subprocess.run([sys.executable,'-m','athena_cohortbridge','run','--input',str(source),'--output',str(out)],capture_output=True,text=True)
    assert result.returncode==2
    assert not out.exists()
    assert 'Traceback' not in result.stderr


def test_package_specific_help_has_no_unrelated_metadata_argument():
    result=subprocess.run([sys.executable,'-m','athena_cohortbridge','run','--help'],capture_output=True,text=True,check=True)
    assert '--metadata' not in result.stdout
