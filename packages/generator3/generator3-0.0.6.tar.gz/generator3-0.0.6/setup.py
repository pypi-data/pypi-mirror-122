import setuptools

long_description = open('README.md', encoding='utf-8').read()

setuptools.setup(
    name='generator3', 
    url='https://github.com/themysticsavages/generator3',                    
    version='0.0.6',                        
    author='themysticsavages',
    license='MIT',        
    description="Parse Scratch's large project JSONs and convert them to scratchblocks notation",
    long_description=long_description,      
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),    
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],                                      
    python_requires='>=3.6',                 
    install_requires=['requests', 'flask']                    
)