from setuptools import setup


setup(
    name='aiomdht',
    version='0.0.1',
    packages=[
        'aiomdht'
    ],
    url='https://github.com/wolfhechel/aiomdht',
    license='MIT',
    author='Pontus Karlsson',
    author_email='pontus@jensenkarlsson.se',
    description='Mainline DHT protocol implemented in Python 3 with asyncio',
    setup_requires=[
        'pytest-runner',
        'sphinx',
        'flake8'
    ],
    tests_require=[
        'pytest',
        'pytest-describe',
        'pytest-cov',
        'pytest-asyncio'
    ]
)
