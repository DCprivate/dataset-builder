---
dataset_info:
  features:
  - name: instruction
    dtype: string
  - name: input
    dtype: string
  - name: output
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 1991209
    num_examples: 500
  download_size: 1007782
  dataset_size: 1991209
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
