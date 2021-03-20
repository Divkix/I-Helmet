# I-Helmet

## Installation
<i><b>Note:</b> Made on Windows 10 64 Bit, so dunno if it will work on linux!</i>

### Download

Using Git:

```sh
git clone https://github.com/Divkix/I-Helmet.git
```

or download zip from [Here](https://github.com/Divkix/I-Helmet/archive/master.zip)

### Setting up enviornment

```sh
virtualenv venv
venv\Scripts\activate
```

### Install Requirements:

#### Windows

```sh
pip install -r requirements.txt
```
Now we need to install PyAudio, it cannot be installed automatically in Virtualenv, so we'll need to download and install it manually.

Goto [this site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and download the file corresponding to your python version.

Open up Command Prompt or Windows Terminal and type:

```sh
python --version
```
![Python Version](https://i.imgur.com/AtDXtxY.png)
also check you windows version, 32-bit or 64-bit.

My Setup is Python 3.8.6 and 64-Bit Windows so I will download the `PyAudio‑0.2.11‑cp38‑cp38m‑win_amd64.whl` and install it using the command `pip install PyAudio‑0.2.11‑cp37‑cp37m‑win_amd64.whl`

So, now everything is fixed and the script should work!


### Usage:
```sh
python main.py
```

The script should work now!

Say `help` to check the list of modules.
