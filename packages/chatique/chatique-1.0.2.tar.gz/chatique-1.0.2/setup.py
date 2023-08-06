from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='chatique',
    packages=['chatique'],
    version='1.0.2',
    license='MIT',
    description='Just something not important',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='lecrkohuty',
    author_email='lecrkohuty@gmail.com',
    url='https://github.com/lecrkohuty/cmes',
    download_url='https://github.com/lecrkohuty/cmes/archive/v_1.0.0.tar.gz',
    keywords=['colab'],
    install_requires=[
        'requests~=2.26.0',
        'coolname'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
