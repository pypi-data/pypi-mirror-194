from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'siti/version.py').load_module()


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='aiositi-mex',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Cliente para enviar reportes a la CNBV.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/siti-python',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(cuenca=['py.typed']),
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.24,<2.27',
        'aiohttp>=3.7.0,<3.7.5',
        'pydantic>=1.6.0,<1.9.0',
        'pandas>=1.1.0,<1.4.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
