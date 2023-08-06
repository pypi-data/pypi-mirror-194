import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

from av2 import __version__

setuptools.setup(
    name="pyav2",
    version=__version__,
    author="ponponon",
    author_email="1729303158@qq.com",
    maintainer='ponponon',
    maintainer_email='1729303158@qq.com',
    license='MIT License',
    platforms=["all"],
    description="pyav with typing hint",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ponponon/pyav2",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'av2=av2.cli.main:cli',
        ]
    },
    install_requires=[
        'av',
        'numpy',
        'rich',
        'click',
        'pydantic',
        'pyyaml',
    ],
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
