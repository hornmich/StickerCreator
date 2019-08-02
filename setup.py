from distutils.core import setup

setup(
    # Application name:
    name="Stickerer",

    # Version number (initial):
    version="0.9",

    # Application author details:
    author="Michal Horn",
    author_email="michal@apartman.cz",

    # Packages
    packages=["consoleApp", "Sticker_creator"],

    # Include additional files into the package
    package_data={'consoleApp': ['*.html', '*.css']},
    include_package_data=True,

    scripts=['consoleApp/CStickerer.py'],
    # Details
    url="https://github.com/hornmich/StickerCreator",

    #
    license="LICENSE.txt",
    description="Console application for creating stickers from e-shop orders.",
    long_description=open("README").read(),

    # Dependent packages (distributions)
    install_requires=[
        "xmltodict",
        "urllib",
        "re",
        "html"
    ],
)