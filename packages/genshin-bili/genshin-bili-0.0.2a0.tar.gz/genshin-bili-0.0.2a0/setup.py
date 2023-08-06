import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="genshin-bili",
    version="0.0.2-alpha",
    author="ConstasJ",
    author_email="2020212726@qq.com",
    description="A Simple Spider and Downloader to download videos from Genshin Impact Offical Bilibili Page",
    long_description_content_type="text/markdown",
    url="https://gitee.com/jerrypaullee/genshin-bili",
    install_requires=[
        'beautifulsoup4',
        'selenium',
        'html5lib',
        'you-get',
        'ffmpy3'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
