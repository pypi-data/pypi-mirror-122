from distutils.core import setup

setup(
    name='modeldeployer',
    packages=['modeldeployer'],
    version='0.1.7',
    license='apache-2.0',
    description='model deployer',
    author='Ahmet Gürbüz',
    author_email='ahmet.gurbuzz96@gmail.com',
    url='https://github.com/AhmetGurbuzz/model-deployer',
    download_url='https://github.com/AhmetGurbuzz/model-deployer/archive/refs/tags/v0.1.7.tar.gz',
    keywords=['model', 'deployment', 'pickling', 'lambda'],
    install_requires=[
        'cloudpickle'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
