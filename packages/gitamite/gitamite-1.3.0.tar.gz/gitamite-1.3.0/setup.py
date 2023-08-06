from setuptools import find_packages, setup

setup(
    name='gitamite',
    packages=['gitamite'],
    version='1.3.0',
    include_package_data=True,
    url='https://github.com/innovation-center-gitam-hyd/gitamite-library',
    description='This is GITAM library for Moodle and Glearn.',
    long_description="""This library can fetch data from Moodle and Glearn like upcoming activities and assignment 
    submissions.""",
    author='Sumanth Perambuduri',
    author_email='sumanthpera3@gmail.com',
    license='MIT',
    install_requires=[
        'requests', 'beautifulsoup4'
    ]
)
