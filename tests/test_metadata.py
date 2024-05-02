import subprocess

import inferio_x


def test_version():
    version = subprocess.check_output(["poetry", "version"])

    assert f"inferio-x {inferio_x.__version__}" == version.decode().strip()
