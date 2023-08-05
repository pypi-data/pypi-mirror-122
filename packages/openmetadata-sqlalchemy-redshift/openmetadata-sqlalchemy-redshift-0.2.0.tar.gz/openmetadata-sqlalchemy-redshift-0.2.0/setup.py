from setuptools import setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read().replace('.. :changelog:', '')

setup(
    name='openmetadata-sqlalchemy-redshift',
    version='0.2.0',
    url="https://open-metadata.org/",
    author="OpenMetadata Committers",
    license="Apache License 2.0",
    long_description_content_type="text/markdown",
    description='Amazon Redshift Dialect of SqlAlchemy for OpenMetadata',
    long_description=readme + '\n\n' + history,
    packages=['sqlalchemy_redshift', 'redshift_sqlalchemy'],
    package_data={'sqlalchemy_redshift': ['redshift-ca-bundle.crt']},
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'SQLAlchemy>=0.9.2,<2.0.0',
        'packaging',
    ],
    project_urls={
        "Documentation": "https://docs.open-metadata.org/",
        "Source": "https://github.com/open-metadata/sqlalchemy-redshift",
    },
    extras_require={
        ':python_version < "3.4"': 'enum34 >= 1.1.6, < 2.0.0'
    },
    entry_points={
        'sqlalchemy.dialects': [
            'redshift = sqlalchemy_redshift.dialect:RedshiftDialect_psycopg2',
            'redshift.psycopg2 = sqlalchemy_redshift.dialect:RedshiftDialect_psycopg2',
            'redshift.psycopg2cffi = sqlalchemy_redshift.dialect:RedshiftDialect_psycopg2cffi',
            'redshift.redshift_connector = sqlalchemy_redshift.dialect:RedshiftDialect_redshift_connector',
        ]
    },
)
