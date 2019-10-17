
from .lshvec import LSHVec

def set_lshvec_jar_path(jar_path):
    LSHVec.set_lshvec_jar_path(jar_path)

def add_java_options(*args):
    LSHVec.add_java_options(*args)
