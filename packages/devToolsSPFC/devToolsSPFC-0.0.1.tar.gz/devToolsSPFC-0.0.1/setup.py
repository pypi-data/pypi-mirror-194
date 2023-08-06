from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'devToolsSPFC'
LONG_DESCRIPTION = 'A package to create long tasks applications such as making calculator,spammer,time etc,in just one line of code.                       Type "import devToolsFCOD".your_variable = devToolsFCOD.MLibrary.            Play around with the module ,it is small and easy to use module ,you can understand easily.                                                         These are the functions spam(),infSpam(),currentTime(),facts() and calculator()'

# Setting up
setup(
    name="devToolsSPFC",
    version=VERSION,
    author="Dev Raj",
    author_email="dev.raj.pandey.7836@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pyautogui", "randfacts", "keyboard"],
    keywords=['python', 'easy-to-use', 'one line code', 'simple', 'Dev Raj'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
# python -m pip install -upgrade twine setuptools
# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
# ;zwX8j4^zmE?Y2y
