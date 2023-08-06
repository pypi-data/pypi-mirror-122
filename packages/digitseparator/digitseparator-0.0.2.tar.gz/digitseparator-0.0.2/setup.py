from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='digitseparator',
    version='0.0.2',
    description='separate digits',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='coldsober irene',
    author_email='nseirene3@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['spacing'],
    packages=find_packages(),
    install_requires=[]
)