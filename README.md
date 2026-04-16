# Audio Spoof Detection Web App

## Overview

This project is a web application that detects spoofed audio.

Users can upload an audio file and the system predicts whether the audio is genuine or spoofed.

## 概要（日本語）

このプロジェクトはディープラーニングを用いて音声が本物か偽造かを判定するWebアプリケーションです。

音声ファイルをアップロードすると、Light CNNベースのモデルが音声の真偽を判定します。

アプリケーションはDockerでコンテナ化され、Google Cloud Runにデプロイされています。


## Demo

Deployed on Google Cloud:

https://spoofing-audio-detector-app-214049572350.asia-northeast1.run.app

## Sample Audio

You can test the model using the following files.

- samples/sample_real.flac
- samples/sample_fake.flac

## Model

The detection model is based on a Light CNN architecture designed for audio classification.

Audio signals are converted into mel-spectrogram features and fed into the neural network for classification.


## Dataset

The model was trained using the ASVspoof 2019 dataset.
Specifically, the Logical Access (LA) subset was used for training, validation, and evaluation.
