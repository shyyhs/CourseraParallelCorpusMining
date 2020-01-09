# Coursera Parallel Corpus and Mining

## Overview
This repo is for our paper ***Coursera Corpus Mining and Multistage Fine-Tuning for Improving Lectures Translation*** (Under review).

It contains high quality English-Japanese parallel documents and sentences from OpenCourse site Coursera.

|       | #lines | #docs | Description                       |
|-------|--------|-------|-----------------------------------|
| Test  | 2005   | 50    | Human checked                     |
| Dev   | 541    | 16    | Human checked                     |
| Train | 40770  | 818   | Automatic aligned<br>High quality |


Also it contain the source codes described in the paper:
1. Crawl multi-language subtitle documents from Coursera.
2. Extract subtitle files of the desired language pair along with data normalization and clean from raw data.
3. Use Machine Translation and sentence embedding combined with DP to extract parallel sentence pair in document pairs.
4. Multistage fine-tuning techniques to leverage out-of- and in- domain data to train a MT system for lectures domain translation.

## Others

We will update data of other language pairs and larger dataset later.

## Contact 
If you have any question, please contact song@nlp.ist.i.kyoto-u.ac.jp
