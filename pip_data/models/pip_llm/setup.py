from setuptools import setup, find_packages

setup(
    name='pip_llm',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'torch',
        'numpy',
    ],
    include_package_data=True,
    author='Your Name',
    description='Tiny SBC-compatible LLM for Pip',
)
