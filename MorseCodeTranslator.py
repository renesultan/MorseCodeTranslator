#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Friday April 15 2022

@author: renesultan
"""

import subprocess
import pyaudio
import wave
import librosa
import matplotlib.pyplot as plt
import librosa.display

CodeMorse = {'A': '.-'   , 'a': '.-'  ,
             'B': '-…'   , 'b': '-…'  ,
             'C': '-.-.' , 'c': '-.-.',
             'D': '-..'  , 'd': '-..' ,
             'E': '.'    , 'e': '.'   ,
             'F': '..-.' , 'f': '..-.',
             'G': '--.'  , 'g': '--.' ,
             'H': '....' , 'h': '....',
             'I': '..'   , 'i': '..'  ,
             'J': '.---' , 'j': '--—' ,
             'K': '-.-'  , 'k': '-.-' ,
             'L': '.-..' , 'l': '.-..',
             'M': '--'   , 'm': '--'  ,
             'N': '-.'   , 'n': '-.'  ,
             'O': '---'  , 'o': '---' ,
             'P': '.--.' , 'p': '.—-.',
             'Q': '--.-' , 'q': '--.-',
             'R': '.-.'  , 'r': '.-.' ,
             'S': '...'  , 's': '...' ,
             'T': '-'    , 't': '-'   ,
             'U': '..-'  , 'u': '..-' ,
             'V': '...-' , 'v': '...-',
             'W': '.--'  , 'w': '.—'  ,
             'X': '-..-' , 'x': '-..-',
             'Y': '-.--' , 'y': '-.--',
             'Z': '--..' , 'z': '--..',
             'CH': '----', 'ch': '----',
             '0': '-----',
             '1': '.----',
             '2': '..---',
             '3': '...--',
             '4': '....-',
             '5': '.....',
             '6': '-....',
             '7': '--...',
             '8': '---..',
             '9': '----.'}

DecodeMorse = {'.-'   : 'a',
               '-...' : 'b',
               '-.-.' : 'c',
               '-..'  : 'd',
               '.'    : 'e',
               '..-.' : 'f',
               '--.'  : 'g',
               '....' : 'h',
               '..'   : 'i',
               '.---' : 'j',
               '-.-'  : 'k',
               '.-..' : 'l',
               '--'   : 'm',
               '-.'   : 'n',
               '---'  : 'o',
               '.--.' : 'p',
               '--.-' : 'q',
               '.-.'  : 'r',
               '...'  : 's',
               '-'    : 't',
               '..-'  : 'u',
               '...-' : 'v',
               '.--'  : 'w',
               '-..-' : 'x',
               '-.--' : 'y',
               '--..' : 'z',
               '----' : 'ch',
               '-----': '0',
               '.----': '1',
               '..---': '2',
               '...--': '3',
               '....-': '4',
               '.....': '5',
               '-....': '6',
               '--...': '7',
               '---..': '8',
               '----.': '9'}

dataset = {"Nature":[1,1,0,0,0],"Dure":[0.1,0.3,0.85,1.75,0.25]
           ,"Class":["dit","dah","silence_lettre","silence_mot","silence_interne"]}

def MorseEcriture(mot_ou_phrase):
    morse_final = ''
    mot = list(mot_ou_phrase)
    i = 0
    while i < len(mot):
        if mot[i] == ' ':
            morse_final = morse_final + ' '
            i = i + 1
        elif mot[i] == "C" or mot[i] == "c":
            if i + 1 < len(mot):
                if mot[i+1]=="H" or mot[i+1] == "h":
                    morse_final += CodeMorse['CH']
                    if i + 1 < len(mot) and mot[i+2] != " ":
                        morse_final = morse_final + '/'
                    i = i + 2
                else:
                    morse_final = morse_final + CodeMorse[mot[i]]
                    if i + 1 < len(mot) and mot[i+1] != " ":
                        morse_final = morse_final + '/'
                    i = i + 1
            else:
                morse_final = morse_final + CodeMorse[mot[i]]
                if i + 1 < len(mot) and mot[i+1] != " ":
                    morse_final = morse_final + '/'
                i = i + 1
        else:
            morse_final = morse_final + CodeMorse[mot[i]]
            if i + 1 < len(mot) and mot[i+1] != " ":
                morse_final = morse_final + '/'
            i = i + 1
    return(morse_final)

def MorseDecode(code):
    to_decode = ''
    result = ''
    for i in range(len(code)):
        if code[i] != '/' and code[i] != ' ':
            to_decode = to_decode + code[i]
        else:
            if code[i] == '/':
                result = result + DecodeMorse[to_decode]
                to_decode = ''
            else:
                result = result + DecodeMorse[to_decode]
                result = result + ' '
                to_decode = ''
    result = result + DecodeMorse[to_decode]
    return result

def MorseSon(mot_ou_phrase):
    print(MorseEcriture(mot_ou_phrase))
    liste_morse=list(MorseEcriture(mot_ou_phrase))
    for elements in liste_morse:
        if elements == ".":
            subprocess.call(["afplay","dit.wav"])
        elif elements == "-":
            subprocess.call(["afplay","dah.wav"])
        elif elements == "/":
            subprocess.call(["afplay","500mill.mp3"])
        elif elements == ' ':
            subprocess.call(["afplay","1sec.mp3"])

def record():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    filename = "temp.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')
    print("Press CTRL + C to stop the recording")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    try:
        while True:
            data = stream.read(chunk)
            frames.append(data)
    except KeyboardInterrupt:
            print("Done recording")
    except Exception as e:
        print(str(e))

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    
    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def distance(row,normalized_input):
    dist = float(abs(dataset['Nature'][row] - normalized_input[0]) 
    + abs(dataset['Dure'][row] - normalized_input[1]))
    return(dist)

def d_liste(normalized_input):
    distance_liste=[]
    for i in range (len(dataset["Nature"])):
        distance_liste = distance_liste + [[distance(i,normalized_input),dataset["Class"][i]]]
    distance_liste.sort(key = lambda distance_liste: distance_liste[0])
    return(distance_liste)

def knn(x_pred,k):
    distance_liste = d_liste(x_pred)
    liste_knn = distance_liste[0:k]
    return(liste_knn[0])
    
def DecodeSon():
    d = {}
    record()
    x , sr = librosa.load("temp.wav")
    plt.figure(figsize=(14, 5))
    librosa.display.waveplot(x, sr=sr)
    for i in range(len(x)):
        x[i] = abs(x[i])
    max_cal = max(x) * 0.25
    num = 0
    ind = 0
    while num < len(x)-2:
        if x[num] <= max_cal:
            ind = ind + 1
            while x[num] <= max_cal and num < len(x)-1:
                if 'silence{0}'.format(ind) in d.keys():
                    d["silence{0}".format(ind)] = d["silence{0}".format(ind)] + [x[num]]
                    num = num + 1
                else:
                    d["silence{0}".format(ind)] = [x[num]]
                    num = num + 1
            if  ind != 1 and len(d["silence{0}".format(ind)]) <= 1000 :
                d["son{0}".format(ind-1)].append(d["silence{0}".format(ind)])
                del(d["silence{0}".format(ind)])
                ind=ind-1
        else:
            ind = ind + 1
            while x[num] > max_cal and num < len(x)-1:
                if "son{0}".format(ind) in d.keys():
                    d["son{0}".format(ind)] = d["son{0}".format(ind)] + [x[num]]
                    num = num + 1
                else:
                    d["son{0}".format(ind)] = [x[num]]
                    num = num + 1
            if  ind % 2 and len(d["son{0}".format(ind)]) <= 1000 :
                d["son{0}".format(ind-1)].append(d["son{0}".format(ind)])
                del(d["son{0}".format(ind)])
                ind=ind-1
    SonAAnalyser = []
    for i in d:
        if i[1] == 'i':
            SonAAnalyser = SonAAnalyser +[[0,len(d[i])*4.5*10**(-5)]]
        else:
            SonAAnalyser = SonAAnalyser +[[1,len(d[i])*4.5*10**(-5)]]
    kl=[]
    for i in SonAAnalyser:
        kl.append(knn(i,1))
    if kl[0][1] == "silence_interne" or kl[0][1] == "silence_lettre" or kl[0][1] == "silence_mot":
        del(kl[0])
    if kl[-1][1] == "silence_interne" or kl[-1][1] == "silence_lettre" or kl[-1][1] == "silence_mot":
        del(kl[-1])
    new_morse = []
    for i in range(len(kl)):
        if kl[i][1] == "dit":
            new_morse.append(".")
        elif kl[i][1] == "dah":
            new_morse.append("-")
        elif kl[i][1] == "silence_lettre":
            new_morse.append("/")
        elif kl[i][1] == "silence_mot":
            new_morse.append(" ")
    code = ''.join(new_morse)
    print(code)
    result = MorseDecode(code)
    return(result)