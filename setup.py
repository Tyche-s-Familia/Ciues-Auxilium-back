from setuptools import setup

setup(
    name='notpatreon',
    packages=['notpatreon'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-SQLAlchemy',
        'psycopg2',
        'gunicorn',
        'bcrypt'
    ],
)
