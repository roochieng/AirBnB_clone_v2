#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['34.234.193.37', '100.27.13.75']


def do_pack():
    """
    Generate a .tgz archive from the contents
    of the web_static folder of this repository.
    """
    d = datetime.now()
    now = d.strftime('%Y%m%d%H%M%S')
    if local("mkdir -p versions"):
        file_name = f"versions/web_static_{now}.tgz"
        local(f"tar -czvf {file_name} web_static")
        return file_name
    else:
        return None
    


def do_deploy(archive_path):
    """
    distribute an archive to the web servers
"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False


def deploy():
    """
    creat and distribut an archive to the web servers
"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
