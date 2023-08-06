import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pinyin3k",
    version="0.0.2",
    description="pinyin and TTL for Chinese learning",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Yonghang Wang",
    author_email="wyhang@gmail.com",
    license="Apache 2",
    classifiers=["License :: OSI Approved :: Apache Software License"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["gtts"],
    keywords=[ "pinyin"],
    entry_points={ "console_scripts": 
        [ 
            "pinyin=pinyin:main", 
        ] 
    },
)
