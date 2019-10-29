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
        """
            Set jlshvec jar library path
        """
        
        if jnius_config.vm_running:
            logger.warn("jvm is running, cannot set java path")
        else:
            LSHVec.lshvec_jar_path = jar_path
            jnius_config.add_classpath(jar_path)
    

    @staticmethod 
    def add_java_options(*args):
        """
            Add jnius java options (refer to jnius_config.add_options)
        """
        
        if jnius_config.vm_running:
            logger.warn("jvm is running, cannot add options")
        else:
            jnius_config.add_options(*args)
        
    def __to_java_stirng (self, s):
        return self.autoclass("java.lang.String")(s)

        
    def __init__(self, model_file, hash_file, threshold=0.005, max_results=500, batch_size=1024,
                 num_thread=1, only_show_main_tax=False, without_uncult=True):
        """
            load a pre-trained lshvec model. 
            
            Parameters:
                model_file: pre-trained model file, which contains k-mer vectors and model parameters
                hash_file: lsh hash function file

            Refer to get methods for the meaning of other parameters
        """
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
        """
            Get the embedding vector/vectors for a sequence or a list of sequence (single thread version)
        """
        
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
        """
            Give the probabilities for each node in the taxonomy tree for a sequence or a list of sequence . (single thread version)
        """
        
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
        """
            Get the embedding vector/vectors for a sequence or a list of sequence (multiple threads if #thread > 1)
        """
        
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
        '''
            Give the probabilities for each node in the taxonomy tree for a sequence or a list of sequence . (multiple threads if #thread > 1)
        '''
        
        is_str = isinstance(seq_or_seqs, str)
        if is_str:
            seq_or_seqs = [seq_or_seqs]
        
        seq_or_seqs = self.__sub_seqs(seq_or_seqs)
        # seq_or_seqs = self.__collection_to_arraylist(seq_or_seqs)
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
        """
            return rank of a tax id. e.g. 2 -> superkingdom
        """
        
        return self.model.getRank(nid);


    def hashTaxId(self, nid):
        """
            check if a tax id exists in the model.
        """
        
        return self.model.hasNode(nid);
    

    def getTaxIdPath(self, nid):
        """
             return path of a taxid (from root to this taxid)
        """
        
        return self.model.getTaxIdPath(nid);


    def getTaxNamePath(self, nid):
        """
             return taxid name path of a taxid (from root to this taxid)
        """
        
        return self.model.getTaxNamePath(nid);


    def getName(self, nid):
        """
            return name of a tax id. e.g. 2 -> bacteria
        """
        
        return self.model.getName(nid);
    

    def getBatchsize(self) :
        """
            batch size when make prediction or embedding (internal use)
        """
        
        return self.model.getBatchsize();


    def getVecDim(self) :
        """
            embedding vector size
        """
        
        return self.model.getVecDim();


    def  getMaxItems(self) :
        """
            maximum number of taxids returned for prediction of a sequence. 
            It prevent to return too many results since a usually a taxonomy tree has millions of nodes.
        """
        
        return self.model.getMaxItems();


    def  isOnlyShowLeaf(self) :
        """
            Only return predictions of leaf nodes (that is only species or strains)
        """ 
        
        return self.model.isOnlyShowLeaf();


    def  getNumThread(self) :
        """
            The number of threads 
        """
        
        return self.model.getNumThread();


    def  getThreshold(self) :
        """
            Probability threshold. The prediction of a taxid is returned only when its probability is greater than the threshold  
        """
        
        return self.model.getThreshold();


    def  isWithoutUncult(self) :
        """
            Whether returns uncultured taxid
        """
        
        return self.model.isWithoutUncult();


    def  isOnlyShowMainTax(self) :
        """
            whether only show main ranks (a.k.a superkingdom, phylum, class, order, family, genus, species) 
        """
        
        return self.model.isOnlyShowMainTax();


    def  getKmerSize(self) :
        """
            The kmer size used when the model was trained
        """
        
        return self.model.getKmerSize();

    def  isInitialized(self) :
        return self.model.isInitialized();

        
if __name__ == '__main__':
    pass
