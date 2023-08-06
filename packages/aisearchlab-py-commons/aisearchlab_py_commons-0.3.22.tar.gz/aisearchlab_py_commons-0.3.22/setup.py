import setuptools

with open('README.md', mode='r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt', mode='r', encoding='utf-8') as f:
    required = f.read().splitlines()

with open('.env', mode='r', encoding='utf-8') as f:
    version = [i.split('=')[-1]
               for i in f.read().splitlines()
               if 'VERSION' in i][0]

setuptools.setup(
    name='aisearchlab_py_commons',
    version=version,
    author='trofiv',
    author_email='stranger.65536@gmail.com',
    description='Some python commons used by python projects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/econtology/py-commons.git',
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
