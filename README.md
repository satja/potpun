# Nadopunitelj - an autocomplete editor

Nadopunitelj is a simple open-source editor, currently supporting English and Croatian word completion.
It suggests up to 10 word completions using word frequencies and word-pair frequencies in a language.
A suggestion is selected by simply pressing the corresponding key from 0 to 9 - no mouse!

<span>
<img src="https://blogaritam.files.wordpress.com/2022/07/en_example.png" width="350">
<img src="https://blogaritam.files.wordpress.com/2022/07/hr_example.png" width="350">
</span>

<em>Nadopunitelj</em> is a Croatian word for "the one who completes", while <em>potpun</em> (the repository name) means "complete".

## Setup

Nadopunitelj is written in Python 3 using Tkinter.

Use the package manager [pip](https://pip.pypa.io/en/stable) to setup your environment.
Install the requirements for running the app:

```bash
pip install configparser
pip install tk
```

Then, simply run [main.py](./main.py).

## Adding a language

Create the list of words and the list of word pairs sorted by frequencies (for example see [croatian.txt](./lang_data/croatian.txt) and [croatian_bigrams.txt](./lang_data/croatian_bigrams.txt))
and convert it to a binary file using [txt2dat.py](./lang_data/txt2dat.py). Then edit [language_menu.py](./language_menu.py).

## Building Windows installer

Download and install [NSIS](https://nsis.sourceforge.io/Download).

Install PyInstaller:

```bash
pip install pyinstaller
```

To build <em>potpun_installer.exe</em>, run the following commands on Windows:

```bash
pyinstaller potpun.spec
makensis create_installer.nsi
```

## Contribution

Created by Adrian Satja Kurdija in 2022.

If you want to contribute, please make a pull request!
