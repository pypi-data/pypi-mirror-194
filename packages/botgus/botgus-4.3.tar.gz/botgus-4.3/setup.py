from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='botgus',
      version='4.3',
      author='Francisco Alas',
      author_email='admin@botgus.com',
      description='INDICADORES DE BOT GUS / 19 INDICADORES EN PYTHON',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/jrchico/botgus',
      py_modules=['botgus'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      )
