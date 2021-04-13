# QUICK START for Voice Activity Detection project

## What's going on here?

We took Filippo Giruzzi's VAD from https://github.com/filippogiruzzi/voice_activity_detection and modified it to work on more than just one hard-coded data set. It uses TensorFlow and is based on tf.estimator. Our modifications to the source code are bracketed with "# initials" and # end initials".

We are only using the LibriSpeech "test-clean" data set from openslr, which is a set of FLAC audio files. It is split into 70% train, 15% validate, 15% test. 

We are using labels provided by the author that indicate, for each audio file, where speech events start and stop.

We added white noise to the test-clean dataset to create additional datasets: test-clean-db-160, test-clean-db-80, etc.

NOTE: The data lives in LibriSpeech/<data set name> and is not in the GitHub repo. 

First, we are training and evaluating the VAD on each dataset. Second, for each trained model created in the first step, we are evalauting it against each of the other datasets, just to see how resilient trained models are to noise levels on which they did not train. 

The code performs 5 main functions:

1. Label data using an exported model provided by the author. We're not doing this, but the code should still work, and has been modified to accept the dataset name as a parameter.

    NOTE: The label data lives in LibriSpeech/labels/<data set name>.

2. Convert the raw data to tfrecords. 

    NOTE: This data lives in LibriSpeech/tfrecords/<data set name>

3. Train using the tfrecords and write the raw model checkpoint data to disk.

4. Export that checkpoint data to a saved model. 

5. Test the saved model on audio data. 

## Steps to get started

0. Reminder: Original author's instructions are at https://github.com/filippogiruzzi/voice_activity_detection (README.md) and also copied below. 

1. Pull repo https://github.com/8bitBrainProject/8BitBrainVADfg

2. Download the the test-clean dataset from https://openslr.org/12/ and put in LibriSpeech as LibriSpeech/test-clean

3. Download the noisy datasets (warning: 11GB) from the Dropbox and extract into LibriSpeech: https://www.dropbox.com/sh/5tmzx8gat67beyz/AABwXXSFKQKwzZV4kGPQ4dsSa/test-clean-but-actually-noisy.zip?dl=0

4. Download the labels for test-clean from this link and put it the json files into LibriSpeech/labels/test-clean: https://drive.google.com/open?id=1ZPQ6wnMhHeE7XP5dqpAEmBAryFzESlin

5. Download the exported model from the same link put its "exported" folder into LibriSpeech/models/pretrainedfg (only needed if we are using it to make more labels) 

6. Your LibriSpeech folder should have these contents:
```
BOOKS.TXT
CHAPTERS.TXT
labels
LICENSE.TXT
models
README.md
README.TXT
SPEAKERS.TXT
test-clean
test-clean-db-10
test-clean-db-160
test-clean-db-20
test-clean-db-40
test-clean-db-5
test-clean-db-80
test-clean-db0
test-clean-db5
tfrecords
```

7. Set up a Python 3.7 environment with the required packages. Notes in the "MISC INSTALL NOTES" file. 

8. I had to set my Windows registry to allow filenames longer than 260 chars. See https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation

9. Command lines to run each step (run from vad folder) (I also put batch files in the scripts folder). **Generally you only want to change the "data_set" parameter to the name of a data folder under LibriSpeech**, plus in the testing step, you can change "model_name" to a different model than the one for the given data_set to implement the second part of our experiment.

    - Step 1: Label: **We probably won't use this** and will just use the labels for test-clean as provided by the author.

    python data_processing/librispeech_label_data.py --data_set test-clean --data_dir ../LibriSpeech/ --out_dir ../LibriSpeech/labels/ --exported_model ../LibriSpeech/models/pretrainedfg/exported     

    - Step 2: Convert raw data to tfrecords. 
    
    python data_processing/data_to_tfrecords.py --data_set test-clean --data_dir ../LibriSpeech/
    
    - Step 3: Train using the tfrecords
    
    python training/train.py --data-set test-clean --data-dir ../LibriSpeech/
    
    - Step 4a: Export the trained model.
    
    python inference/export_model.py --data-set test-clean --model-dir ../LibriSpeech/models/
    
    - Step 4b: Test.
    
    python inference/inference.py --data_set test-clean --model_name test-clean --data_dir ../LibriSpeech/ --smoothing




# ORIGINAL AUTHOR's README for Voice Activity Detection project

Keywords: Python, TensorFlow, Deep Learning, 
Time Series classification

## Table of contents

