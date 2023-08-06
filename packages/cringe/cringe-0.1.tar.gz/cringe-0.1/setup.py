from setuptools import setup, find_packages


setup(
    name='cringe',
    version='0.1',
    license='MIT',
    author="Tom Kyte",
    author_email='nope@cringe.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/tom-kyte/cringe',
    keywords='cringe',
    install_requires=[
      ],

)
