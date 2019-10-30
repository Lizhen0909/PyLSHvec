
# LSHVec pre-trained models and its Python bindings 

This project is still in progress. Check it later.

## Summary

This repository presents a few of pre-tained models for [LSHVec](https://github.com/Lizhen0909/LSHVec). 

Python codes and examples to uses these models are also provided. 

## Requirements

1. Python 3.6
2. Jnius >=1.1.0


## Pre-trained model

### refdb viruses classfication model

* model file: [refdb_viruses_model_gs_k23_l3000_rand_model_299](https://www.amazon.com/clouddrive/share/RmoJ1lduzlqstAJFnKg0aAlx82AyCjnzKncfGjQIQMg) [size: 5.3G]

  **md5sum** 2502b284b336734300c2297d23d1d349 

* hash function file: [lsh_nt_NonEukaryota_k23_h25.crp](https://www.amazon.com/clouddrive/share/6ZNvMXMy30b4vc0RYNVG1lbf1ih8WgpoQ9w4lX91IXy)

  **md5sum** 5eea8a98d224b7ff505091bd483ca75c 

## Sample data

* ActinoMock Nanopore Sample [size: 500M].

  The data is used in example notebook [example_use_vectors_in_bacteria_classfication_model.ipynb](notebook/example_use_vectors_in_bacteria_classfication_model.ipynb).
  
  [Download from FSU](http://ww2.cs.fsu.edu/~lshi/ActinoMock_Nanopore.seq.gz)
  &emsp;&emsp;
  [Download from Amazon Drive](https://www.amazon.com/clouddrive/share/eTIKYVLckXUCMnMQSpO8TCqZOwekmBrx23ZhMa3XO8d)
  
  **md5sum**: b7f3e55438fdc05920aee693a98ded2e

## How to run
