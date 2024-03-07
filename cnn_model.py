# chess command voice regonisation
import librosa
import os
import numpy as np
from matplotlib import pyplot as plt
from keras import layers, models
from keras.utils import load_img, img_to_array
from sklearn.model_selection import train_test_split





# machine learning
# get data
# voice data for chess commands
# train our model on this data 
# test our model on some test data

# voice recognisation for numbers 
# voice recognisation for letters
# voice recognisation for pieces


# link to feature extraction - https://medium.com/mlearning-ai/handling-audio-data-for-machine-learning-7ba225f183cb
# main feature to extract is mfcc

# mfcc feature data from all these audio files
# TODO: what is mfcc and what is included inside it / DONE
# TODO: download data yourself - http://download.tensorflow.org/data/speech_commands_v0.01.tar.gz / DONE

#Constant that sets the initial file path
TRAINING_DATA_FILE_PATH="training data for numbers/"

def get_file_names_in_folder(data_file_path, data_subdirectories):
    print("getting file names in folder", data_file_path)
    file_names_in_folder = {}

    for subdir in data_subdirectories:
        try: 
            file_path = data_file_path + subdir
            file_names = os.listdir(file_path)
            file_names_in_folder[subdir] = file_names

        except FileNotFoundError as err:
            print(f"folder {subdir} does not exist")

    return file_names_in_folder


def get_wav_file_data(data_file_path, file_names_in_folder):
    wav_file_data = {}

    for subdir in file_names_in_folder.keys():
        print(f"reading data from {subdir} subdirectory ...")
        for file_name in file_names_in_folder[subdir]:
            # Train data/eight/sdfsdf231.wav
            file_path = data_file_path + subdir + "/" + file_name
            signal, sample_rate = librosa.load(file_path)
            signal = librosa.effects.time_stretch(y=signal, rate=len(signal)/sample_rate)
            
            if subdir not in wav_file_data:
                wav_file_data[subdir] = []
            
            wav_file_data[subdir].append((signal, sample_rate))

    return wav_file_data


def extract_mel_spectrograms(wav_file_data):
    for subdir in wav_file_data.keys():
        ix = 0
        for signal, sample_rate in wav_file_data[subdir]:
    
            fig = plt.figure(figsize=[1,1])
            ax = fig.add_subplot(111)
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            ax.set_frame_on(False)
            
            S = librosa.feature.melspectrogram(y=signal, sr=sample_rate, n_fft=2048, hop_length=512)
            librosa.display.specshow(librosa.power_to_db(S, ref=np.max), x_axis='time', y_axis='mel', fmin=50, fmax=280)
            file  = f"mel_spectrograms/{subdir}_{ix}.jpg"
            plt.savefig(file, dpi=500, bbox_inches='tight',pad_inches=0)
            plt.close()
            ix += 1

def process_specotgrams(height,width):
    mels = []
    labels = []
    img_array = []
    
    for file in os.listdir("mel_spectrograms"):
        img_path = os.path.join("mel_spectrograms",file)
        img = load_img(img_path, target_size=(height, width), color_mode='rgb')
        img_array = img_to_array(img) / 255.0
        file_split = file.split('_')
        mels.append(img_array)
        labels.append(file_split[0])
    return np.array(mels), np.array(labels)
    
    
def cnn_model(mel_db, labels, height, width):
    X_train, X_test, Y_train, Y_test = train_test_split(mel_db, labels, test_size=0.2, random_state=42)
    Y_train = np.array([label - 1 for label in Y_train])
    Y_test = np.array([label - 1 for label in Y_test])
    
    model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(height, width, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(8, activation='softmax')])
    
    model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

    # Train the model
    epochs = 10
    model.fit(X_train, Y_train, epochs=epochs, validation_data=(X_test, Y_test))
    model.save("spoken_digits_model_cnn.keras")

    # Evaluate the model
    test_loss, test_acc = model.evaluate(X_test, Y_test)
    print("Test accuracy:", test_acc)
    
    

    

def train_cnn_model(data_subdirectories, label_mapping):
    height, width = 385, 387
    if not os.path.exists("mel_spectrograms"):
        file_names_in_folder = get_file_names_in_folder(TRAINING_DATA_FILE_PATH, data_subdirectories)
        wav_file_data = get_wav_file_data(TRAINING_DATA_FILE_PATH, file_names_in_folder)
        extract_mel_spectrograms(wav_file_data)
    mel_db, labels = process_specotgrams(height,width)
    labels = [label_mapping[label] for label in labels]
    cnn_model(mel_db, labels, height, width)


def main():


    data_subdirectories = ["one","two","three","four","five","six","seven","eight"]
    word_to_number = {"one":1,
                    "two":2,
                    "three":3,
                    "four":4,
                    "five":5,
                    "six":6,
                    "seven":7,
                    "eight":8,
                    "nine":9
                    }
                    
    print(f"training using cnn model")
    train_cnn_model(data_subdirectories, word_to_number)


    # TODO: Country segragration to imporve accuracy. Select country of player. Train the model based on accents used in that country. 
    # TODO: Get google dataset
    # TODO: Make the user speak into the application and train the model on that dataset
    

    # TODO: extract mfcc features from that data

if __name__ == "__main__":
    main()


# get data from alphabets
# make mel spectrograms
# save to a directory
# reconfugure code to get mel spectrograsm from directoy
# train model