from distutils.core import setup
from mpwatcher.version import __version__

setup(
    name='mpwatcher',
    version=__version__,
    packages=['mpwatcher'],
    install_requires=[
        'pyHook',
        'pygame',
        'pywin32',
        'pyinstaller==3.6'
    ],
    entry_points={
        'console_scripts': [
            'mpwatcher = mpwatcher.__main__:main'
        ]
    },
    url='',
    license='MIT',
    author='tyler',
    author_email='tomorrow@comes.today',
    description='watch keyboard and mouse input and run executor'
)
