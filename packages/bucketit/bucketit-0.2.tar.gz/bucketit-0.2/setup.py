try:
    from setuptools import find_packages, setup
except ImportError:
    print(
        "Package setuptools is missing from your Python installation. "
        "You can install it by 'pip3 install setuptool' command."
    )
    exit(1)

try:
    from pathlib import Path
except ImportError:
    print(
        "Package pathlib is missing from your Python installation. "
        "You can install it by 'pip3 install pathlib' command."
    )
    exit(1)

project_dir = Path(__file__).parent
long_description = (project_dir / "README.md").read_text()

setup(
    name='bucketit',
    version='0.2',
    license='MIT',
    author="Anton Sazonov",
    description="BucketIt is a CLI tool for uploading files to S3 bucket.",
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages('bucketit'),
    package_dir={'': 'bucketit'},
    url='https://github.com/sazonovanton/BucketIt',
    keywords='BucketIt CLI Tool',
    install_requires=[
          'boto3',
      ],
    entry_points='''
        [console_scripts]
        bucketit=bucketit.bucketit:cli
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],  
)
