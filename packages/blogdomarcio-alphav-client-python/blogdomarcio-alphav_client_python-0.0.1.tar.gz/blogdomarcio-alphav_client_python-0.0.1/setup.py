from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='blogdomarcio-alphav_client_python',
      version='0.0.1',
      url='https://github.com/blogdomarcio/alphav_client_python',
      license='MIT License',
      author='Claudio Marcio',
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email='blogdomarcio@live.com',
      keywords='Pacote',
      description=u'Consumo de API utilizando a ALPHA VANTAGE',
      packages=['alphav_client_python', 'core'],
      install_requires=['requests', 'python-decouple'],)
