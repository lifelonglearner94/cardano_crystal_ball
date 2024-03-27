from setuptools import setup, find_packages

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='cardano_crystal_ball',
      description=
      """
      predict the price of cardano currency in the next hours and days
      based on a deep learning model.
      """,
      install_requires=requirements,
      packages=find_packages(include=['cardano_crystal_ball', 'cardano_crystal_ball.*']),
      version="0.0.1",
)
