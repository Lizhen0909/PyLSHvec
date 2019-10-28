'''
Created on Oct 11, 2019

@author: bo
'''

from pylshvec import utils
import jnius_config
import re

logger = utils.get_logger("pylshvec")

sub_re = re.compile(r"[^ACGT]")


class LSHVec(object):
    lshvec_jar_path = None
    
    @staticmethod 
    def set_lshvec_jar_path(jar_path):
        if jnius_config.vm_running:
            logger.warn("jvm is running, cannot set java path")
        else:
            LSHVec.lshvec_jar_path = jar_path
            jnius_config.add_classpath(jar_path)

    @staticmethod 
    def add_java_options(*args):
        if jnius_config.vm_running:
            logger.warn("jvm is running, cannot add options")
        else:
            jnius_config.add_options(*args)

        
    def __to_java_stirng (self,s):
        return self.autoclass("java.lang.String")(s)
    def __init__(self, model_file, hash_file, threshold=0.005, max_results=500, batch_size=1024,
                 num_thread=1, only_show_main_tax=False, without_uncult=True):

        from jnius import autoclass
        self.autoclass = autoclass
        PyLSHVec = self.autoclass("net.jfastseq.PyLSHVec")
        jlshvec = PyLSHVec(self.__to_java_stirng(model_file), self.__to_java_stirng(hash_file))
        
        jlshvec.setThreshold(threshold)
        jlshvec.setMaxItems(max_results)
        jlshvec.setBatchsize(batch_size)
        jlshvec.setNumThread(num_thread)
        jlshvec.setOnlyShowLeaf(only_show_main_tax)
        jlshvec.setWithoutUncult(without_uncult)

        jlshvec.initialize()
                
        self.model = jlshvec
    
    def __collection_to_arraylist(self, lst):
        alist = self.autoclass('java.util.ArrayList')()
        for u in lst:
            alist.add(u)
        return alist

    def __arraylist_to_list(self, alist):
        return [ alist.get(i) for i in range(alist.size())]
    
    def __sub_seqs(self, seqs):
        return [sub_re.sub("N", seq.upper()) for seq in seqs]

    def embedding_single_thread(self, seq_or_seqs):
        is_str = isinstance(seq_or_seqs, str)
        if is_str:
            seq_or_seqs = [seq_or_seqs]
        
        seq_or_seqs = self.__sub_seqs(seq_or_seqs)
        
        ret = [self.model.getEmbedding(u) for u in seq_or_seqs]

        if is_str:
            return ret[0]
        else:
            return ret
        
    def predict_single_thread(self, seq_or_seqs):
        is_str = isinstance(seq_or_seqs, str)
        if is_str:
            seq_or_seqs = [seq_or_seqs]
        
        seq_or_seqs = self.__sub_seqs(seq_or_seqs)
        
        ret = [self.model.predict(u) for u in seq_or_seqs]

        def f(line):
            line = [u.split(':') for u in line.split()]
            line = {int(u[0]):float(u[1]) for u in line}
            return line 

        ret = [f(ret[i]) for i in range(len(ret))]

        if is_str:
            return ret[0]
        else:
            return ret        

    def embedding(self, seq_or_seqs):
        is_str = isinstance(seq_or_seqs, str)
        if is_str:
            seq_or_seqs = [seq_or_seqs]
        
        seq_or_seqs = self.__sub_seqs(seq_or_seqs)
        
        ret = self.model.getEmbedding(seq_or_seqs)

        if is_str:
            return ret[0]
        else:
            return ret


    def predict(self, seq_or_seqs):
        is_str = isinstance(seq_or_seqs, str)
        if is_str:
            seq_or_seqs = [seq_or_seqs]
        
        seq_or_seqs = self.__sub_seqs(seq_or_seqs)
        #seq_or_seqs = self.__collection_to_arraylist(seq_or_seqs)
        ret = self.model.predict(seq_or_seqs)

        def f(line):
            line = [u.split(':') for u in line.split()]
            line = {int(u[0]):float(u[1]) for u in line}
            return line 

        ret = [f(ret[i]) for i in range(len(ret))]
        if is_str:
            return ret[0]
        else:
            return ret

    def getRank(self, nid):
        return self.model.getRank(nid);

    def hashTaxId(self, nid):
        return self.model.hasNode(nid);
    
    def getTaxIdPath(self, nid):
        return self.model.getTaxIdPath(nid);

    def getTaxNamePath(self, nid):
        return self.model.getTaxNamePath(nid);

    def getName(self, nid):
        return self.model.getName(nid);
    
    def getBatchsize(self) :
        return self.model.getBatchsize();

    def getVecDim(self) :
        return self.model.getVecDim();

    def  getMaxItems(self) :
        return self.model.getMaxItems();
 
    def  isOnlyShowLeaf(self) :
        return self.model.isOnlyShowLeaf();

    def  getNumThread(self) :
        return self.model.getNumThread();

    def  getThreshold(self) :
        return self.model.getThreshold();

    def  isWithoutUncult(self) :
        return self.model.isWithoutUncult();

    def  isOnlyShowMainTax(self) :
        return self.model.isOnlyShowMainTax();

    def  getKmerSize(self) :
        return self.model.getKmerSize();

    def  isInitialized(self) :
        return self.model.isInitialized();

        
if __name__ == '__main__':
    pass
