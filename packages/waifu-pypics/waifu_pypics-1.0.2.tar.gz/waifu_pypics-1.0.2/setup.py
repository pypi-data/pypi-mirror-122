from setuptools import setup
import re

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ''
with open('waifu_pypics/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(name='waifu_pypics',
      author='Reidy',
      url='https://github.com/This-is-not-Reidy/Waifu-Pypics.git',
      project_urls={
        "Author Discord": "https://discord.com/users/848593011038224405",
      },
      version=version,
      packages=['waifu_pypics'],
      description='A Python wrapper for Waifu-Pics Api',
      long_description=readme,
      long_description_content_type='text/markdown',
      include_package_data=True,
      install_requires=requirements,
      )
