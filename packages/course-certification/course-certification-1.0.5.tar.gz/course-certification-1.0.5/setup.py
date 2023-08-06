from setuptools import setup, find_packages

with open('/Users/cxl/work/course-certification/certification/requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Generate course certificates and\
      keep track of them using Google Spreadsheets API.'

setup(
    name='course-certification',
    version='1.0.5',
    author='CloudxLab',
    author_email='karthik@cloudxlab.com',
    url='https://gitlab.com/karthik49/course-certification',
    description='Generate course certificates from Google Spreadsheets',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'certificate_generator = certification.certificate_generator:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='Certificate generation',
    install_requires=requirements,
    zip_safe=False
)