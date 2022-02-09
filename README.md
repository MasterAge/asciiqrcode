# AsciiQrCode
A library for processing ASCII representations of QR Codes.

This is intended to be used for CTFs, but may be used by anyone.

## Setup
```bash
git clone git@github.com:MasterAge/asciiqrcode.git
cd asciiqrcode
pip install -r requirements.txt
```

## Usage
```bash
usage: asciiqrcode.py [-h] [-v] [--dump-qr-code] file

Processes ASCII QR Codes.

positional arguments:
  file            A file containing an ASCII QR code.

optional arguments:
  -h, --help      show this help message and exit
  -v, --verbose   Enable verbose logging.
  --dump-qr-code  Write the created QR code image to disc.

```