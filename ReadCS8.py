#!/usr/bin/env python

# Read IQ from a CS8 file
# ie:
#  
# python ./ReadCS8.py ./test.cs8
#


import numpy
import matplotlib.pyplot as plt
import sys


def read_iq(input_file):
 
    try:
        # Chargement des données du fichier .cs8
        data = numpy.fromfile(input_file, dtype=numpy.int8)
        
        # Les données alternent entre la partie réelle et la partie imaginaire
        real = data[0::2]
        imag = data[1::2]
        
        # Tracé de la partie réelle
        plt.figure(figsize=(10, 6))
        plt.plot(real, label="Partie Réelle", color="blue")
        plt.title("Signal en baseband - Partie Réelle")
        plt.xlabel("Échantillons")
        plt.ylabel("Amplitude")
        plt.legend(loc="upper right")
        plt.grid()
        plt.show()
        
        # Tracé de la partie imaginaire
        plt.figure(figsize=(10, 6))
        plt.plot(imag, label="Partie Imaginaire", color="red")
        plt.title("Signal en baseband - Partie Imaginaire")
        plt.xlabel("Échantillons")
        plt.ylabel("Amplitude")
        plt.legend(loc="upper right")
        plt.grid()
        plt.show()

    except FileNotFoundError:
        print(f"Le fichier {input_file} est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {str(e)}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: <script> <input file>")
        sys.exit(0)

    read_iq(sys.argv[1])
