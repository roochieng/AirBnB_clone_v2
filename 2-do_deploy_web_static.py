#!/usr/bin/python3
from datetime import datetime
from fabric.api import *
from os import path


env.hosts = ['34.234.193.37', '100.27.13.75']


def do_pack():
    """
    Generates a .tgz archive from the contents
    of the web_static folder of this repository.
    """

    d = datetime.now()
    now = d.strftime('%Y%m%d%H%M%S')

    local("mkdir -p versions")
    local(f"tar -czvf versions/web_static_{now}.tgz web_static")


def do_deploy(archive_path):
    """
    Distributes an .tgz archive through web servers
    """

    if path.exists(archive_path):
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

    return False
