
# LSHVec pre-trained models and its Python bindings 

This project is still in progress. Check it later.

## Summary

This repository presents a few of pre-tained models with JLSHVec (which is a rewritten java version of  [LSHVec](https://github.com/Lizhen0909/LSHVec)).  See [Remark](#remark) for technical details.

Python codes and examples to uses these models are also provided. 

## Remark

### What is JLSHVec ? Why JLSHVec instead of LSHVec? 

JLSHVec is a rewritten version of [LSHVec](https://github.com/Lizhen0909/LSHVec) in Java language. 

When we use LSHVec with big dataset (e.g. [GenBank](https://www.ncbi.nlm.nih.gov/genbank/), [RefDB](https://www.ncbi.nlm.nih.gov/pubmed/12652131)), we found that LSHVec is hard to process such a big data size.

The reason is that LSHVec which inherits from [FastText](https://fasttext.cc/) requires the input is text format separated by white space and then loads all the text in memory. This is acceptable for natural languages since the data size is at most tens GBs.

However in LSHVec k-mers are used instead of words. Suppose we want to train a k-mer embedding of simulated Illumina reads with RefDB bacteria assemblies (about 500G genetic bits). The number of kmers is about D*n, where D is the assembly data size and n is coverage. In our case, assuming n=10 and k=23, the number of kmers is 5T and requires a disk space of 125TB and tens TB of memory, which is unrealistic even for most HPC systems.

### How were JSLVec pre-trained models trained ?
First we prepared a RockDB for the reference sequences (e.g. all RefDB bacteria assemblies). 

Then we have several nodes to train the model: one node (train node) trains the vectors and others (hash nodes) generate and hash kmers. The nodes pass protocol-buf message with a Redis server. 

Hash node randomly reads reference sequences from RockDB, simulates (e.g. simulations Illumina, Pacbio, Gold Standard) reads, generates kmers and hashes them, then feeds the hashed-kmer-sequences to a Redis queue.

Train node reads from the Redis queue and does jobs of embedding or classification training.  Our training code supports hierarchical softmax using NCBI taxonomy tree, which is essential for multi-label(an instance can have a label for each rank) and multi-class(an instance can only have one label for a rank)  mixture classification model.

## Requirements

1. Python 3.6
2. Jnius >=1.1.0
3. java >=1.8

## Install

### build from source
```bash
git clone https://github.com/Lizhen0909/PyLSHvec.git && cd pylshvec && python setup.py install
```

### or use pip
```bash
pip install pylshvec
```

### or use docker
```bash
docker pull lizhen0909/pylshvec
```



## Download 

### JLSHvec jar file
  The pre-trained models were trained with a rewritten  [LSHVec](https://github.com/Lizhen0909/LSHVec) in java. 
  The assembly jar file is needed to load the models.

  [Download jlshvec-assembly-0.1.jar](https://www.amazon.com/clouddrive/share/4NiogpuW1lzBMyGmMlkrDbjhSMYpQgWjW5GUcKFR7Q6)
  
  **md5sum**: aeb207b983b3adc27e14fd9c431e2130



### Pre-trained model

#### refdb viruses classfication model

* model file: [refdb_viruses_model_gs_k23_l3000_rand_model_299](https://www.amazon.com/clouddrive/share/RmoJ1lduzlqstAJFnKg0aAlx82AyCjnzKncfGjQIQMg) [size: 5.3G]

  **md5sum** 2502b284b336734300c2297d23d1d349 

* hash function file: [lsh_nt_NonEukaryota_k23_h25.crp](https://www.amazon.com/clouddrive/share/6ZNvMXMy30b4vc0RYNVG1lbf1ih8WgpoQ9w4lX91IXy)

  **md5sum** 5eea8a98d224b7ff505091bd483ca75c 

#### refdb bacteria classfication model

* model file: [refdb_bacteria_model_gs_k23_l3000_rand_model_214](https://www.amazon.com/clouddrive/share/LoXz6k229SwYuElPTHvu0SSJOq56nJenvBbOTGVeb9a) [size: 11G]

  **md5sum** 402e9a286b71068999caa9766b2dbf8c 

* hash function file: [lsh_nt_NonEukaryota_k23_h25.crp](https://www.amazon.com/clouddrive/share/6ZNvMXMy30b4vc0RYNVG1lbf1ih8WgpoQ9w4lX91IXy)

  **md5sum** 5eea8a98d224b7ff505091bd483ca75c 

### Sample data

* ActinoMock Nanopore Sample [size: 500M].

  The data is used in example notebook [example_use_vectors_in_bacteria_classfication_model.ipynb](notebook/example_use_vectors_in_bacteria_classfication_model.ipynb).
  
  [Download from FSU](http://ww2.cs.fsu.edu/~lshi/ActinoMock_Nanopore.seq.gz)
  &emsp;&emsp;
  [Download from Amazon Drive](https://www.amazon.com/clouddrive/share/eTIKYVLckXUCMnMQSpO8TCqZOwekmBrx23ZhMa3XO8d)
  
  **md5sum**: b7f3e55438fdc05920aee693a98ded2e

