from setuptools import setup, find_packages

setup(
    name="feamerge",
    version="0.1.0",
    description="Merge Adobe feature files for variable fonts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="mitradranirban",
    url="https://github.com/mitradranirban/feamerge",
    license="GPL-3.0",
    packages=find_packages(),  # assumes __init__.py exists
    python_requires=">=3.8",
    install_requires=[
        "fonttools[ufo]>=4.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Fonts"
    ]
)

