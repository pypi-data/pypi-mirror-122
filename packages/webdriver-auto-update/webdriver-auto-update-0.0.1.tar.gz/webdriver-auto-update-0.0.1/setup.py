from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='webdriver-auto-update',
    version='0.0.1',
    description='Checks local chrome driver version and automatically downloads the latest available version online',
    author='Rony Khong',
    author_email='ronykhong77@gmail.com',
    url='https://github.com/competencytestlvl/webdriver-auto-update',
    py_modules=['webdriver-auto-update'],
    packages=find_packages(),
    package_dir={'': 'src'},
    python_requires='>=3.9',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'selenium',
        'chrome',
        'driver',
        'auto',
        'download',
        'update'],
    install_requires=[
        'requests',
        'wget'],
    )
