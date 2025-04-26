#!/usr/bin/env python

# Optimized IQ and FFT Signal Analysis

import numpy as np
import pyfftw
import matplotlib.pyplot as plt
import sys
import gc

def read_img_real(input_file):

    print("[*] Reading IQ and real parts...")
    try:
        # Lecture optimisée via numpy.memmap
        data = np.memmap(input_file, dtype=np.int8, mode='r')

        # Les données alternent entre la partie réelle et imaginaire
        real = data[0::2]
        imag = data[1::2]

        # Échantillonnage des données (si trop volumineux)
        step = max(1, len(real) // 2000)  # Limite à 2000 points affichés
        plt.figure(figsize=(10, 6))
        plt.plot(real[::step], label="Partie Réelle (échantillon)", color="blue")
        plt.title("Signal en baseband - Partie Réelle")
        plt.xlabel("Échantillons")
        plt.ylabel("Amplitude")
        plt.legend(loc="upper right")
        plt.grid()
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(imag[::step], label="Partie Imaginaire (échantillon)", color="red")
        plt.title("Signal en baseband - Partie Imaginaire")
        plt.xlabel("Échantillons")
        plt.ylabel("Amplitude")
        plt.legend(loc="upper right")
        plt.grid()
        plt.show()

        # Libération explicite de la mémoire
        del data, real, imag
        gc.collect()

    except FileNotFoundError:
        print(f"file {input_file} not found")
    except Exception as e:
        print(f"Error:\n{str(e)}")


def read_fft(input_file):

    print("[*] FFT...")
    try:
        # Lecture optimisée via numpy.memmap
        data = np.memmap(input_file, dtype=np.int8, mode='r')

        # Les données alternent entre la partie réelle et imaginaire
        real = data[0::2].astype(np.float32)  # Conversion en float32
        imag = data[1::2].astype(np.float32)  # Conversion en float32
        iq_signal = real + 1j * imag

        # Taille optimale pour la FFT
        optimal_size = 2**np.ceil(np.log2(len(iq_signal))).astype(int)
        iq_signal = np.pad(iq_signal, (0, optimal_size - len(iq_signal)), mode='constant')

        # Utilisation de pyFFTW pour accélérer la FFT
        fft_object = pyfftw.builders.fft(iq_signal, threads=4)  # Utilisation de 4 threads
        fft_signal = pyfftw.interfaces.numpy_fft.fftshift(fft_object())
        fft_magnitude = 20 * np.log10(np.abs(fft_signal))

        # Échantillonnage pour l'affichage graphique
        step = max(1, len(fft_magnitude) // 1000)  # Limite à 1000 points affichés
        plt.figure(figsize=(10, 6))
        plt.plot(fft_magnitude[::step], label="Spectre du Signal (FFT)", color="green")
        plt.title("Spectre en Fréquence (FFT)")
        plt.xlabel("Fréquence (échantillons)")
        plt.ylabel("Amplitude (dB)")
        plt.legend(loc="upper right")
        plt.grid()
        plt.show()

        # Libération explicite de la mémoire
        del data, real, imag, iq_signal, fft_signal, fft_magnitude
        gc.collect()

    except FileNotFoundError:
        print(f"file {input_file} not found")
    except Exception as e:
        print(f"Error:\n{str(e)}")


def read_amplitude(input_file, sampling_rate=8000000): #default sample rate = 8000000 (cf. script qui créé le CS8 à transmettre)

    print("[*] Amp vs Time...")
    try:
        # Lecture optimisée via numpy.memmap
        data = np.memmap(input_file, dtype=np.int8, mode='r')

        # Extraction des parties réelle et imaginaire avec conversion
        real = data[0::2].astype(np.float32)  # Conversion en float32 pour compatibilité
        imag = data[1::2].astype(np.float32)
        iq_signal = real + 1j * imag

        # Calcul rapide de l'amplitude complexe
        amplitude = np.abs(iq_signal)

        # Création de l'axe temporel (éviter de calculer un par un)
        time = np.linspace(0, len(amplitude) / sampling_rate, num=len(amplitude))

        # Optimisation de l'affichage avec échantillonnage
        step = max(1, len(amplitude) // 40000)  # Afficher 40000 points maximum
        plt.figure(figsize=(10, 6))
        plt.plot(time[::step], amplitude[::step], label="Amplitude du Signal", color="purple")
        plt.title("Amplitude du Signal en Fonction du Temps")
        plt.xlabel("Temps (s)")
        plt.ylabel("Amplitude")
        plt.legend(loc="upper right")
        plt.grid()
        plt.show()

        # Libération explicite des ressources
        del data, real, imag, iq_signal, amplitude, time
        gc.collect()

    except FileNotFoundError:
        print(f"Fichier introuvable : {input_file}")
    except ValueError:
        print("Erreur de type dans les données. Vérifiez le fichier.")
    except Exception as e:
        print(f"Une erreur est survenue :\n{str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: <script> <input file>")
        sys.exit(0)

    
    read_img_real(sys.argv[1]) 
    read_amplitude(sys.argv[1])
    read_fft(sys.argv[1])
