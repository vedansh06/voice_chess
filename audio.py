import pyaudio
import wave
from pydub import AudioSegment
from pydub.silence import split_on_silence
import librosa
import numpy as np
import matplotlib.pyplot as plt
import speech_recognition as sr

# takes audio inputs from user and outputs what the audio inputs where
#for the game, need to add a mechanism which confirms what the move of user is after its played without affecting game and give 5 seconds to confirm


def get_audio_input(file_name):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = f"{file_name}.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def split_sound_into_grid_points(file_name):
    sound_file = AudioSegment.from_wav(file_name)
    audio_chunks = split_on_silence(sound_file, min_silence_len=600, silence_thresh=-50)

    for i, chunk in enumerate(audio_chunks):
        out_file = "chunk{0}.wav".format(i)
        print("exporting", out_file)
        chunk.export(out_file, format="wav")


def get_decibals(file_name):
    audio=AudioSegment.from_wav(file_name)
    signal, sr = librosa.load(file_name)
    samples=audio.get_array_of_samples()
    samples_sf=0
    try:
        samples_sf = signal[:, 0]  # use the first channel for dual
    except:
        samples_sf=signal  # for mono


    def convert_to_decibel(arr):
        ref = 1
        if arr!=0:
            return 20 * np.log10(abs(arr) / ref)
            
        else:
            return -60

    data=[convert_to_decibel(i) for i in samples_sf]
    percentile=np.percentile(data,[25,50,75])
    print(f"1st Quartile : {percentile[0]}")
    print(f"2nd Quartile : {percentile[1]}")
    print(f"3rd Quartile : {percentile[2]}")
    print(f"Mean : {np.mean(data)}")
    print(f"Median : {np.median(data)}")
    print(f"Standard Deviation : {np.std(data)}")
    print(f"Variance : {np.var(data)}")


    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(samples)
    plt.xlabel('Samples')
    plt.ylabel('Data: AudioSegment')

    plt.subplot(3, 1, 2)
    plt.plot(samples_sf)
    plt.xlabel('Samples')
    plt.ylabel('Data: Soundfile')
    plt.subplot(3, 1, 3)
    plt.plot(data)
    plt.xlabel('Samples')
    plt.ylabel('dB Full Scale (dB)')
    plt.tight_layout()
    plt.show()


def main():
    r = sr.Recognizer()
    move = ""
    # prompt user for start position
    #print("Say move command slowly")
    # get_audio_input("start_position")
    # get_decibals("start_position.wav")
    
    '''get_audio_input("position")
    split_sound_into_grid_points("position.wav")
    # prompt user for end position

    r.energy_threshold = 1000
    for i in range(2):
        position = sr.AudioFile(f"chunk{i}.wav")

        with position as source: 
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)

        try:
            print("You said: " + r.recognize_google(audio))
            move+=str(r.recognize_google(audio))
        except:
            print("Couldn't process data")
    print(move)'''
        
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration = 2)
        print("*recording")
        audio = r.listen(source, phrase_time_limit = 6)
        print("*done recording")
        return r.recognize_google(audio)

        

 #TODO:   letter1, number1, letter2, number2

 #TODO:   load the trained model/google model and predict from audio data.


