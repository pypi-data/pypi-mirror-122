#
#  SPDX-FileCopyrightText: 2021 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

from os import path,makedirs,getcwd, walk
import logging
import argparse
import tarfile
import re

import yaml

from diadmin.vctl_cmds.login import di_login
from diadmin.vctl_cmds.vrep import get_all_files, mkdir_p,upload_file,import_artifact

VFLOW_PATHS = {'operators':'/files/vflow/subengines/com/sap/python36/operators/',
               'pipelines':'/files/vflow/graphs/',
               'dockerfiles':'/files/vflow/dockerfiles/'}


def make_tarfile(source_dir) :
    tar_filename = path.join(path.dirname(source_dir),path.basename(source_dir) + '.tgz')
    with tarfile.open(tar_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=path.basename(source_dir))
    return tar_filename

def main() :
    logging.basicConfig(level=logging.INFO)

    #
    # command line args
    #
    achoices = ['operators','pipelines','dockerfiles','bundle','solution']
    description =  "Uploads operators, pipelines, dockerfiles, bundle and solution to SAP Data Intelligence.\nPre-requiste: vctl."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-c','--config', help = 'Specifies yaml-config file',default='config_demo.yaml')
    parser.add_argument('-r','--conflict', help = 'Conflict handling flag of \'vctl vrep import\'')
    parser.add_argument('-a', '--artifact_type', help='Type of artifacts',choices=achoices)
    parser.add_argument('-f', '--artifact', help='Artifact file(tgz) or directory')
    parser.add_argument('-u', '--user', help='Filter on user created solutions')
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

    user = params['USER']
    if  args.user :
        user = args.user

    conflict = None
    if args.conflict :
        conflict = args.conflict

    if re.match('.+\.tgz$',args.artifact) or re.match('.+\.tar.gz$',args.artifact) :
        import_artifact(args.artifact_type,args.artifact,user,conflict)
    else :
        tf = make_tarfile(args.artifact)
        import_artifact(args.artifact_type,tf,user,conflict)


if __name__ == '__main__':
    main()