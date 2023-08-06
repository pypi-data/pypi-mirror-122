from setuptools import setup, find_packages

def readme():
    with open('Readme.md') as f:
        return f.read()

setup(
    name = 'pastebinfs',
    version = '0.4',
    description = 'Using Pastebin pastes as if they were files',
    long_description = readme(),
    long_description_content_type='text/markdown',
    keywords = 'pastebin file file-like',
    url = 'https://github.com/K0IN/pastebin-as-file',
    author = 'K0IN',
    author_email = 'thisk0in@gmail.com',
    license = 'MIT',
    packages = find_packages(),
    zip_safe = False,
    install_requires = [
        'requests'
    ])