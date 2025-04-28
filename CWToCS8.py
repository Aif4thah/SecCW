#!/usr/bin/env python

""""
Text to CW for transmit in AM and FM

* Convert text to Morse
* Write IQ in CS8 format

"""

import sys
import numpy

def make_am_samples(amplitude, length_units, frequency=300.0):
    """
    Génère un signal AM avec une fréquence porteuse plus basse pour être plus audible.
    
    :param amplitude: Amplitude du signal
    :param length_units: Durée en unités
    :param frequency: Fréquence porteuse (en Hz)
    :return: Signal AM
    """
    sample_rate = 8000000
    unit_seconds = 0.2

    length_samples = int(round(unit_seconds * length_units * sample_rate))
    t = numpy.arange(length_samples) / sample_rate
    
    # Génération du signal AM avec une fréquence porteuse plus basse
    carrier = amplitude * (1 + 0.5 * numpy.sin(2 * numpy.pi * frequency * t))  # Modulation index = 0.5
    return carrier


def make_fm_samples(amplitude, length_units, carrier_frequency=100000.0, modulation_frequency=1000.0, deviation=75000.0, sample_rate=8000000):
    """
    Génère un signal FM audible avec des variations de fréquence importantes.

    :param amplitude: Amplitude du signal
    :param length_units: Durée en unités
    :param carrier_frequency: Fréquence porteuse (en Hz)
    :param modulation_frequency: Fréquence de modulation (en Hz, le "beep")
    :param deviation: Excursion de fréquence maximale (en Hz)
    :param sample_rate: Taux d'échantillonnage (en Hz)
    :return: Signal FM
    """
    unit_seconds = 0.2  # Durée de base pour chaque unité
    length_samples = int(round(unit_seconds * length_units * sample_rate))
    t = numpy.arange(length_samples) / sample_rate

    # Calcul de la fréquence instantanée avec une grande déviation
    instantaneous_phase = 2 * numpy.pi * carrier_frequency * t + \
                          (deviation / modulation_frequency) * numpy.sin(2 * numpy.pi * modulation_frequency * t)

    # Génération du signal FM
    signal_fm = amplitude * numpy.sin(instantaneous_phase)
    return signal_fm



def convert_to_CW(message, modulation='AM'):
    character_to_symbols_map = {
        'A': '.-','B': '-...','C': '-.-.','D': '-..','E': '.','F': '..-.','G': '--.',
        'H': '....','I': '..','J': '.---','K': '-.-','L': '.-..','M': '--','N': '-.',
        'O': '---','P': '.--.','Q': '--.-','R': '.-.','S': '...','T': '-','U': '..-',
        'V': '...-','W': '.--','X': '-..-','Y': '-.--','Z': '--..',
        '1': '.----','2': '..---','3': '...--','4': '....-','5': '.....',
        '6': '-....','7': '--...','8': '---..','9': '----.','0': '-----',
        ' ': ' ','É': '..-..','.': '.-.-.-',',': '--..--',':': '---...',
        '?': '..--..','!': '-.-.--','\'': '.----.','-': '-....-','|': '-..-.',
        '(': '-.--.-',')': '-.--.-','À':'.--.-','@': '.--.-.',
        '<': '-.-.-', # begin transmission
        '>': '.-.-.' # end transmission
    }

    amplitude = 127
    dot_units = 1
    dash_units = dot_units * 3
    space_internal_units = 1
    space_letters_units = 3
    space_words_units = 7

    if modulation == 'AM':
        make_samples = make_am_samples
    elif modulation == 'FM':
        make_samples = make_fm_samples
    else:
        raise ValueError("Unsupported modulation type")

    baseband_dot = make_samples(1, dot_units)
    baseband_dash = make_samples(1, dash_units)
    baseband_between_symbols = make_samples(0, space_internal_units)
    baseband_between_letters = make_samples(0, space_letters_units - space_internal_units)
    baseband_space = make_samples(0, space_words_units - space_letters_units - space_internal_units)

    symbol_to_baseband_map = {
        '.': baseband_dot,
        '-': baseband_dash,
        ' ': baseband_space,
    }

    # Start with a little silence.
    output = [baseband_space]

    for character in ' < ' + message.upper() + ' > ':  # Add "<" and ">" to respect convention
        symbols = character_to_symbols_map[character]
        for symbol in symbols:
            output.append(symbol_to_baseband_map[symbol])
            output.append(baseband_between_symbols)
        output.append(baseband_between_letters)

    # Append a little extra silence at the end.
    output.append(baseband_space)
    output = numpy.concatenate(output) * amplitude

    return output

def write_toCS8(IQ, file):
    output_int = numpy.empty((len(IQ) * 2,), dtype=numpy.int8)
    output_int[0::2] = numpy.round(IQ.real)
    output_int[1::2] = numpy.round(IQ.imag)
    output_int.tofile(file)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: <script> <message> <output file> <modulation AM|FM>")
        print("\nExemple :")
        print("python ./CWToCS8.py abcdefghijklmnopqrstuvwxyz0123456789 test-abc.cs8 AM")
        sys.exit(0)

    write_toCS8(convert_to_CW(sys.argv[1], sys.argv[3]), sys.argv[2])
