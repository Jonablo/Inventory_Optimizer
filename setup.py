from setuptools import setup, find_packages

setup(
    name='inventory_optimizer',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scipy>=1.7.0',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0',
        'flask>=2.0.0',
        'requests>=2.25.0',
        'pytest>=6.0.0'
    ],
)
