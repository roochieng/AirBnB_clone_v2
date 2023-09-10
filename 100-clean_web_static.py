#!/usr/bin/python3
"""
do_pack(): Generates a .tgz archive from the
contents of the web_static folder
do_deploy(): Distributes an archive to a web server
deploy (): Creates and distributes an archive to a web server
do_clean(): Deletes out-of-date archives
"""

from fabric.operations import local, run, put, sudo
from datetime import datetime
import os
from fabric.api import env
import re


env.hosts = ['34.234.193.37', '100.27.13.75']


def do_pack():
    """Function to compress files in an archive"""
    local("mkdir -p versions")
    filename = "versions/web_static_{}.tgz".format(datetime.strftime(
                                                   datetime.now(),
                                                   "%Y%m%d%H%M%S"))
    result = local(f"tar -cvzf {filename} web_static")
    if result.failed:
        return None
    return filename


def do_deploy(archive_path):
    """Function to distribute an archive to a server"""
    if not os.path.exists(archive_path):
        return False
    rex = r'^versions/(\S+).tgz'
    match = re.search(rex, archive_path)
    filename = match.group(1)
    res = put(archive_path, f"/tmp/{filename}.tgz")
    if res.failed:
        return False
    res = run(f"mkdir -p /data/web_static/releases/{filename}/")
    if res.failed:
        return False
    res = run(f"tar -xzf /tmp/{filename}.tgz -C /data/web_static/releases/{filename}/")
    if res.failed:
        return False
    res = run(f"rm /tmp/{filename}.tgz")
    if res.failed:
        return False
    res = run(f"mv /data/web_static/releases/{filename}"
              f"/web_static/* /data/web_static/releases/{filename}/")
    if res.failed:
        return False
    res = run(f"rm -rf /data/web_static/releases/{filename}/web_static")
    if res.failed:
        return False
    res = run("rm -rf /data/web_static/current")
    if res.failed:
        return False
    res = run(f"ln -s /data/web_static/releases/{filename}/ /data/web_static/current")
    if res.failed:
        return False
    print('New version deployed!')
    return True


def deploy():
    """Create and distribute an archive to a web server"""
    filepath = do_pack()
    if filepath is None:
        return False
    d = do_deploy(filepath)
    return d


def do_clean(number=0):
    """Delete out-of-date archives"""
    files = local("ls -1t versions", capture=True)
    file_names = files.split("\n")
    n = int(number)
    if n in (0, 1):
        n = 1
    for i in file_names[n:]:
        local(f"rm versions/{i}")
    dir_server = run("ls -1t /data/web_static/releases")
    dir_server_names = dir_server.split("\n")
    for i in dir_server_names[n:]:
        if i is 'test':
            continue
        run(f"rm -rf /data/web_static/releases/{i}")
