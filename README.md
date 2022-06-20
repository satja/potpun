# Nadopunitelj - an autocomplete editor

Nadopunitelj is a simple open-source editor, currently supporting English and Croatian word completion.
It suggests up to 10 word completions sorted by word frequencies in a language.
A suggestion is chosen by simply pressing the corresponding key from 0 to 9 - no mouse!

<span>
<img src="https://blogaritam.files.wordpress.com/2022/06/example_en.png" width="450">
<img src="https://blogaritam.files.wordpress.com/2022/06/hr_example.png" width="450">
</span>

Context-based suggestions using neural networks might work better - feel free to contribute!

"Nadopunitelj" is a Croatian word for "the one who completes", while "potpun" (the repository name) means "complete".

## Setup

Nadopunitelj is written in Python 3 using Tkinter.

Use the package manager [pip](https://pip.pypa.io/en/stable) to setup your environment.
Install the requirements for running the app:

```bash
pip install configparser
pip install tk
```

Then, simply run main.py.

## Building Windows installer

Download and install [NSIS](https://nsis.sourceforge.io/Download).

Install PyInstaller:

```bash
pip install pyinstaller
```

To build potpun_installer.exe, run the following commands on Windows:

```bash
pyinstaller potpun.spec
makensis create_installer.nsi
```

## Contribution

Created by Adrian Satja Kurdija in 2022.

If you want to contribute, please make a pull request!
