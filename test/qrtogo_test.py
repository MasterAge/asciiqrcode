import os
import unittest

from parameterized import parameterized

import asciiqrcode


class MyTestCase(unittest.TestCase):
    digitalcube_soln = "HTB{QR_!snt_d34d}"

    @parameterized.expand([
        ("digitalcube_1.txt", digitalcube_soln),
        ("digitalcube_split.txt", digitalcube_soln),
        ("digitalcube_inverse.txt", digitalcube_soln)
    ])
    def test_qrcode_files(self, file, output):
        data = asciiqrcode.parse_ascii_qrcode("test_files/" + file)
        self.assertEqual(output, data)

    def test_dump_qr_code(self):
        file = "test_files/digitalcube_1.txt"
        asciiqrcode.parse_ascii_qrcode(file, True)

        image = file.replace("txt", "png")
        self.assertTrue(os.path.isfile(image))


if __name__ == '__main__':
    unittest.main()
