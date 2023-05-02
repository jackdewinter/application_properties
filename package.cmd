pipenv run pyroma -q -n 10 .

rmdir /s /q dist
rmdir /s /q build
rmdir /s /q application_properties.egg-info

pipenv run python setup.py sdist bdist_wheel

pipenv run twine check dist/*
