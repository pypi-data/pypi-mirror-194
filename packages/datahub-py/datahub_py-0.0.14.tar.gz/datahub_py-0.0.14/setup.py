from setuptools import setup, find_packages

from datahub_py import __version__

setup(
    name='datahub_py',
    version=__version__,
    description='Datahub core',

    url='https://github.com/26medias/Datahub-py',
    author='Julien L',
    author_email='julien@leap-forward.ca',

    packages=find_packages(exclude=['tests', 'tests.*']),

    install_requires=[
        'Flask==2.2.2',
        'Flask-RESTful==0.3.9',
        'pika==1.3.1',
        'requests==2.28.1',
        'setuptools==67.4.0',
        'tinydb==4.7.1',
        'tqdm==4.64.1',
        'Werkzeug==2.2.3',
    ],

    classifiers=[
        'Intended Audience :: Developers',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
