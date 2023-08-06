from setuptools import setup, Extension
import setuptools


setup(
    name='ExplainAI',
    version='0.0.1',
    author='HuangFeini',
    author_email='386899557@qq.com',
    url='https://github.com/HuangFeini',
    description=u'This integrated XAI tool is designed for interpretation in hydrometeorological forecast.',
    long_description_content_type="text/markdown",
    long_description = '',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[],
    entry_points={
        'console_scripts': [
        ]
    }
)