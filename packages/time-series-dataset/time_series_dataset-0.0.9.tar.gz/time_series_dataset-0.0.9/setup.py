from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='time_series_dataset',
    version='0.0.9',
    description='Time series dataset for torch.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='The Unlicense',
    packages=find_packages(exclude=("tests",)),
    author='Daniel Kaminski de Souza',
    author_email='daniel@kryptonunite.com',
    keywords=['Time series dataset'],
    url='https://github.com/krypton-unite/time_series_dataset.git',
    download_url='https://pypi.org/project/time-series-dataset/',
    install_requires = [
        # Use the following for CUDA driver
        # 'torch==1.9.1+cu111',
        # Without CUDA
        'torch'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'pandas',
            'seaborn'
        ],
        'dev': [
            'bumpversion',
            'twine',
            'wheel'
        ]
    }
)