1. [ Installation ](#1-installation)  
    1.1 [ Basic installation ](#11-basic-installation)  
    1.2 [ Virtual environment installation ](#12-virtual-environment-installation)  
    1.3 [ Docker installation ](#13-docker-installation)
2. [ Introduction ](#2-introduction)  
    2.1 [ Goal ](#21-goal)  
    2.2 [ Results ](#22-results)  
3. [ Project structure ](#3-project-structure)
4. [ Dataset ](#4-dataset)
5. [ Project usage ](#5-project-usage)  
    5.1 [ Dataset automatic labeling ](#51-dataset-automatic-labeling)  
    5.2 [ Record raw data to .tfrecord format ](#52-record-raw-data-to-tfrecord-format)  
    5.3 [ Train a CNN to classify Speech & Noise signals ](#53-train-a-cnn-to-classify-speech--noise-signals)  
    5.4 [ Export trained model & run inference on Test set ](#54-export-trained-model--run-inference-on-test-set)  
6. [ Todo ](#6-todo)
7. [ Resources ](#7-resources)

## 1. Installation

This project was designed for:
* Ubuntu 20.04
* Python 3.7.3
* TensorFlow 1.15.4

```
$ cd /path/to/project/
$ git clone https://github.com/filippogiruzzi/voice_activity_detection.git
$ cd voice_activity_detection/
```

### 1.1 Basic installation

```
$ pip3 install -r requirements.txt
$ pip3 install -e .
```

## 1.2 Virtual environment installation

## 1.3 Docker installation

Build the docker image:
```
$ sudo make build
```
(This might take a while.)

Run the docker image:
```
$ sudo make local
```
(Update `scrips/docker_local.sh` with your personal paths.)

## 2. Introduction

### 2.1 Goal

The purpose of this project is to design and implement 
a real-time Voice Activity Detection algorithm based on Deep Learning.

The designed solution is based on MFCC feature extraction and 
a 1D-Resnet model that classifies whether a audio signal is 
speech or noise.

### 2.2 Results

| Model | Train acc. | Val acc. | Test acc. |
| :---: |:---:| :---:| :---: |
| 1D-Resnet | 99 % | 98 % | 97 % |

Raw and post-processed inference results on a test audio signal are shown below.

![alt text](pics/inference_raw.png "Raw VAD inference")
![alt text](pics/inference_smooth.png "VAD inference with post-processing")

## 3. Project structure

The project `voice_activity_detection/` has the following structure:
* `vad/data_processing/`: raw data labeling, processing, 
recording & visualization
* `vad/training/`: data, input pipeline, model 
& training / evaluation / prediction
* `vad/inference/`: exporting trained model & inference

## 4. Dataset

Please download the LibriSpeech ASR corpus dataset from https://openslr.org/12/, 
and extract all files to : `/path/to/LibriSpeech/`.

The dataset contains approximately 1000 hours of 16kHz read English speech 
from audiobooks, and is well suited for Voice Activity Detection.

I automatically annotated the `test-clean` set of the dataset with a 
pretrained VAD model.

Please feel free to use the `labels/` folder and the pre-trained VAD model (only for inference) from this 
[ link ](https://drive.google.com/open?id=1ZPQ6wnMhHeE7XP5dqpAEmBAryFzESlin).

## 5. Project usage

```
$ cd /path/to/project/voice_activity_detection/vad/
```

### 5.1 Dataset automatic labeling

Skip this subsection if you already have the `labels/` folder, that contains annotations 
from a different pre-trained model.

```
$ python3 data_processing/librispeech_label_data.py --data_dir /path/to/LibriSpeech/test-clean/
                                                    --exported_model /path/to/pretrained/model/
                                                    --out_dir /path/to/LibriSpeech/labels/
```

This will record the annotations into `/path/to/LibriSpeech/labels/` as 
`.json` files.

### 5.2 Record raw data to .tfrecord format

```
$ python3 data_processing/data_to_tfrecords.py --data_dir /path/to/LibriSpeech/
```

This will record the splitted data to `.tfrecord` format in `/path/to/LibriSpeech/tfrecords/`

### 5.3 Train a CNN to classify Speech & Noise signals

```
$ python3 training/train.py --data-dir /path/to/LibriSpeech/tfrecords/
```

### 5.4 Export trained model & run inference on Test set

```
$ python3 inference/export_model.py --model-dir /path/to/trained/model/dir/
                                    --ckpt /path/to/trained/model/dir/
$ python3 inference/inference.py --data_dir /path/to/LibriSpeech/
                                 --exported_model /path/to/exported/model/
                                 --smoothing
```

The trained model will be recorded in `/path/to/LibriSpeech/tfrecords/models/resnet1d/`. 
The exported model will be recorded inside this directory.

## 6. Todo

- [ ] Compare Deep Learning model to a simple baseline
- [ ] Train on full dataset
- [ ] Improve data balancing
- [ ] Add time series data augmentation
- [ ] Study ROC curve & classification threshold
- [ ] Add online inference
- [ ] Evaluate quantitatively post-processing methods on the Test set
- [ ] Add model description & training graphs
- [ ] Add Google Colab demo

## 7. Resources

* _Voice Activity Detection for Voice User Interface_, 
[Medium](https://medium.com/linagoralabs/voice-activity-detection-for-voice-user-interface-2d4bb5600ee3)
* _Deep learning for time series classifcation: a review_,
Fawaz et al., 2018, [Arxiv](https://arxiv.org/abs/1809.04356)
* _Time Series Classification from Scratch 
with Deep Neural Networks: A Strong Baseline_, Wang et al., 2016,
[Arxiv](https://arxiv.org/abs/1611.06455)
