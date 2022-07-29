import os
import sys
import time
import subprocess
import shutil
import win32com.shell.shell as shell
import __main__

def install():
    ASADMIN = 'asadmin'

    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        try:
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
            __main__.is_admin = True
        except:
            sys.exit()

    p = subprocess.run(["powershell.exe",
              "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass \n ./Dependencies/sub_install.ps1"], stdin=subprocess.DEVNULL, capture_output=True, text=True)

    user = os.getlogin()
    source = "./Dependencies/src"
    destination = f"C:/Users/{user}/Documents/SideKick"
    shutil.copytree(source, destination)

    os.rmdir("./Dependencies/src")
