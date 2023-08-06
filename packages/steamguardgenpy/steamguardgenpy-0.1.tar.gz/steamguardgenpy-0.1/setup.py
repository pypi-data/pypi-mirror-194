from setuptools import setup, find_packages

with open('README.md', 'r') as r:
    long_description = r.read()

setup(
    name='steamguardgenpy',
    version=0.1,
    description='Generate steam twofactor (onetime/TOTP) code.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/paradox4280/steamguardgenpy',
    author='paradox4280',
    license='MIT',
    packages=find_packages()
)