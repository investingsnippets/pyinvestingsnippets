import re
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open('pyinvestingsnippets/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

with open('README.md', 'rb') as f:
    content = f.read().decode('utf8')
    long_description = '\n{}'.format(content)


def requirements(filename):
    reqs = list()
    with open(filename, encoding='utf8') as f:
        for line in f.readlines():
            reqs.append(line.strip())
    return reqs


setup(
    name='pyinvestingsnippets',
    version=version,
    author='InvestingSnippets',
    author_email='investingsnippets@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://pyinvestingsnippets.readthedocs.io/',
    packages=find_packages(exclude=['docs', 'tests', 'examples', 'secrets']),
    include_package_data=True,
    test_suite='test.test_suite',
    python_requires='>=3.7',
    install_requires=requirements(filename='requirements.txt'),
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=requirements(filename='requirements-dev.txt'),
    extras_require={
        'tests':requirements(filename='requirements-dev.txt')
    },
    zip_safe=False,
    entry_points={
        'console_scripts': ['pyinvestingsnippets = pyinvestingsnippets.__main__:main']
    },
    license='MIT License',
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries"
    ],
    keywords=', '.join(['investing', 'financial-data']),
    project_urls={
        'Bug Reports': 'https://github.com/investingsnippets/pyinvestingsnippets/issues',
        'Source': 'https://github.com/investingsnippets/pyinvestingsnippets',
        'Documentation': 'https://pyinvestingsnippets.readthedocs.io/'
    },
)
