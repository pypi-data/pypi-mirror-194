# Kadota

Tools for working with Figma programmatically. 

Package page can be found here: https://pypi.org/project/kadota/.

# Working with this repository

For creating and regenerating environment file:
```
conda env create --file env.yaml
conda env export --no-builds | grep -v "^prefix: " > env.yaml
```

For creating requirements file required for pip installability (may need to install pipreqs):
```
pipreqs . --force
```

For deleting old builds:
```
rm build dist -rf
```

For building before publishing to pypi:
```
python setup.py sdist bdist_wheel
```

For testing before publishing to pypi:
```
twine check dist/*
```

For publishing to pypi:
```
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```