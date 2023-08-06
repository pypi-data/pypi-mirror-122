from setuptools import setup

setup(name='python-gestpay',
      version='0.2.0',
      description='Gestpay WSs2s and WsCryptDecrypt SOAP Client',
      url='https://bitbucket.org/metadonors/python-gestpay',
      author='Fabrizio Arzeni',
      author_email='fabrizio.arzeni@metadonors.it',
      license='MIT',
      packages=['pygestpay'],
      install_requires=[
          'zeep',
          ],
      zip_safe=False)
 