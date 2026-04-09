import os
import sys


def project_dir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def assets_dir():
    return os.path.join(project_dir(), "assets")


def img_path(nome, pasta="bsfuctpath"):
    return os.path.join(assets_dir(), pasta, nome)


def cmd_path(nome):
    return os.path.join(assets_dir(), "cmds", nome)