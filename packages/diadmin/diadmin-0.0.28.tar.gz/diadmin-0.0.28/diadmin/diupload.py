#
#  SPDX-FileCopyrightText: 2021 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

from os import path,makedirs,getcwd, walk
import errno
import logging
import argparse
import re
from subprocess import run

import yaml

from diadmin.vctl_cmds.login import di_login
from diadmin.vctl_cmds.vrep import get_all_files, mkdir_p,upload_file

VFLOW_PATHS = {'operators':'/files/vflow/subengines/com/sap/python36/operators/',
               'pipelines':'/files/vflow/graphs/',
               'dockerfiles':'/files/vflow/dockerfiles/'}

def save_open(file):
    parentpath = path.dirname(file)
    try:
        makedirs(parentpath)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and path.isdir(parentpath):
            pass
        else: raise
    return open(file, 'w')

def upload(artifact, artifact_type='operator') :

    folder = path.join(artifact_type,artifact.replace('.',path.sep))
    files = [path.join(root, name)  for root, dirs, filenames in walk(folder) for name in filenames]
    for f in files :
        pathlist = f.split(path.sep)
        parent_path = VFLOW_PATHS[artifact_type]
        for pf in pathlist[1:-1] :
            mkdir_p(parent_path,pf)
            parent_path = path.join(parent_path,pf)
        target = path.join(VFLOW_PATHS[artifact_type],path.relpath(f,artifact_type))
        upload_file(f,target)


def main() :
    logging.basicConfig(level=logging.INFO)

    #
    # command line args
    #
    description =  "Uploads operators, pipelines to SAP Data Intelligence.\nPre-requiste: vctl."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-c','--config', help = 'Specifies yaml-config file',default='config_demo.yaml')
    parser.add_argument('-o', '--operator', help='Uploads operators from operators-folder')
    parser.add_argument('-p', '--pipeline', help='Uploads pipelines from graphs-folder ')
    parser.add_argument('-d', '--dockerfile', help='Uploads dockerfiles from dockerfiles-folder')
    args = parser.parse_args()

    config_file = 'config.yaml'
    if args.config:
        config_file = args.config
    with open(config_file) as yamls:
        params = yaml.safe_load(yamls)

    ret = 0
    ret = di_login(params)
    if not ret == 0 :
        return ret

    if args.operator :
        upload(args.operator, 'operators')
    elif args.pipeline :
        upload(args.pipeline, 'pipelines')
    elif args.dockerfile :
        upload(args.dockerfile, 'dockerfiles')
    else:
        print('Error: Missing artifact type [-o,-p,-d]')
        return -1


if __name__ == '__main__':
    main()