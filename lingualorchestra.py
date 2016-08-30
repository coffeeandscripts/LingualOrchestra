#!/usr/env/bin python

# Lingual Orchestra
# by coffeeandscripts
# generate music from text
# version 0.0.1

import textinterpret
import MIDI
from statistics import median
import time

title = input("Title: ")
filename = input("Filename: ")
f = open(filename, "r")
text = f.read()
f.close()
key_signature = textinterpret.get_key(title)
key_mode = textinterpret.get_mode(title)
time_signature = textinterpret.get_time_signature(title)

print(title)
print(key_signature)
print(key_mode)
print(time_signature)

scale = textinterpret.get_scale(key_signature, key_mode)

print(scale)

time.sleep(5)

paragraphs = text.split("\n")

para_words = []
sent_words = []

for paragraph in paragraphs:
    words = paragraph.split(" ")
    if len(words) > 1:
        para_words.append(len(words))

med_para_length = median(para_words)

sentences = text.split(".")

for sentence in sentences:
    words = sentence.split(" ")
    if len(words) > 1:
        sent_words.append(len(words))

med_sent_length = median(sent_words)

current_clock = 0

score = [90, [],]

for paragraph in paragraphs:
    para_tempo = textinterpret.get_para_tempo(paragraph, med_para_length)
    prev_tempo = para_tempo
    sentences = paragraph.split(".")
    for sentence in sentences:
        sent_tempo_variation = textinterpret.get_sent_tempo(sentence, med_sent_length)
        sent_no_punc = textinterpret.remove_punctuation(sentence)
        sent_length = len(sentence.replace(" ", ""))
        words = sentence.split(" ")
        letter_counter = 0
        for word in words:
            word_notes_length_sum = 0
            word = textinterpret.remove_punctuation(word)
            if len(word) >= 5:
                chord_notes = textinterpret.get_chord(scale, word, current_clock, sent_tempo_variation)

            for letter in word:
                try:
                    melody_notes = textinterpret.get_note(scale, letter, word,para_tempo, sent_tempo_variation, current_clock, prev_tempo, sent_length, letter_counter)
                    print(melody_notes)
                    score[1].append(melody_notes)
                
                    note_tempo = int(para_tempo * sent_tempo_variation)
                    word_notes_length_sum = word_notes_length_sum + float(melody_notes[1]/note_tempo)
                    current_clock = current_clock + int(melody_notes[2])

                    letter_counter = letter_counter + 1

                except:
                   print(letter)
                   time.sleep(5)

            while word_notes_length_sum > time_signature[0]:
                word_notes_length_sum = word_notes_length_sum - int(time_signature[0]/4)
            
            note_space_length = int(para_tempo * sent_tempo_variation * (time_signature[0]-word_notes_length_sum)*100)/100
            score[1][-1][2] = score[1][-1][2] + note_space_length
            current_clock = current_clock + int(note_space_length)
            print("Hold for " + str(note_space_length))

            if len(word) >= 5:
                chord_hold_length = current_clock - chord_notes[0][1]
                for note in chord_notes:
                    note[2] = int(4*para_tempo*sent_tempo_variation)
                    score[1].append(note)

        prev_tempo = int(para_tempo * sent_tempo_variation)

my_midi = MIDI.score2midi(score)

f = open("my_midi.mid", "wb")
f.write(my_midi)
f.close()
