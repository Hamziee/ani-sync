from setuptools import setup, find_packages

setup(
    name="ani-sync",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "ani-sync=ani_sync.main:main",
        ],
    },
    description="Sync your ani-cli progress with a remote server.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='HamzieDev',
    author_email='hamza@heo-systems.net',
    url='https://github.com/Hamziee/ani-sync',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3) ',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
