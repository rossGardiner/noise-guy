import argparse
import os
from glob import glob
import librosa
import numpy as np
from scipy.io import wavfile
import random

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        try:
            os.mkdir(string)
            return string
        except:
            raise NotADirectoryError(string)


parser = argparse.ArgumentParser(description='Creates noisey audio data samples')
parser.add_argument('--gtzan', type=dir_path, default='gtzan',
                    help='directory of gtzan clean audio data for noise to be added')
parser.add_argument('--noise', type=dir_path, default='noise-sources',
                    help='directory of noise audio samples for adding to clean data')
parser.add_argument('--out', type=dir_path, default='output',
                    help='output directory')
parser.add_argument('--nr_clean', type=int, help='number of clips to use from each gtzan genre', default=1)
parser.add_argument('--nr_noise', type=int, help='number of noise clips to use', default=10)
parser.add_argument('--rand', type=bool, help='take a random audio file from each genre rather than the first', default=False)
parser.add_argument('--upsample', type=bool, help='upsample the used gtzan files to 44khz', default=True)
parser.add_argument('--noise_gain', type=float, help='gain of noise in generated data, as a fraction of the clean data gain', default=0.7)
args = parser.parse_args()
print(args)

clean_files = []

for dir in glob(args.gtzan + '/*'):
    files = glob(dir + '/*.wav')
    if args.rand:
        random.shuffle(files)
    for file in files[:args.nr_clean]:
        clean_files.append(file)

upsampled_files = []
if args.upsample:
    if not os.path.exists(args.out + '/upsampled'):
        os.makedirs(args.out + '/upsampled')
    for clean in clean_files:
        clean_name = os.path.splitext(os.path.basename(clean))[0]
        clean_data, s = librosa.load(clean)
        print("sample rate of pre-upsampled clean data, {}, {}Hz".format(clean, s))
        resampled = librosa.resample(y=clean_data, orig_sr=s, target_sr=44100)
        resampled *= (1.0 - args.noise_gain)
        filename = args.out + '/upsampled/{}.wav'.format(clean_name)
        upsampled_files.append(filename)
        wavfile.write(filename, 44100, resampled)

noise_files = []
for dir in glob(args.noise + '/*')[:args.nr_noise]:
    file = glob(dir + '/*.wav')[0]
    noise_files.append(file)

output = []
for noise in noise_files:
    noise_name = os.path.splitext(os.path.basename(noise))[0]
    s, noise_data = wavfile.read(noise)
    noise_data = noise_data.astype(np.float32) / (2**16)
    print("name: {} shape: {}".format(noise, noise_data.shape))
    if len(noise_data.shape) >= 2:
        print('invalid noise shape')
        noise_data = np.ravel(noise_data)
        noise_data = np.delete(noise_data, np.arange(0, noise_data.size, 2))
    middle = len(noise_data) // 2
    print("for {}, sample rate :{}, length: {}".format(noise, s, len(noise_data)))

    files = upsampled_files if args.upsample else clean_files
    for clean in files:
        clean_name = os.path.splitext(os.path.basename(clean))[0]
        s, clean_data = wavfile.read(clean)
        print(clean_data.shape)
        clean_data = clean_data.astype(np.float32)

        print("for {}, sample rate :{}, length: {}".format(clean, s, len(clean_data)))

        l = len(clean_data)
        print(l)
        noise_slice = noise_data
        diff = l - len(noise_slice)
        if diff > 0:
            noise_slice = np.pad(noise_data, pad_width=diff//2, mode='edge')
        else:
            noise_slice = noise_slice[middle - l//2: middle + l//2]
        noise_slice *= args.noise_gain
        new_data = clean_data + noise_slice
        if not os.path.exists(args.out + '/noisy'):
            os.makedirs(args.out + '/noisy')
        wavfile.write(args.out + '/noisy/{}-{}.wav'.format(clean_name, noise_name), s, new_data.astype(np.float32))





