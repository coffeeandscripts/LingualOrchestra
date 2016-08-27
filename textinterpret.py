#!/usr/env/bin python

# Opens the text file, has an overview of how to interpret, generates music
# table

all_modes = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian",
    "Aeolian", "Locrian"]

alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"

all_notes = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

def remove_punctuation(word_list):

    punc_list = [".",";","-","'",":","!","?","/","\\",",","#","@","$","&",")","(","\"","’","”"]
    for punc in punc_list:
        word_list= word_list.replace(punc,"")
    
    return word_list

def get_key(title):
    
    all_keys = ["C", "G", "D", "A", "E", "B", "GB", "DB", "AB", "EB", "BB",
    "F"]

    title = remove_punctuation(title)

    sum_of_letters = 0

    for letter in (title.replace(" ", "")):
        sum_of_letters = sum_of_letters + alphabet.index(letter.lower())

    while (sum_of_letters > (len(all_keys) - 1)):
        sum_of_letters = sum_of_letters - len(all_keys)

    key_signature = all_keys[sum_of_letters]

    if sum_of_letters % 2 != 0:
        key_signature = key_signature.lower()

    return key_signature

def get_mode(title):

    title = remove_punctuation(title)

    total_letters = len(title.replace(" ", ""))

    while (total_letters > (len(all_modes) - 1)):
        total_letters = total_letters - len(all_modes)

    key_mode = all_modes[total_letters]

    return key_mode

def get_time_signature(title):

    time_signature = []

    title = remove_punctuation(title)

    sum_of_letters = len(title.replace(" ", ""))

    words_in_title = title.split()

    total_words = len(words_in_title)

    time_signature.append(int(sum_of_letters/total_words))

    if time_signature[0] < 6:
        time_signature.append(4)
    elif time_signature[0] < 10:
        time_signature.append(8)
    elif time_signature[0] < 14:
        time_signature.append(12)
    elif time_signature[0] < 24:
        time_signature.append(16)
    else:
        time_signature.append(32)

    return time_signature

def get_scale(key_signature, key_mode):

    mode_value = all_modes.index(key_mode)

    f = open("key_sig_data", "r")

    key_sig_data_dict = eval(f.read())

    f.close()

    key_scale = key_sig_data_dict[key_signature]

    scale = []

    for n in range(7):
        x = n + mode_value
        if x >= 7:
            x = x - 7
        scale.append(key_scale[x])

    return scale

def get_para_tempo(paragraph, med_para_length):

    words = paragraph.split(" ")
    total_words = len(words)

    tempo = int(total_words/med_para_length * 90)

    return tempo

def get_sent_tempo(sentence):

    words = sentence.split(" ")
    total_words = len(words)

    tempo_variation = total_words/28

    return tempo_variation

def get_note(scale, letter, word, para_tempo, sent_tempo_variation, current_clock, prev_tempo, sent_length, letter_counter):

    note_data = ['note']

    note_lengths = ["2", "1.5", "1", "0.75", "0.5", "0.375", "0.25", "0.125"]

    word_length = len(word) - 1

    if word_length >= len(note_lengths):
        word_length = len(note_lengths) - 1

    note_length = note_lengths[word_length]

    note_value_position = alphabet.index(letter.lower())
    
    octave = 0

    while (note_value_position > (len(scale) - 1)):
        note_value_position = note_value_position - len(scale)
        octave = octave + 1

    note_value = scale[note_value_position]

    note_midi_value = 60 + all_notes.index(note_value) + 12*octave

    tempo_change = prev_tempo - int(para_tempo * sent_tempo_variation)

    if int(letter_counter) < int(int(sent_length) / 4):
        note_tempo = prev_tempo - int((tempo_change / int(sent_length / 4)) * letter_counter)
    else:
        note_tempo = int(para_tempo * (sent_tempo_variation))

    note_duration = int(float(note_length) * note_tempo)

    if note_duration == 0:
        note_duration = 1

    note_data.append(current_clock)     #start time
    note_data.append(note_duration)       #duration
    note_data.append(1)                 #channel
    note_data.append(note_midi_value)        #pitch
    note_data.append(81)        #velocity

    return note_data

def get_chord(scale, word, current_clock):

    chord_data = [['note'], ['note'], ['note']]

    counter = 0
    letter_counter = 0

    while counter < 3:
        
        letter = word[letter_counter]

        note_value_position = alphabet.index(letter.lower())
    
        octave = 0

        while (note_value_position > (len(scale) - 1)):
            note_value_position = note_value_position - len(scale)
            octave = octave + 1

        note_value = scale[note_value_position]

        note_midi_value = 36 + all_notes.index(note_value) - 12*octave

        chord_data[counter].append(current_clock)
        chord_data[counter].append(0)
        chord_data[counter].append(1)
        chord_data[counter].append(note_midi_value)
        chord_data[counter].append(81)

        counter = counter + 1
        letter_counter = letter_counter + 2

    return chord_data
