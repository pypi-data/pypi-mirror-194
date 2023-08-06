from setuptools import setup
from flask_cblueprint import __title__, __author__, __author_email__, __version__, __copyright__, __license__


readme = open("./README.md", "r")

setup(
    name=__title__,
    version= __version__,
    author= __author__,
    author_email= __author_email__,
    license= __license__,
    copyright= __copyright__,
    url='https://github.com/Sigurd06/flask-cblueprint/tree/main',
    download_url='https://github.com/Sigurd06/flask-cblueprint/tree/v0.1.0',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    keywords=['Flask'],
    install_requires=[
        "Flask>=1.0.4",
        "Werkzeug>=1.0.1",
    ]
)