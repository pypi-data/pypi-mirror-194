from setuptools import setup

setup(
    name='funke-enrichment-core',
    version='1.0',
    author='Friedrich Schmidt',
    author_email='friedrich.schmidt@funkemedien.de',
    packages=['funke-enrichment-core'],
    scripts=[],
    license='MIT',
    description='This package contains everthing to orchestrate several microservices in the GCP',
    install_requires=[
        'aiohttp-retry',
        'asyncio',
        'google_cloud_bigquery',
        'pandas',
        'pyarrow',
        'firebase-admin',
        'google-cloud-secret-manager',
        'google-cloud-pubsub'
    ]
)