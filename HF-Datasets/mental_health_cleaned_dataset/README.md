---
dataset_info:
  features:
  - name: client
    dtype: string
  - name: therapist
    dtype: string
  - name: category
    dtype: string
  splits:
  - name: train
    num_bytes: 16166708.30689905
    num_examples: 16426
  - name: test
    num_bytes: 6929854.693100951
    num_examples: 7041
  download_size: 11528028
  dataset_size: 23096563.0
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: test
    path: data/test-*
---
