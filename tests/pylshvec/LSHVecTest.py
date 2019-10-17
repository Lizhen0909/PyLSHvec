'''
Created on Oct 11, 2019

@author: bo
'''
import unittest
from pylshvec  import LSHVec, set_lshvec_jar_path, add_java_options
import numpy as np 

class Test(unittest.TestCase):

    def setUp(self):
        self.getIgnore = ['getRank', 'getName', 'getTaxIdPath', 'getTaxNamePath']
        self.jarpath = 'data/jlshvec-assembly-0.1.jar'
        set_lshvec_jar_path(self.jarpath)
        add_java_options("-Xmx16G")
        self.seqs = [
            "GTGTAGGCTTACACTCATGTTTTTTATCGTATTCATGAGTTATTAATTGTTCTACTTCTGGTAAACCTGCTACATTTTTACCCTCTAAAGTAATACTTTCACCACATGCTACCATGA\n" + 
                    "TTTTAAATTTACAGTCATCTATAAATTTTATCATATCTCCAGTTAACTTTTCAATTTTATCTACGTCTTTCATGTACATAGCAGCTTTTTCAGCAACAGCTGGATTTGATTTATCTGCTGCTACTTCAGCTAATCCATTTTTCTTTTCTTCACCTCTTTCATAAGTGTTCTC\n" + 
                    "GTTTGAAATTTGAATGTTTTCTTCAATTGCAACGAAAGCCTCAAGAATGGTCTTAGAAACATTCATCGCTAAAAGTGCTAAAAGTACAAGGTACATAAGACCTACCATCTTTTGCCTTGGGGTTTCTTTTCCTCCTCCCATTTTTTATTATCTTATTTTCTATTAATAAATG\n" + 
                    "TTTTTTTTAATTTAAAAGATCGATTAACCTTTATTGATAGACATAGCTTTTAACATGTTACCA",
            "AGCATCAGCGTATTGGTGCGCTCGCCGCCGTAGCCTAGTCCATCGGCAGTCTTAGCGATAGTAGTGACCATAAGCATGTCCCGACCAAGTAAGCTATCAGGGATTTCATAATAATACTTGC\n" + 
                    "CTTCGATCTCATGGACTTTAAACAATCCATCTTTTGATTTGGAAGCTTTGGTAATCACCTCGCCGTATGGTTTCGGGCCTGTGGATTTAGAGGGCTTTGCTGGAGCGACAGTCGCAGCAGGAGTATTTTTGGCATCTTTCTTCTTCTTTTTTTGTGCCAAAGTATCCCCTGA\n" + 
                    "ATACAACATAAAGCCCATGACTCCTAGGATAAGAGTAAATCTCCTAAGTAATTTGGGTAGTGAACTTCTCATTTAGACGTGAATTTTGTTAAGGTTATTAAACATCTAATTTCAATATTGGGTAGATATTGAACCTTCATTTTTGATGGGCGGTTTAATCTTCAAATTAAAG\n" + 
                    "GCAAAAGCGAAGTGGAAAAATTGGAAAATGTGATCATTGGAGGAGGGCTTGCGG",

            "ATGGCGGGGCCGTTCGGGCGTGCAGGAGGAAGAGGTGGGCGAGAACGCCCGCGGTCCCAGGGGGTGGGGTCAGCGCTTGGCGCGATTGAGCGGGTCCCAGTACTCGGAGTTGATCAAGGC\n" + 
                    "GCGCGCGCTGCCGCTGACGGGATCGGCCGGCGGGTTGATCTGGGTGTCCTTGCGGATCTCGGCGTGGCCGTCGGCGAAGTTCATGGAGCCGCCGGTGCGATGACGGAGGAAGTCGATTCCTTCATAGCCCTTGGTGGTGGAGGCCTTGGAGTTCATGCAGGACGACGGCCAC\n" + 
                    "CAGAGGGAGCTGGACCATTCCTTGTTTTGGGTGGGCATGGTTTCTCCGACTTCCATGGTGCTCGAGGGGCTGACGATGGAGGTCCGCTTGAACCAGGGGGCGACATCGAATCGGACGCCACCGACGGTCATGCTCTCGGCACCGTAAGGATGGCGGGCGAGGAAGAAGGCGT\n" + 
                    "TCATGCCGTACCCGACGAAGTGGGAATCAAACCTCCAGAACCAGTCGATGTTGTTGTCCTTGCGTTTCCCCTTGAGGGAGGGGCAGCGGAACATGTTGGTCTGGGGACGAGTGTTGTAGCCTTGGATGGTGACGCCCCACCAGTTGGTCAGGATGACCTGGCTCTGGCCGTT\n" + 
                    "GGCGAGGTTGCCGTTGCGATGGCCGGGGTACACGTCTTTGTTCTCGTCGGTGTA"
    ];

    def tearDown(self):
        pass

    def show_model(self, model):
        for u in dir(model):
            if not u in self.getIgnore:
                if u.startswith('get') or u.startswith('is'):
                    fun = getattr(model, u)
                    print(u, fun())
        for u in self.getIgnore:
            fun = getattr(model, u)
            print(u, fun(410536))
            
    def testPredict(self):
        obj = LSHVec("data/model/model_299", 'data/lsh/lsh_CAMI2_pacbio_k9_h25.crp')
        self.show_model(obj)
        
        result = obj.predict(self.seqs[0])
        print(result)
        
        result = obj.predict(self.seqs)
        self.assertEqual(len(self.seqs), len(result))
        for u in result:
            print (u)

        result = obj.embedding(self.seqs[0])
        print(result)
        

    def testPredictMulithread(self):
        obj = LSHVec("data/model/model_299", 'data/lsh/lsh_CAMI2_pacbio_k9_h25.crp', num_thread=4)
        self.show_model(obj)
        
        result = obj.predict(self.seqs[0])
        print(result)
        
        result1 = obj.predict(self.seqs)
        self.assertEqual(len(self.seqs), len(result1))
        for u in result1:
            print (u)

        result2 = obj.predict_single_thread(self.seqs)
        self.assertEqual(len(self.seqs), len(result2))
        for u in result2:
            print (u)
            
        for u,v in zip(result1,result2):
            self.assertAlmostEqual(np.sum(np.abs(list(u.values()))),np.sum(np.abs(list(v.values()))))

        print("embedding by single thread")
        result1 = obj.embedding_single_thread(self.seqs)
        self.assertEqual(len(self.seqs), len(result1))
        for u in result1:
            print (u)
 
        print("embedding by multiple threads")
        result2 = obj.embedding(self.seqs)
        self.assertEqual(len(self.seqs), len(result2))
        for u in result2:
            print (u)
            
        for u,v in zip(result1,result2):
            self.assertAlmostEqual(np.sum(np.abs(u)),np.sum(np.abs(v)))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testConstructor']
    unittest.main()
