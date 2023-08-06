from setuptools import setup

from setuptools import setup

with open('README.md', 'rt') as arq:
    readme = arq.read()


keywords = ['html', 'pyhtml', 'myhtml', 'mypyhmtl', '8tml', 'mypyhtml', 'mypy8tml', '']

setup(name='mypy8tml',
      url='https://github.com/MikalROn/MyPy8TML',
      version='0.1.1',
      license='MIT license',
      author='Daniel Coêlho',
      long_description=readme,
      long_description_content_type='text/markdown',
      author_email='heromon.9010@gmail.com',
      keywords=keywords,
      description='A new way to generates html code using class methods in python',
      packages=['mypy_8tml'],
      python_requires='>=3',
      maintainer='Daniel Coêlho',
      maintainer_email='heromon.9010@gmail.com',
      project_urls={
            'Source': 'https://github.com/MikalROn/MyPy8TML',
            'Demos': 'https://github.com/MikalROn/MyPy8TML/tree/main/demos/demo_site'
      }
)