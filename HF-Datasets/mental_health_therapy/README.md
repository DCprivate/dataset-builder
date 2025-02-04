---
dataset_info:
  features:
  - name: instruction
    dtype: string
  - name: input
    dtype: string
  - name: output
    dtype: string
  splits:
  - name: train
    num_bytes: 25479047.04845815
    num_examples: 8580
  - name: test
    num_bytes: 10922136.95154185
    num_examples: 3678
  download_size: 17206567
  dataset_size: 36401184
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: test
    path: data/test-*
language:
- en
license: mit
---


This dataset is a combination of a real-therapy conversation from a conselchat forum and a synthetic discussion generated with chatGpt.

This dataset was obtained from the following repository and cleaned to make it anonymized and remove convo that is not relevant:
1. https://huggingface.co/datasets/nbertagnolli/counsel-chat?row=9
2. https://huggingface.co/datasets/Amod/mental_health_counseling_conversations
3. https://huggingface.co/datasets/ShenLab/MentalChat16K