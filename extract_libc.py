# -*-coding:utf-8-*-
__author__ = 'joker'

import os
import commands
import sys

def list_dir(rootdir):
    file_list = []
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            #print "the full name of the file is:" + os.path.join(parent, filename)
            file_list.append(os.path.join(parent,filename))
    return file_list

def extract_libc(filename):
    filename_tmp = os.path.basename(filename)
    (shotname,extension) = os.path.splitext(filename_tmp)
    if extension != ".deb":
        return None,None,None
    tempdirectory= "/tmp/{0}".format(shotname)
    _,_ = commands.getstatusoutput("mkdir {0}".format(tempdirectory))
    _,_ = commands.getstatusoutput("dpkg-deb -x {0} {1}".format(filename,tempdirectory))
    status, output = commands.getstatusoutput('find {0} -name "libc-*.so" -print'.format(tempdirectory))
    return shotname,output,tempdirectory


def extract_libc_run(rootdir):
    _,_ = commands.getstatusoutput("mkdir ./libc_collections")
    file_list = list_dir(rootdir)
    for filename in file_list:
        libc_version,libc_path,tempdirectory = extract_libc(filename)
        if libc_version is None:
            continue
        libc_record = libc_version + "-" + os.path.basename(libc_path)
        _,_ = commands.getstatusoutput("cp {0} ./libc_collections/{1}".format(libc_path,libc_record))
        _,_ = commands.getstatusoutput("rm -rf {0}".format(tempdirectory))

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print "python extract_libc.py rootdir_of_debs"
        sys.exit(-1)
    rootdir = sys.argv[i]
    extract_libc_run(rootdir)
