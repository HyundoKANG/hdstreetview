from setuptools import setup

setup(
  name='hdstreetview',
  version='0.1',
  description='Get pictures and timelines of panoramas from Naver Map.'
  url='https://github.com/arawatki97/streetview.git',
  author='Hyundo_Kang',
  author_email='arawatki97@gmail.com',
  license='Hyundo_Kang',
  packages=['hdstreetview'],
  zip_safe=False,
  install_requires=[
    'requests',
    'pandas',
    'PIL',
    'shutil'
    'itertools'
  ]
)
