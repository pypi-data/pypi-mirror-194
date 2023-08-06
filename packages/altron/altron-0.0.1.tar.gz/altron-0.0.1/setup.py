from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "TheAltron"
LONG_DESCRIPTION = "A Package to use Gcast, Stats and Must Join on telegram"


# SETTING UP
setup(
    name="altron",
    version=VERSION,
    author="Axen",
    author_email="thexboy131@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyrogram==1.4.16'],
    keywords=['python', 'pyrogram', 'altron'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
