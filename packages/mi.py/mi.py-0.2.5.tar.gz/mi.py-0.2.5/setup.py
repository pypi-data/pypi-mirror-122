import pathlib

from setuptools import find_packages, setup

description = 'A Python wrapper for the Misskey API'
readme_file = pathlib.Path(__file__).parent/'README.md'
with readme_file.open(encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='mi.py',
    version='0.2.5',
    install_requires=['websockets', 'requests', 'pydantic', 'emoji'],
    url='https://github.com/yupix/mi.py',
    author='yupix',
    author_email='yupi0982@outlook.jp',
    license='MIT',
    python_requires='>=3.9, <4.0',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Natural Language :: Japanese',
        'License :: OSI Approved :: MIT License',
    ]
)
