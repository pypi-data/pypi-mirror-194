from setuptools import setup, find_packages

def get_version(rel_path: str) -> str:
    with open(rel_path) as fp:
        lines = fp.readlines()
    for line in lines:
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

setup(
    name='pbandplot',
    version=get_version("pbandplot/__init__.py"),
    author='kan',
    author_email='luokan@hrbeu.edu.cn',
    python_requires=">=3.6",
    license='MIT',
    license_files=('LICENSE.txt',),
    platforms=['Unix', 'Windows'],
    keywords='phonopy band structure plot',
    description='pbandplot: phonon band structure plot from phonopy result.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/lkccrr/pbandplot',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3 :: Only",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    install_requires=[
        'numpy>=1.22.0',
        'matplotlib>=3.4.0'
    ],
    entry_points={
        'console_scripts': ['pbandplot=pbandplot.wrapper:main']
    },
    packages=find_packages(),
    include_package_data=True
)