# import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

# setuptools.setup(
#     name="example-pkg-YOUR-USERNAME-HERE",
#     version="0.0.1",
#     author="Nimmy Patel",
#     author_email="pateln2021@my.fit.edu",
#     description="Relational Algebra Tool",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/pypa/sampleproject",
#     project_urls={
#         "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
#     },
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     package_dir={"": "src"},
#     packages=setuptools.find_packages(where="src"),
#     python_requires=">=3.6",
# )


from setuptools import setup, find_packages
# import codecs
# import os

VERSION = '0.0.1'
DESCRIPTION = 'Relational Algebra Tool'
LONG_DESCRIPTION = 'Manipulating relational algebra queries'

# Setting up
setup(
    name="Relational_tool",
    version=VERSION,
    author="Nimmy patel",
    author_email="pateln2021@my.fit.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'relational', 'algebra', 'tool', 'nimmypatel'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        # "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)