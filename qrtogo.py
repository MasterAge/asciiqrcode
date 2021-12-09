#!/usr/bin/env python3

import argparse
import logging
from PIL import Image
from pyzbar.pyzbar import decode


def to_image(qrcode: list, black_char: str) -> Image:
    img = Image.new('RGB', (len(qrcode[0]), len(qrcode)), 'white')
    pixels = img.load()

    for y, line in enumerate(qrcode):
        for x, pixel in enumerate(line):
            if qrcode[y][x] == black_char:
                pixels[y, x] = (0, 0, 0)

    return img


def read_file(file, width) -> list:
    with open(file) as f:
        qrcode = f.readlines()

    if len(qrcode[0]) != width:
        contents = "".join([line.strip() for line in qrcode])
        if len(contents) % width != 0:
            raise RuntimeError(f"QR code has characters left over after dividing by width ({width}).")

        qrcode = []
        for i in range(0, int(len(contents)/width)):
            start = i * width
            qrcode.append(contents[start:start + width])

    logging.info(f"Read the following QR Code from {file}:")

    for i in qrcode:
        logging.info("  " + i)

    return qrcode


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="QRToGo", description='Processes ASCII QR Codes.')
    parser.add_argument('-w', '--width', type=int, required=True,
                        help='The width of the QR code, including the whitespace.')
    parser.add_argument('-b', '--black', type=str, default='1',
                        help='The character that represents the black squares')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Enable verbose logging.')
    parser.add_argument('--dump-qr-code', action='store_true', default=False,
                        help='Write the created QR code image to disc.')
    parser.add_argument('file', type=str,
                        help='A file containing an ASCII QR code.')

    return parser.parse_args()


def parse_ascii_qrcode(file: str, width: int, black: str, dump_qr_code: bool) -> str:
    qrcode_chars = read_file(file, width)
    img = to_image(qrcode_chars, black)

    if dump_qr_code:
        filename = file.split(".")[0] + ".png"
        img.save(filename, 'PNG')
        logging.info(f"Wrote QR code to {filename}")

    return str(decode(img)[0].data, "utf-8")


if __name__ == '__main__':
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO if args.verbose else logging.WARNING)

    data = parse_ascii_qrcode(args.file, args.width, args.black, args.dump_qr_code)
    print(f"Data from qr code: \n{data}\n")
