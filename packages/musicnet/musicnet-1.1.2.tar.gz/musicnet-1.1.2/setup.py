from setuptools import setup, find_packages

setup(name='musicnet',
      version='1.1.2',
      author='SpryGorgon',
      author_email='sprygorgon@mail.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy>=1.19.5', 'pandas>=1.2.4', 'librosa>=0.8.1', 'joblib>=1.0.1', 'scikit-learn>=0.23.2', 'ipython>=7.24.1'
      ],
      include_package_data=True,
      zip_safe=False)