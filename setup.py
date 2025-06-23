from setuptools import setup, find_packages

setup(
    name='ai-agents-project',
    version='0.1.0',
    author='Vadym Ovcharuk',
    author_email='your.email@example.com',
    description='A project for AI agents with testing functionality',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pytest',
        # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)