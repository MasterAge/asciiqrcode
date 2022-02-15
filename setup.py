from distutils.core import setup

setup(
  name='asciiqrcode',
  packages=['asciiqrcode'],
  version='1.0',
  license='MIT',
  description='A library for processing ASCII representations of QR Codes.',
  author='Adrian Seddon',
  url='https://github.com/MasterAge',
  download_url='https://github.com/user/reponame/archive/v_01.tar.gz',  # Fix
  keywords=['ASCII', 'QR', 'QRCODE', 'CTF', 'MISC'],
  scripts=['asciiqrcode/asciiqrcode.py'],
  install_requires=[
    'pyzbar',
    'pillow',
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
