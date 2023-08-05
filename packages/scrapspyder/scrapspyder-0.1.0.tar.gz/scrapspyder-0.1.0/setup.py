from setuptools import setup, find_packages
import scrapspyder

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()



VERSION = scrapspyder.__version__
DESCRIPTION = scrapspyder.__doc__

setup(
    name="scrapspyder",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Mohamed Aliwi",
    author_email="aliwimo@gmail.com",
    license="MIT License",
    packages=find_packages(),
    install_requires=["requests", "beautifulsoup4"],
    url="https://github.com/aliwimo/scrapspyder",
    keywords=["scraper", "scrap", "website scraper", "downloader"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)