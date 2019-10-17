'''
Created on Apr 6, 2018

@author: lizhen
'''

import os
import logging
import tempfile
import shutil
import time
import sys
import subprocess
import importlib
import multiprocessing
import fnmatch
from multiprocessing import Pool

def check_output_file_exists(prefix, logger):
    file1 = prefix + ".gz"
    if file_exists(file1):
        logger.info("{} exists, skip!".format(file1))
        return True

    file1 = prefix + ".zst"
    if file_exists(file1):
        logger.info("{} exists, skip!".format(file1))
        return True
    return False


def get_input_file(prefix, logger):
    file1 = prefix + ".gz"
    if file_exists(file1):
        return file1
    
    file1 = prefix + ".zst"
    if file_exists(file1):
        return file1
    
    raise Exception("file not found for {}.[gz|.zst]".format(prefix))

def file_exists(file_path):
    return os.path.exists(file_path)


def create_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def remove_if_file_exit(fname, is_dir=False):
    if os.path.exists(fname):
        if is_dir: 
            shutil.rmtree(fname) 
        else:
            os.remove(fname)


def list_dir(mypath, pattern=None):
    onlyfiles = [f for f in os.listdir(mypath)]
    if pattern is not None:
        onlyfiles = [ u for u in onlyfiles if fnmatch.fnmatch(u, pattern)]
    return [os.path.join(mypath, u) for u in onlyfiles if os.path.isfile(os.path.join(mypath, u))]


def set_if_not_exists(self, name, fun):
    if hasattr(self, name):
        return getattr(self, name)
    else:
        # print ("call fun for " + name)
        value = fun()
        setattr(self, name, value)
        return value 


def abspath(fpath):
    return os.path.abspath(fpath)


def path_equals(path1, path2):    
    return os.path.abspath(path1) == os.path.abspath(path2)    

            
def basename(path):        
    return os.path.basename(path)


def touch(filepath):
    with open(filepath, 'a'):
        os.utime(filepath, None)


_LOGGERS = {}


def get_logger(name):
    if name not in _LOGGERS:
        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        logger.addHandler(ch)
        _LOGGERS[name] = logger 
    return _LOGGERS[name]


logger = get_logger("utils")


class TempDir():

    def __init__(self):
        self.dirpath = None  
        
    def __enter__(self):
        self.dirpath = tempfile.mkdtemp()
        return self.dirpath

    def __exit__(self, type, value, traceback):
        if self.dirpath is not None:
            shutil.rmtree(self.dirpath)


def shell_run_and_wait2(command, working_dir=None, env=None, logger=None):
    
    fd, path = tempfile.mkstemp()
    if logger is None:
        print ("tmp file: ", path)
        print ("cmd: ", command)
    else:
        logger.info("tmp file: "+ path)
        logger.info("cmd: "+ command)
    try:
        with os.fdopen(fd, 'wt') as fin:
            fin.write(command)
        status = shell_run_and_wait("bash " + path, working_dir=working_dir, env=env)
    finally:
        os.remove(path)
    return status

        
def shell_run_and_wait(command, working_dir=None, env=None):
    curr_dir = os.getcwd()
    if working_dir is not None:
        os.chdir(working_dir)
    command = command.split(" ")
    import subprocess
    
    # process = subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process = subprocess.Popen(command, env=env)
    process.wait()
    if working_dir is not None:
        os.chdir(curr_dir)
    return process.returncode


def timeit(fun):
    t0 = time.time()
    ret = fun()
    t1 = time.time()
    return t1 - t0, ret

 

def urlretrieve(src, dst):
    try:
        if sys.version_info[0] >= 3:
            from urllib.request import urlretrieve
        else:
            # Not Python 3 - today, it is most likely to be Python 2
            # But note that this might need an update when Python 4
            # might be around one day
            from urllib import urlretrieve
        return urlretrieve(src, dst)
    except:
        remove_if_file_exit(fname=dst, is_dir=False)
        raise


def check_output(lst):
    if sys.version_info[0] >= 3:
        return subprocess.getoutput((" ".join (lst)))
    else:
        return subprocess.check_output(lst)        


def link_file(path, dest_dir=None, destname=None):
    assert not(dest_dir is None and destname is None)
    if not os.path.exists(path):
        raise Exception("source path not found: " + path)
    if dest_dir is None:
        destpath = destname
    else: 
        if destname is None :
            destname = path.split("/")[-1]
        destpath = os.path.join(dest_dir, destname)
        
    remove_if_file_exit(destpath)
    os.symlink(path, destpath)
    return destpath            


def try_import(module_name, module_path):
    '''
    import module, if failed try import from module_path
    '''
    try:
        return importlib.import_module(module_name)
    except: 
        if not module_path in sys.path:
            sys.path.insert(0, module_path)
            # print(module_name,module_path)
        return importlib.import_module(module_name)


def check_module_available(module_name):
    try:
        importlib.import_module(module_name)
        return True 
    except ImportError: 
        return False


def get_num_thread(nthread=None):
    if nthread is not None and nthread > 0: return nthread
    if 'OMP_NUM_THREADS' in os.environ:
        nthread = int(os.environ['OMP_NUM_THREADS'])
    elif 'SLURM_CPUS_ON_NODE' in os.environ:
        nthread = int(os.environ['SLURM_CPUS_ON_NODE'])
        
    if nthread is None  or nthread < 1:
        nthread = max(1, multiprocessing.cpu_count() - 1)
    return nthread  

    

    
def unique_name():
    import uuid
    return str(uuid.uuid4())    
    

def move(tmpoutpath, outpath):
    shutil.move(tmpoutpath, outpath) 
    assert file_exists(outpath)



