from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='junyu',
    version='1.0.4',
    author='Li Weijian',
    author_email='liweijian@junyu.ai',
    description='君禹科技',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=['torch>=1.13.1+cu117', 'numpy>=1.23', 'Pillow>=9.2'],
    python_requires='>=3'
)
