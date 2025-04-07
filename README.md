[![License: GNU GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Github Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-30363D?&logo=GitHub-Sponsors&logoColor=EA4AAA)](https://github.com/sponsors/Aif4thah/)

# SecCW

Secured Continuous Wave transmission


> 🤝 **Ethical Sponsorship Request** : While this project is open-source and free to use, we kindly ask that if you are using it for commercial purposes or in a business setting, please consider sponsoring the project through GitHub Sponsors. Your support helps maintain and improve the project, ensuring it remains a valuable resource for everyone. Thank you for your understanding and generosity!

> ⚠️ **Disclaimer** : **This is a non-standardized POC at this time. Use it at your own risk.**, I do not guarantee any form of confidentiality or authenticity without further study. This repository and its tools are provided "as is." The author(s) make no representations or warranties, express or implied, regarding the operation of the information, content, materials, tools, services, or products included. The author(s) disclaim, to the full extent permissible by law, all warranties, express or implied, including implied warranties of merchantability and fitness for a particular purpose.


## Quick Demo

To leverage this proof of concept, I suggest using an LNA as an RF amplifier to gain a small amount of power (less than 0.5W). **Ensure compliance with local regulations**.

<p align="center">
    <img src="./HackRF-LaNa-Transmit.jpg" alt="HackRF-Lan" style="width: 800px;" />
</p>

## Transmit

```sh
python ./MsgToCypher.py enc test 9CEA372979FFDCBA028BD523A3F43A44B527DE31E2BBAE56F641D87D3F6C80BC A977EA111934D65E8A6B5AC3D52B82F8
key: 9CEA372979FFDCBA028BD523A3F43A44B527DE31E2BBAE56F641D87D3F6C80BC
iv: A977EA111934D65E8A6B5AC3D52B82F8

# cipher: EFAADCF7EA0A786EF7B4EF7504605970
```


```sh
python ./CWToCS8.py EFAADCF7EA0A786EF7B4EF7504605970 test.cs8
```

<p align="center">
    <img src="./Plot.png" alt="PltBlue" style="width: 600px;" />
</p>

```sh
hackrf_transfer -s 8000000 -x 16 -a 1 -f 40677000 -b 1750000 -t test.cs8
```

## Recieve

* Receive with HackRF or another material like a Talkie-Walkie and Decode Morse

```pyhton
python ./ReadCS8.py ./test.cs8
```

<p align="center">
    <img src="./PlotRed.png" alt="PltRed" style="width: 600px;" />
</p>


* Decrypt

```sh
python ./MsgToCypher.py dec EFAADCF7EA0A786EF7B4EF7504605970 9CEA372979FFDCBA028BD523A3F43A44B527DE31E2BBAE56F641D87D3F6C80BC A977EA111934D65E8A6B5AC3D52B82F8

# message: test
```


## Misc

### Python

* version: 3.13.2.
* Virtual Env: read `requirement.txt`

### HackRF-One

* Binaries: 2024.02.1
* Firmware Version: 2024.02.1

## Go further...

* Read Scripts

* More info about DSP and RF on [Dojo-101](https://github.com/Aif4thah/Dojo-101)

## Credits

* Special thanks to Jared Boone (ShareBrained Technology) for his original script, without him the development would have been much longer !