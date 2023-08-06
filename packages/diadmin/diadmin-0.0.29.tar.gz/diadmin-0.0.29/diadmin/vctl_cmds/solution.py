import logging
from datetime import datetime
import json
import re
from os import path
from subprocess import check_output, run, CalledProcessError

VFLOW_PATHS = {'operators':'/files/vflow/subengines/com/sap/python36/operators/',
               'pipelines':'/files/vflow/graphs/',
               'dockerfiles':'/files/vflow/dockerfiles/'}

def list_solutions(user = False,from_date = None ) :
    logging.info('List solutions')
    solutions = json.loads(check_output(['vctl','solution','list','-o','json']).decode('utf-8'))
    # Filter
    if user :
        solutions = [s for s in solutions if re.match(f".+/{user}",s['CreatedBy'])]
    if from_date :
        solutions = [s for s in solutions if  datetime.strptime(s['CreatedAt'][:26],'%Y-%m-%dT%H:%M:%S.%f') > from_date ]
    return solutions

def download_solution(solution_name,version) :
    file = path.join('solutions',solution_name + '_' + version + '.zip')
    logging.info(f'Download solution: {solution_name} to {file}')
    run(['vctl','solution','download',solution_name,version,'-f',file])

def upload_solution(solution_file,user) :
    logging.info(f'Upload solution: {solution_file} to user: {user}')
    run(['vctl','solution','upload',solution_file,'-u',user])

def import_artifact(artifact_type,file,user) :
    logging.info(f'Import {artifact_type[:-1]}: {file} to user: {user}')
    run(['vctl','vrep','user','import',file,VFLOW_PATHS[artifact_type],'-u',user])

def import_solution(solution_file,user) :
    destination = '/files'
    run(['vctl','vrep','user','import',solution_file,destination,'-u',user])

def import_solution_sameuser(solution_file) :
    destination = '/'
    cmd = ['vctl','vrep','user','import',solution_file,destination]
    logging.info(f'Cmd: {" ".join(cmd)}')
    run(cmd)

def import_solution_repo(solution_name,version) :
    destination = '/files'
    run(['vctl','vrep','user','import-solution',solution_name,destination,version])