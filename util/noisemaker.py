"""
### Authors: Dennis Brown, Shannon McDade, Jacob Parmer
###
### Created: Mar 28, 2021
"""

import os
from pydub import AudioSegment
from pydub.generators import WhiteNoise
from pydub.utils import make_chunks


# From https://stackoverflow.com/questions/33720395/can-pydub-set-the-maximum-minimum-volume
def get_loudness(sound, chunk_size = 1000):
    '''
    Loudness = dBFS of the loudest chunk of the sound

    default chunk size = 1 second
    '''
    return max(chunk.dBFS for chunk in make_chunks(sound, chunk_size))


# From https://stackoverflow.com/questions/33720395/can-pydub-set-the-maximum-minimum-volume
def set_loudness(sound, target_dBFS):
    loudness_difference = target_dBFS - get_loudness(sound)
    return sound.apply_gain(loudness_difference)


def test_stuff():
    speech = AudioSegment.from_file('../sandbox/voice_activity_detection/LibriSpeech/test-clean/61/70968/61-70968-0000.flac')
    print('Speech loudness', get_loudness(speech))
    noise = WhiteNoise().to_audio_segment(duration = len(speech))
    print('Noise loudness before', get_loudness(noise))
    noise = set_loudness(noise, -28)
    print('Noise loudness after', get_loudness(noise))
    combined = speech.overlay(noise)
    print('Combined loudness', get_loudness(combined))
    combined.export('derp.flac',  format = 'flac')


def dump_audio_stats_to_CSV(input_folder, output_file):
    lengths = []
    dBFSs = []

    output = open(output_file, 'w')
    output.write('filename,length,loudness\n')

    # Assume subfolder structure:
    # input_foldername / reader ID / chapter ID / FLAC audio files
    # (see LibriSpeech README.TXT)
    _, reader_folders, _ = next(os.walk(input_folder))
    for reader_folder in reader_folders:
        _, chapter_folders, _ = next(os.walk(input_folder + '/' + reader_folder))
        for chapter_folder in chapter_folders:
            _, _, files = next(os.walk(input_folder + '/' + reader_folder + '/' + chapter_folder))
            # print(files)
            for file in files:
                if file.endswith('.flac'):
                    filename = input_folder + '/' + reader_folder + '/' + chapter_folder + '/' + file
                    sound = AudioSegment.from_file(filename)
                    length = len(sound) / 1000.0
                    lengths.append(length)
                    loudness = get_loudness(sound)
                    dBFSs.append(loudness)
                    outstring = filename + ',' + str(length) + ',' + str(loudness)
                    output.write(outstring + '\n')
                    print(outstring)
    print('Average length (s):', sum(lengths) / len(lengths))
    print('Average loudness:', sum(dBFSs) / len(dBFSs))


    output.close()
    return


def add_noise(sound, loudness):
    noise = WhiteNoise().to_audio_segment(duration = len(sound))
    noise = set_loudness(noise, loudness)
    combined = sound.overlay(noise)
    return combined


def make_noisy_files(input_folder, target_noise_loudnesses):
    filenames = []

    # Get all sound filenames relative to the input_folder
    # Assume subfolder structure:
    # input_foldername / reader ID / chapter ID / FLAC audio files
    # (see LibriSpeech README.TXT)
    _, reader_folders, _ = next(os.walk(input_folder))
    for reader_folder in reader_folders:
        _, chapter_folders, _ = next(os.walk(input_folder + '/' + reader_folder))
        for chapter_folder in chapter_folders:
            _, _, files = next(os.walk(input_folder + '/' + reader_folder + '/' + chapter_folder))
            # print(files)
            for file in files:
                if file.endswith('.flac'):
                    filename = reader_folder + '/' + chapter_folder + '/' + file
                    filenames.append(filename)

    # For every file, make new versions with the prescribed level of noise
    count = 0
    for filename in filenames:
        sound = AudioSegment.from_file(input_folder + '/' + filename)
        count += 1
        for loudness in target_noise_loudnesses:
            combined = add_noise(sound, loudness)
            outfile = input_folder + '-db' + str(loudness) + '/' + filename
            directory = os.path.dirname(outfile)
            if not os.path.exists(directory):
                os.makedirs(directory)
            combined = combined.set_frame_rate(16000)
            combined.export(outfile, format = 'flac')
            print(str(count) + ':' + str(loudness))


def main():
    input_folder = '../LibriSpeech/test-clean'
    # dump_audio_stats_to_CSV(input_folder, '../results/audio-stats.csv')
    target_noise_loudnesses = [-160, -80, -40, -20, -10, -5, 0, 5]
    make_noisy_files(input_folder, target_noise_loudnesses)


if __name__ == '__main__':
    main()
