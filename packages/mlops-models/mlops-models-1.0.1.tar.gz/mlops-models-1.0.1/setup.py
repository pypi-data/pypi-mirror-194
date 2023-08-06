import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mlops-models',
    version='1.0.1',
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["notebooks/*", "data/*", "build*", "dist*"]),
    package_data={'mlops_models' :['mlops_models/resources/models/*']},
    include_package_data=True,
    license='MIT License',  # example license
    description='Service for ...',
    long_description_content_type='text/markdown',
    long_description=README,
    url='https://repo-link.com',
    author='Bostjan Kaluza',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
