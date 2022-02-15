# Packaging a new release
1. `pip install -r requirements-dev.txt`
2. Bump the version in setup.py
3. `./build.sh`
4. `twine upload --repository testpypi dist/*`
   1. Upload to testpypi to verify packaging will work
5. Once you are confident. This is IRREVERSIBLE `twine upload dist/*`