from setuptools import setup

setup(
    name='cloud-workshop-check',
    version='0.1.0',
    description='Check service for cloud workshops',
    author='Pierre Gaxatte',
    author_email='pierre.gaxatte@gmail.com',
    license='BSD 2-clause',
    packages=['cloud-workshop-check'],
    install_requires=[
        'Flask==2.2.2',
        'Flask-RESTful==0.3.9',
        'waitress==2.1.2'
    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
