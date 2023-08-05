from setuptools import setup, find_packages
import codecs
import sys
try:
    # https://stackoverflow.com/questions/30700166/python-open-file-error
    with codecs.open( "README.md", 'r', errors='ignore' ) as file:
        readme_contents = file.read()

except Exception as error:
    readme_contents = ""
    sys.stderr.write( "Warning: Could not open README.md due %s\n" % error )
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='awgp_aadhar_pan_extractor',
  version='0.0.2',
  description='extracts Aadhaar and extracts Pan information',
  long_description=readme_contents,
  long_description_content_type='text/markdown',
  url='',  
  author='Deepak Singh Chauhan',
  author_email='deepaksingh0034602@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='aadhar extracts information', 
  packages=find_packages(),
  install_requires=[''] 
)