import subprocess

import inferio


def test_version():
    version = subprocess.check_output(["poetry", "version"])

    assert f"inferio {inferio.__version__}" == version.decode().strip()
