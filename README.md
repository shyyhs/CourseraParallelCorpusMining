# Coursera Corpus Mining and Multistage Fine-Tuning for Improving Lectures Translation

## Overview
This repo is for our paper [***Coursera Corpus Mining and Multistage Fine-Tuning for Improving Lectures Translation***](https://www.aclweb.org/anthology/2020.lrec-1.449/).

It contains both the dataset and all source codes in the paper. 

Keywords: Japanese-English parallel dataset, educational domain machine translation, lectures translation, multistage fine-tuning

## Dataset

|       | #lines | #docs | Description                       |
|-------|--------|-------|-----------------------------------|
| Test  | 2005   | 50    | Human-validated                     |
| Dev   | 541    | 16    | Human-validated                     |
| Train | 40770  | 818   | Automatic aligned<br>High quality |

Table 1: English-Japanese parallel dataset in educational domain.


|       | #lines | #docs | Description                       |
|-------|--------|-------|-----------------------------------|
| Test  | 2009   | 90    | Human-validated                     |
| Dev   | 865    | 34    | Human-validated                     |
| Train | 40074  | 997   | Automatic aligned<br>High quality |

Table 2: English-Chinese parallel dataset in educational domain.



It contains high quality English-Japanese (English-Chinese) parallel sentences and documents from site [Coursera](https://coursera.org/). Please refer our paper for details.


## Source code
Also it contain the source codes described in the paper:
1. Crawling multi-language subtitle documents from Coursera using [youtube-dl](https://github.com/ytdl-org).
2. Extracting subtitle files of the desired language pair, data normalization and data clean.
3. Using machine translation and sentence embedding combined with DP to extract parallel sentence pairs in comparable document pairs.
4. Multistage fine-tuning techniques to leverage out-of- and in- domain data to train a MT system for lectures domain translation.

## Experiment results
|       | Ja->En | En->Ja |
|-------|--------|-------|
| Coursera dataset only  | 6.2   | 6.4    |
| Combined with OOD datasets   | 27.5    | 18.5    | 

|       | Zh->En | En->Zh |
|-------|--------|-------|
| Coursera dataset only  | 14.8   | 14.5    |
| Combined with OOD datasets   | 29.5    | 29.1    | 

Table 2: BLEU scores of using only Coursera dataset and combined with [ASPEC](http://orchid.kuee.kyoto-u.ac.jp/ASPEC/), [TED Talks](https://wit3.fbk.eu/mt.php?release=2017-01-ted-test) datasets for Japanese-English and news commentary, TED Talks for Chinese-English with multistage fine-tuning techniques. Please refer our paper for details.

## Reference
Please cite our paper if you used our code or dataset:
```
@inproceedings{song-etal-2020-coursera,
    title = "{C}oursera Corpus Mining and Multistage Fine-Tuning for Improving Lectures Translation",
    author = "Song, Haiyue  and
      Dabre, Raj  and
      Fujita, Atsushi  and
      Kurohashi, Sadao",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.449",
    pages = "3640--3649",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```

## Contact 
If you have any question, please contact song@nlp.ist.i.kyoto-u.ac.jp
