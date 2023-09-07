#!/usr/bin/python3
from fabric.api import run, put, env
from os import path


env.hosts = ['34.234.193.37', '100.27.13.75']
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    Distributes an .tgz archive through web servers
    """

    if path.exists(archive_path):
        if path.exists(archive_path) is False:
        return False
    else:
        try:
            put(archive_path, "/tmp/")
            file_name = archive_path.split("/")[1]
            file_name2 = file_name.split(".")[0]
            final_name = "/data/web_static/releases/" + file_name2 + "/"
            run("mkdir -p " + final_name)
            run("tar -xzf /tmp/" + file_name + " -C " + final_name)
            run("rm /tmp/" + file_name)
            run("mv " + final_name + "web_static/* " + final_name)
            run("rm -rf " + final_name + "web_static")
            run("rm -rf /data/web_static/current")
            run("ln -s " + final_name + " /data/web_static/current")
            print("Updated version deployed!")
            return True
        except Exception:
            return False
