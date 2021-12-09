#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE
from pwn import *
from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode

def parse_line(line: bytes):
    qrline = str(line, "utf-8").strip()
    qrline = qrline.replace("\x1b[7m  \x1b[0m", " ")
    qrline = qrline.replace("\x1b[41m  \x1b[0m", "b")
    return qrline

port = sys.argv[1]

c = remote('docker.hackthebox.eu', port)

for _ in range(0, 13):
    #c.recvline()
    print(c.recvline())

qrcode = [c.recvline() for _ in range(0, 51)]
qrcode = [parse_line(l) for l in qrcode]

print("\n".join(qrcode))

img = Image.new('RGB', (len(qrcode[0]),len(qrcode)), 'white')
pixels = img.load()

for y, line in enumerate(qrcode):
    for x, pixel in enumerate(line):
        if qrcode[y][x] == "b":
            pixels[y,x] = (0,0,0)

data = str(decode(img)[0].data, "utf-8").replace(' = ', '').replace('x', '*')
print(data)

output = eval(data)
print(output)

print(c.recvuntil(b'Decoded string: '))

c.sendline(bytes(str(output), 'utf-8'))
c.interactive()
