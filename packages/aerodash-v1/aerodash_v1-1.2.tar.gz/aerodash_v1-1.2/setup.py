from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='aerodash_v1',
    version='1.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aerodash-v1=aerodash_v1.cli:app',
        ],
    },
    install_requires=[
        "numpy",
        "pandas",
        "typer",
        "requests",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    author='Lokeshwaran Venugopal Balamurugan',
    author_email='lokesh2000.balamurugan@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
