from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(	
      install_requires=['numpy', 'pandas', ],
      name="conorm",
      version="1.0.0",
      author="Georgy Meshcheryakov",
      author_email="i@georgy.top",
      description="Normalization methods for RNA-seq count data.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      python_requires=">=3.7",
      classifiers=[
              "Programming Language :: Python :: 3.7",
	      "Programming Language :: Python :: 3.8",
	      "Programming Language :: Python :: 3.9",
	      "Programming Language :: Python :: 3.10",
	      "Development Status :: 5 - Production/Stable",
	      "Topic :: Scientific/Engineering",
              "Operating System :: OS Independent"])
