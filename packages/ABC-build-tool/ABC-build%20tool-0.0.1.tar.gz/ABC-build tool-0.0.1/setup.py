import setuptools 

with open("README.md", "r", encoding="utf-8") as fh: 
  long_description = fh.read() 

setuptools.setup( 
  name="ABC-build tool", 
  version="0.0.1", 
  author="Jason-Kills-U", 
  author_email="guyisntback@gmail.com", 
  description="An easy-to-use yet powerful build system",
  long_description=long_description, 
  long_description_content_type="text/markdown", 
  url="https://replit.com/@jason-kills-u/Testing-testing-again", 
  project_urls={},
  classifiers=[ "Programming Language :: Python :: 3", 
               "License :: OSI Approved :: MIT License", 
               "Operating System :: OS Independent", 
              ], 
  package_dir={"": "abc"}, 
  packages=setuptools.find_packages(where="abc"), 
  python_requires=">=3.6",
)