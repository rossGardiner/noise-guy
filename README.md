# Welcome to noise-guy
`noise-guy` is a program to generate audio music with added noise from various sources. By default, the audio sources used are members of the GTZAN dataset which sees popular use in the ML community for genre recognition. This program produces a set of noisy audio files and their original formats; this may be used to benchmark noise cancellation strategies. 

Learn more about GTZAN here: https://www.kaggle.com/andradaolteanu/gtzan-dataset-music-genre-classification

Noise data that we use are taken from the BBC's sound effects library. Learn more about BBC sound effects and usage rights here: https://sound-effects.bbcrewind.co.uk/licensing

## How it works
`noise-guy` will download our audio data and noise data from predetermined Amazon AWS S3 buckets. After this, the noise and audio are mixed using a `python` script. The output is a selection of noisy audio files from a range of music genres. This can be used for further processing.  

## Setup
To setup `noise-guy` you will need to download and unzip our datasets and to configure a `python` virtualenv to run our script. For convenience, a setup script is provided:

```commandline
bash setup.sh
```

## Running
Use our running script to generate the data:
```commandline
bash run.sh
```

Alternatively, `noise-guy` may be run manually:
```commandline
source venv/bin/activate
python3 make-noisy-audio.py
```
After running, a selection of `.wav` files should be accessible in the `./output` directory.

## Other Options
The `make-noisy-audio.py` script has a number of extra options for you to adjust if you would like more control or more data examples. These are accessible as command line arguments to the `make-noisy-audio.py` script:

```commandline
  --gtzan GTZAN        directory of gtzan clean audio data for noise to be added
  --noise NOISE        directory of noise audio samples for adding to clean data
  --out OUT            output directory
  --nr_clean NR_CLEAN  number of clips to use from each gtzan genre
  --nr_noise NR_NOISE  number of noise clips to use
  --rand RAND          take a random audio file from each genre rather than the first
```

