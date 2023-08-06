python3 setup.py sdist bdist_wheel

python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*  --verbose
python3 -m twine upload dist/*  --verbose


python3 -m build
python3 -m twine upload dist/*  --verbose

# kiJM6jdmyqTLJdD