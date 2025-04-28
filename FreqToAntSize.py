#!/usr/bin/env python

"""
convert frequancy to wave length

"""

import sys

def get_ant_size(frequency):

    speed_of_light = 299792458  # célérité
    wavelength = speed_of_light / int(frequency)  # calculer la longueur d'onde
    antenna_size = (wavelength / 4) * 100  # pour une antenne quart d'onde et en centimètres

    print(f"λ (m) : {wavelength:.6f}")
    print(f"Ant (cm) : {antenna_size:.6f}")

# Exemple d'utilisation

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: <script> <frequency (Hz)>")
        print("\nExemple :")
        print("python ./FreqToAntSize.py 44600625")
        sys.exit(0)

    get_ant_size(sys.argv[1])
