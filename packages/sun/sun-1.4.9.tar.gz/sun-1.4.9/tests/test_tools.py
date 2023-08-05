import subprocess
from sun.cli.tool import check_updates, process_status


def test_check_updates():
    message, packages = check_updates()
    if len(packages) == 0:
        assert message == 'No news is good news!'


def test_daemon_status():
    out = subprocess.getoutput('ps -a')
    if 'sun_daemon' in out:
        assert 'SUN is running...' == process_status()
    else:
        assert 'SUN not running' == process_status()
