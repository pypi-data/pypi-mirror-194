# Kadota

Tools for working with Figma programmatically

# Working with this repository

For creating and regenerating environment file:
```
conda env create --file env.yaml
conda env export --no-builds | grep -v "^prefix: " > env.yaml
```

For creating requirements file required for pip installability:
```
pip freeze > requirements.txt
```

For building before publishing to pypi:
```
python setup.py sdist bdist_wheel
```

For testing and publishing to pypi:
```
twine check dist/*
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```