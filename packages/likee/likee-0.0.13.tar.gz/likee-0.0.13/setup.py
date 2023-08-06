from setuptools import setup, find_packages

# Setting up
setup(
    name="likee",
    version='0.0.13',
    author="Purya Jafari",
    author_email="purya.jafari@hotmail.com",
    description='Python Likee Downloader',
    long_description_content_type="text/markdown",
    long_description='A package that allows to download from like',
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'likee', 'downloader'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)