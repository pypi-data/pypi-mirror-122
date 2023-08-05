from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='PYTHON_TRANSFORMATIONS',
    version='0.0.1',
    description='A very basic calculator',
    long_description=open('README.rst').read(),
    url='',
    author='Anjana V',
    author_email='anjana.v@bdb.ai',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=[
          'pandas',
        'numpy',
        'logging',
        'hashlib',
        'num2words',
        'datetime',
        'math'
      ]
)