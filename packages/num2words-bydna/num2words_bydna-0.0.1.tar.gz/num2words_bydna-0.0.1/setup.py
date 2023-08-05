from setuptools import setup, find_packages


setup(
    name='num2word_mydna',
    version='0.6',
    license='MIT',
    author="Beast Boi",
    author_email='beastboigithub89@gmail.com',
    packages=find_packages(
        'C:\\Users\\khara\\Downloads\\example-publish-pypi-main\\example-publish-pypi-main\\src\\num2word_mydna.py'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='first project',
    install_requires=[
        'scikit-learn',
    ],

)
