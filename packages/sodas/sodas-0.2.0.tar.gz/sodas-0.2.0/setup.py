from setuptools import setup, find_packages

setup(
    name='sodas',
    version='0.2.0',
    description='Sodas Workflow Development Tools',
    author='ETRI Gyeongryun JEONG',
    author_email='etri32568@etri.re.kr',
    url='',
    packages=find_packages(),
    install_requires=[
        'boto3==1.26.45',
        'pandas',
        'requests',
        'python-dotenv',
    ],
    extras_require={},
    setup_requires=[],
    tests_require=[],
    entry_points={},
    package_data={}
)