
# LSHVec pre-trained models and its Python bindings 


## Summary

This repository presents a few of pre-tained models with JLSHVec (which is a rewritten java version of  [LSHVec](https://github.com/Lizhen0909/LSHVec)).  See [Remark](#remark) for technical details.

Python codes and examples to uses these models are also provided. 


## Requirements

1. Python 3.6
2. cython>=0.28.5
3. Jnius >=1.1.0
4. java >=1.8

## Install

### build from source
```bash
git clone https://github.com/Lizhen0909/PyLSHvec.git && cd PyLSHvec && python setup.py install
```

### or use pip
```bash
pip install pylshvec
```

### or use docker
```bash
docker pull lizhen0909/pylshvec
```

### or use singularity 3
```bash
singularity pull --name pylshvec.sif shub://Lizhen0909/PyLSHvec
```

## How to use

Put things simply, just

```python
from pylshvec import *

#here needs jlshvec jar file, download it first
set_lshvec_jar_path("/mnt/jlshvec-assembly-0.1.jar")

#since vector model is usually large, set a big java memory limit is preferred. 
add_java_options("-Xmx32G")

#here need model file and lsh function file, download them first
#use help(model) to see all the methods and constructor options 
model= LSHVec(model_file="/mnt/refdb_viruses_model_gs_k23_l3000_rand_model_299", 
              hash_file="/mnt/lsh_nt_NonEukaryota_k23_h25.crp")

reads = ['ACGTACGT.....', 'ACGTACGT.....', 'ACGTACGT.....', 'ACGTACGT.....', ....]

predicts = model.predict(reads)

```

For more complete examples please see the notebooks (see [Download](#download) for minimum memory requirement):

[example_use_virus_classfication_model.ipynb](notebook/example_use_virus_classfication_model.ipynb)

[example_use_bacteria_classfication_model.ipynb](notebook/example_use_bacteria_classfication_model.ipynb)

[example_use_vectors_in_bacteria_classfication_model.ipynb](notebook/example_use_vectors_in_bacteria_classfication_model.ipynb)

[example_use_Illumina_bacteria_classfication_model.ipynb](notebook/example_use_Illumina_bacteria_classfication_model.ipynb)

[example_use_Pacbio_bacteria_classfication_model.ipynb](notebook/example_use_Pacbio_bacteria_classfication_model.ipynb)

### Use Docker
Assume you put your data in /mnt/data and your notebook in /mnt/notebook. 

* run python or ipython
```bash
docker run -v /mnt/data:/data -it lizhen0909/pylshvec python #or ipython
```
* run Jupyter notebook 

```bash
docker run -v /mnt/data:/data -v /mnt/notebook:/notebook -p 8888:8888  -it lizhen0909/pylshvec jupyter_notebook
```
   Find connection url in the console output.
   
### Use Singularity

Since singularity maps the $HOME directory, here just assumes data/model are going to locate in $HOME. Otherwise, you need map the directories like docker.

* run python or ipython
```bash
singularity run pylshvec.sif python #the nrun any pylshvec code 
```
* run Jupyter notebook 
```bash
#It should work, however singularity maps too many things that host settings may affect the notebook
singularity run  --bind $HOME/notebook:/notebook pylshvec.sif jupyter_notebook 
```

## Download 

### JLSHVec jar file
  The pre-trained models were trained with a rewritten  [LSHVec](https://github.com/Lizhen0909/LSHVec) in java. 
  The assembly jar file is needed to load the models.

  [Download jlshvec-assembly-0.1.jar](https://www.amazon.com/clouddrive/share/4NiogpuW1lzBMyGmMlkrDbjhSMYpQgWjW5GUcKFR7Q6)
  
  **md5sum**: aeb207b983b3adc27e14fd9c431e2130


### Pre-trained models

**Be Warned** that like all the machine learning models, the model cannot preform better beyond the data. If your data is significant other than the pre-trained model data, training your own model is preferred. 

Here are issues I can think of:

* Some NCBI taxonomy id may never be predicted since not all ids have train data.
* Data is not balanced. Some ids (e.g. a specified species) have much more data than others, which makes prediction may prefer to the rich-data ids.
* Strain (even some species) prediction is terrible. Don't expect it.


#### RefDB viruses classfication model

Trainned with 9.3k viruses assemblies of RefDB. Minimum Java memory: 16G.

* model file: [refdb_viruses_model_gs_k23_l3000_rand_model_299](https://www.amazon.com/clouddrive/share/RmoJ1lduzlqstAJFnKg0aAlx82AyCjnzKncfGjQIQMg) [size: 5.3G]

  **md5sum** 2502b284b336734300c2297d23d1d349 

* hash function file: [lsh_nt_NonEukaryota_k23_h25.crp](https://www.amazon.com/clouddrive/share/6ZNvMXMy30b4vc0RYNVG1lbf1ih8WgpoQ9w4lX91IXy)

  **md5sum** 5eea8a98d224b7ff505091bd483ca75c 

#### RefDB bacteria classfication model

Trainned with 42k bacteria assemblies of RefDB. Minimum Java memory: 32G.

* model file: [refdb_bacteria_model_gs_k23_l3000_rand_model_214](https://www.amazon.com/clouddrive/share/LoXz6k229SwYuElPTHvu0SSJOq56nJenvBbOTGVeb9a) [size: 11G]

  **md5sum** 402e9a286b71068999caa9766b2dbf8c 

* hash function file: [lsh_nt_NonEukaryota_k23_h25.crp](https://www.amazon.com/clouddrive/share/6ZNvMXMy30b4vc0RYNVG1lbf1ih8WgpoQ9w4lX91IXy)

  **md5sum** 5eea8a98d224b7ff505091bd483ca75c 

#### GenBank bacteria and viruses classfication model (Illumina Simulation)

Trainned with 54k assemblies from GenBank. **Only one assembly was sampled for each species.** Because viruses data is too samll compared to bateria, it rarely predicts any viruses. Just take it as a bateria model.  

[art_illumina](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3278762/) was used to simulate the paired-end reads with length of 150, mean size of 270 and stddev of 27. 

Minimum Java memory: 48G.

* model file: [genbank_model_ill_k23_model_299](https://www.amazon.com/clouddrive/share/zQnu2ti1vfBMGcXrRqsohgfzuaYzZs4HGESP58vobRn) [size: 12G]

  **md5sum** d6b117a4c7ffe4f25e6c532a88bb3a47 

* hash function file: [lsh_CAMI2_illumina_k23_h25.crp](https://www.amazon.com/clouddrive/share/efWceiTHId4EVhY1DEppmW6amyBQoEt3iIU6oW5FbcX)
  
  **md5sum** 706633919e347f920ce6ab3277091efb 
  
#### GenBank bacteria and viruses classfication model (Pacbio Simulation)

Trainned with 54k assemblies from GenBank. **Only one assembly was sampled for each species.** Because viruses data is too samll compared to bateria, it rarely predicts any viruses. Just take it as a bateria model.  

[pbsim](https://github.com/pfaucon/PBSIM-PacBio-Simulator) was used to simulate the pacbio reads with Continuous Long Read (CLR) profile, mean size of 3000 and stddev of 1000. 

Minimum Java memory: 16G.

* model file: [genbank_model_pb_k9_model_299](https://www.amazon.com/clouddrive/share/OmU9cmVKknacpt0W9HpI6QY2jXC17dQpWaaERpLhOGl) [size: 121M]

  **md5sum** 351275531493a4866be4afcd9df3932c 

* hash function file: [lsh_CAMI2_pacbio_k9_h25.crp](https://www.amazon.com/clouddrive/share/zw4JwJCE4Lst5I4q36ijwrhc3db9rHYsCuyQ4KkihVC)
  
  **md5sum** df7ee38cf8b58d5f8034bb9b266e3334 
  
### Sample data

* ActinoMock Nanopore Sample [size: 500M].

  The data is used in example notebook [example_use_vectors_in_bacteria_classfication_model.ipynb](notebook/example_use_vectors_in_bacteria_classfication_model.ipynb).
  
  [Download from FSU](http://ww2.cs.fsu.edu/~lshi/ActinoMock_Nanopore.seq.gz)
  &emsp;&emsp;
  [Download from Amazon Drive](https://www.amazon.com/clouddrive/share/eTIKYVLckXUCMnMQSpO8TCqZOwekmBrx23ZhMa3XO8d)
  
  **md5sum**: b7f3e55438fdc05920aee693a98ded2e

## Remark

### What is JLSHVec ? Why JLSHVec instead of LSHVec? 

JLSHVec is a rewritten version of [LSHVec](https://github.com/Lizhen0909/LSHVec) in Java language. 

When we use LSHVec with big dataset (e.g. [GenBank](https://www.ncbi.nlm.nih.gov/genbank/), [RefDB](https://www.ncbi.nlm.nih.gov/pubmed/12652131)), we found that LSHVec is hard to process such a big data size.

The reason is that LSHVec which inherits from [FastText](https://fasttext.cc/) requires the input is text format separated by white space and then loads all the text in memory. This is acceptable for natural languages since the data size is at most tens GBs.

However in LSHVec k-mers are used instead of words. Suppose we want to train a k-mer embedding of simulated Illumina reads with RefDB bacteria assemblies (about 500G genetic bits). The number of kmers is about D*n, where D is the assembly data size and n is coverage. In our case, assuming n=10 and k=23, the number of kmers is 5T and requires a disk space of 125TB, of which the data preparation and loading process will take forever.

### How were JLSHVec pre-trained models trained ?
First we prepared a [RockDB](https://rocksdb.org/) for the reference sequences (e.g. all bacteria assemblies in RefDB). 

Then we have several nodes to train the model: one node (train node) trains the model and others (hash nodes) generate and hash kmers. The nodes communicates by passing [protocol-buf](https://developers.google.com/protocol-buffers) message with a [Redis](https://redis.io/) server.

A hash node randomly reads reference sequences from the RockDB, simulates (e.g. simulations Illumina, Pacbio, Gold Standard) reads, generates kmers and hashes them, then feeds the hashed-kmer-sequences to a Redis queue.

Train node reads from the Redis queue and does jobs of embedding or classification training.  Our training code supports hierarchical softmax using NCBI taxonomy tree, which is essential for multi-label(an instance can have a label for each rank) and multi-class(an instance can only have one label for a rank)  mixture classification model.

## Citation

Please cite:

[A Vector Representation of DNA Sequences Using Locality Sensitive Hashing](https://www.biorxiv.org/content/biorxiv/early/2019/08/06/726729.full.pdf)
## License 

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

