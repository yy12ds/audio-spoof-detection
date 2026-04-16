# Audio Spoof Detection Web App

## Overview

This project is a web application that detects spoofed audio.

Users can upload an audio file and the system predicts whether the audio is genuine or spoofed.

## Demo

Deployed on Google Cloud:

https://spoofing-audio-detector-app-214049572350.asia-northeast1.run.app

## Model

The detection model is based on a Light CNN architecture designed for audio classification.

Audio signals are converted into mel-spectrogram features and fed into the neural network for classification.


## 概要（日本語）

このプロジェクトはディープラーニングを用いて音声が本物か偽造かを判定するWebアプリケーションです。

音声ファイルをアップロードすると、Light CNNベースのモデルが音声の真偽を判定します。

アプリケーションはDockerでコンテナ化され、Google Cloud Runにデプロイされています。
