<p align="center">
    <img src="./Docs/HackRF-LaNa-Transmit.jpg" alt="HackRF-Lan" style="width: 800px;" />
</p>


[![License: GNU GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Github Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-30363D?&logo=GitHub-Sponsors&logoColor=EA4AAA)](https://github.com/sponsors/Aif4thah/)

# SecCW

Secured Continuous Wave Transmission

> [!WARNING]
> This repository and its tools are provided "as is." The author(s) make no representations or warranties, express or implied, regarding the operation of the information, content, materials, tools, services, or products included. The author(s) disclaim, to the full extent permissible by law, all warranties, express or implied, including implied warranties of merchantability and fitness for a particular purpose.

> [!NOTE]
> While this project is open-source and free to use, we kindly ask that if you are using it for commercial purposes or in a business setting, please consider sponsoring the project through GitHub Sponsors. Your support helps maintain and improve the project, ensuring it remains a valuable resource for everyone. Thank you for your understanding and generosity.


## Proof Of Concept

### Transmit

Generate Key, IVs and encrypt : 

```sh
python ./MsgToCypher.py enc test

# key: 9CEA372979FFDCBA028BD523A3F43A44B527DE31E2BBAE56F641D87D3F6C80BC
# iv: A977EA111934D65E8A6B5AC3D52B82F8
# cipher: EFAADCF7EA0A786EF7B4EF7504605970
```

You can also specify Key and IV : 

```sh
python ./MsgToCypher.py enc test 9CEA372979FFDCBA028BD523A3F43A44B527DE31E2BBAE56F641D87D3F6C80BC A977EA111934D65E8A6B5AC3D52B82F8

# key: 9CEA372979FFDCBA028BD523A3F43A44B527DE31E2BBAE56F641D87D3F6C80BC
# iv: A977EA111934D65E8A6B5AC3D52B82F8
# cipher: EFAADCF7EA0A786EF7B4EF7504605970
```

> [!IMPORTANT]  
> Unlike keys, IVs must not be used more than once. Generate as many IVs as messages.


Convert to CW and write an IQ file :

```sh
python ./CWToCS8.py EFAADCF7EA0A786EF7B4EF7504605970 test-to-transmit.cs8
```

verify real part before sending :

```sh
python ./ReadCS8.py test-to-transmit.cs8
```

![PltRealPart](./Docs/PlotReal.png)

Transmit with SDR (adjust LNA and VGA) :

```sh
hackrf_transfer -s 8000000 -x 47 -g 60 -l 40 -a 1 -f 40677000 -b 1750000 -t .\test-to-transmit.cs8
```


### Receive

> [!TIP]
> The easy way to receive is to use a third party tool such as SDR# or a simple Talkie Walkie.

![Waterfall](./Docs/Waterfall.png)

For further analysis, here is the `HackRF_transfer` command to write the signal in an IQ file (adjust LNA and VGA) :

```sh
hackrf_transfer -s 8000000 -f 40677000 -b 1750000 -a 1 -l 24 -g 12 -r test-recvd.cs8
```

Then we can visualize the Signal :

```sh
python ./ReadCS8.py .\test-recvd.cs8
```

FFT :

![recv](./Docs/test-recvd-FFT.png)


Amplitude over time :

![recv](./Docs/test-recvd-amp-vs-time.png)


Decrypt :

```sh
python ./MsgToCypher.py dec EFAADCF7EA0A786EF7B4EF7504605970 9CEA372979FFDCBA028BD523A3F43A44B527DE31E2BBAE56F641D87D3F6C80BC A977EA111934D65E8A6B5AC3D52B82F8

# message: test
```


### Amplification

To leverage this proof of concept, I suggest using an external LNA as RF amplifier to gain a small amount of power (less than **0.5W to ensure compliance with local regulations.**)

> [!WARNING]
> Using an LNA or other external amplifiers can damage your SDR. Always use a DC blocker.


### Cryptography

**crpyptagraphic keys management is a big deal**. this POC just simplify the [NIST.SP.800-57](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final) Key States :

| States | Short Description |
|-----|-----|
| Pre-activation | Key has been generated but has not been authorized for use |
| Active | Key may be used to cryptographically protect information |
| Compromised | Compromised key shall not be used to apply cryptographic protection to information |
| Destroyed  | Key cannot be recovered by either physical or electronic means |

Simplified Key Management Phases and Functions :

```mermaid
flowchart TD
    P[Pre-Activation]
    A[Active]
    D[Destroyed]
    C[Compromised]

    P --> | Generation | P
    P --> | If not used | D
    P --> | Integrity or Confidentiality suspicion | C
    P --> | Distribution| A
    A --> | After Used | D
    A --> | Integrity or Confidentiality suspicion | C
    C --> | Not allowed or needed | D
```

Simplified key management states and phases :

```mermaid
journey
    title states and phases
    section Pre-Operational Phase
      Generation: 2: Alice
      Distribution: 3: Alice, Bob
    section Operational Phase
      Communication: 6: Alice, Bob
    section Post Operational Phase
      Destruction: 3: Alice,Bob
    section Destroyed phase
      Destroyed: 2: Alice,Bob
```


### Frequencies

Obfuscation is not security, but to avoid detection you can change frequency over time.

```mermaid
gantt
    title Frequencies Plan 
    dateFormat  YYYY-MM-DD
    section Fréquences
    f1 :active, T1, 2025-04-10, 2025-04-20
    f2 :active, T2, 2025-04-01, 2025-04-05
    f3 :active, T3, 2025-04-20, 2025-04-25
    f4 :active, T4, 2025-04-05, 2025-04-10
    f5 :active, T5, 2025-04-25, 2025-05-01
    f6 :active, T6, 2025-05-01, 2025-05-05
```


### Environment

### Python

* version: 3.13.2.
* Virtual Env and dependencies: read `requirement.txt`

### HackRF-One

* Binaries: 2024.02.1
* Firmware Version: 2024.02.1

## Credits

* Special thanks to @jboone [for his original Morse script](https://gist.github.com/jboone/de67df55a2059dcebcdb).
