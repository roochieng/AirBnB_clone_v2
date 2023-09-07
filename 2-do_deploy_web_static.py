#!/usr/bin/python3
from datetime import datetime
from fabric.api import *
from os import path


env.hosts = ['34.234.193.37', '100.27.13.75']
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    Distributes an .tgz archive through web servers
    """

    if path.exists(archive_path):
        if os.path.exists(archive_path) is False:
        return False
    else:
        try:
            archive = archive_path.split('/')[1]
            a_path = f"/tmp/{archive}"
            folder = archive.split('.')[0]
            f_path = f"/data/web_static/releases/{folder}/")
            put(archive_path, a_path)
            run(f"mkdir -p {f_path}")
            run(f"tar -xzf {a_path} -C {f_path}")
            run(f"rm {a_path}")
            run(f"mv -f {f_path}web_static/* {f_path}")
            run(f"rm -rf {f_path}web_static")
            run("rm -rf /data/web_static/current")
            run(f"ln -s {f_path} /data/web_static/current")

            return True
        except Exception:
            return False
