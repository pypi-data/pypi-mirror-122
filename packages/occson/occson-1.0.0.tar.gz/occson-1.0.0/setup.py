import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="occson",
  version="1.0.0",
  author="Tomasz Kowalewski",
  author_email="me@tkowalewski.pl",
  maintainer="Tomasz Kowalewski",
  maintainer_email="me@tkowalewski.pl",
  description="Store, manage and deploy configuration securely with Occson.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/occson/occson.py",
  packages=setuptools.find_packages(),
  keywords=['occson'],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ]
)
