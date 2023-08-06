from setuptools import setup

setup(
    name='funke-enrichment-core',
    version='0.5',
    author='Friedrich Schmidt',
    author_email='friedrich.schmidt@funkemedien.de',
    packages=['funke-enrichment-core'],
    scripts=[],
    license='MIT',
    description='The core modules for a text document enrichment',
    install_requires=[
        'aiohttp-retry',
        'asyncio',
        'google_cloud_bigquery',
        'pandas',
        'pyarrow',
        'pytz',
        'uuid',
        'firebase-admin',
        'google-cloud-secret-manager',
        'google-cloud-pubsub'
    ]
)