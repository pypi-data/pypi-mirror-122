from os import environ, remove
from os.path import isfile

from .config import system

s = system()

if s == "Linux":
    autostart_path = f"{environ['HOME']}/.config/autostart/AwakeGuardian.desktop"

    def create_autostart(file_path=autostart_path):
        with open(file_path, "w") as f:
            f.write(
                "[Desktop Entry]\nExec=AwakeGuardian\nHidden=false\nIcon=system-run\n"
                "Name=AwakeGuardian\nTerminal=false\nType=Application\n"
            )


elif s == "Windows":
    autostart_path = f"{environ['AppData']}/Microsoft/Windows/Start Menu/Programs/Startup/AwakeGuardian.bat"

    def create_autostart(file_path=autostart_path):
        with open(file_path, "w") as f:
            f.write(
                "@echo off\n"
                """FOR /F "delims=" %%i IN ('where AwakeGuardian.py') DO set aw=%%i"""  # don't change %%, """, ", '
                "\nstart pythonw %aw%\n"
            )


else:
    autostart_path = ""

    def create_autostart(file_path=autostart_path):
        pass


def is_autostart(path=autostart_path):
    return isfile(path)


def remove_autostart(file_path=autostart_path):
    remove(file_path)
