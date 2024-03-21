from setuptools import setup, find_packages

setup(name='cardano_crystal_ball',
      description=
      """
      predict the price of cardano currency in the next hours and days
      based on a deep learning model.
      """,
      packages=find_packages(include=['cardano_crystal_ball', 'cardano_crystal_ball.*']),
      version="0.0.1",
)
