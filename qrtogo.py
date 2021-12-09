#!/usr/bin/env python3

import argparse
import logging
from PIL import Image
from pyzbar.pyzbar import decode


def to_image(qrcode: list, black_char: str) -> Image:
    """
    Converts an ASCII QR code list to a RGB image.
    :param qrcode: The ASCII QR code.
    :param black_char: The character in the ASCII QR code that represents the black squares.
    :return: A QR code with a white background.
    """
    img = Image.new('RGB', (len(qrcode[0]), len(qrcode)), 'white')
    pixels = img.load()

    for y, line in enumerate(qrcode):
        for x, _ in enumerate(line):
            if qrcode[y][x] == black_char:
                pixels[y, x] = (0, 0, 0)

    return img


def read_file(file, width) -> list:
    """
    Reads an ASCII QR code file into a list of lines.
    :param file: The filename to read from.
    :param width: The width of the QR code in pixels.
    :return: A list of lines.
    """
    with open(file) as f:
        qrcode = f.readlines()

    # If the qr code is not already broken up.
    if len(qrcode[0]) != width:
        # Strip all newlines.
        contents = "".join([line.strip() for line in qrcode])

        if len(contents) % width != 0:
            raise RuntimeError(f"QR code has characters left over after dividing by width ({width}).")

        qrcode = []
        for i in range(0, int(len(contents)/width)):
            start = i * width
            qrcode.append(contents[start:start + width])

    # Extra spaces are needed after second newline to ensure top row of QR code is indented.
    logging.info(f"Read the following QR Code from %s:\n\n  %s\n",
                 file, "\n  ".join(qrcode))

    return qrcode


def parse_ascii_qrcode(file: str, width: int, black: str, dump_qr_code: bool) -> str:
    """
    Retrieves the data from an ASCII QR code.
    :param file: The filename to read from.
    :param width: The width of the QR code in pixels.
    :param black: The character in the ASCII QR code that represents the black squares.
    :param dump_qr_code: Whether to write the QR code image to disk.
    :return: The data stored in the QR code.
    """
    qrcode_chars = read_file(file, width)
    img = to_image(qrcode_chars, black)

    if dump_qr_code:
        filename = file.split(".")[0] + ".png"
        img.save(filename, 'PNG')
        logging.info(f"Wrote QR code to {filename}")

    return str(decode(img)[0].data, "utf-8")


def _parse_args() -> argparse.Namespace:
    """
    Creates an arg parser for QRToGo and parses the supplied args.
    :return: The parsed args.
    """
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


if __name__ == '__main__':
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO if args.verbose else logging.WARNING)

    data = parse_ascii_qrcode(args.file, args.width, args.black, args.dump_qr_code)
    print(f"Data from qr code: \n{data}\n")
