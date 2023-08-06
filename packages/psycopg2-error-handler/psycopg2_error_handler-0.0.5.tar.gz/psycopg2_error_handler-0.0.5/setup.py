from setuptools import setup

setup(
    name="psycopg2_error_handler",
    install_requires=[
        "psycopg2-binary >= 2.9",
    ],
    packages=["psycopg2_error"],
    version='0.0.5',
    description='Psycopg2 Error Handler',
    author='Alexander Lopatin',
    license='MIT',
)
