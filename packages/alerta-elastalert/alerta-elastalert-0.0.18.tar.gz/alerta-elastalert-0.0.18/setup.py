from setuptools import setup, find_packages

#version should be bumbed whenever a new code push required to pypi account
#if not bumped it will give error, version already exists
version = '0.0.18'

setup(
    name="alerta-elastalert",
    version=version,
    description='Alerta webhook for elastalert',
    url='https://github.com/alerta/alerta-contrib',
    license='Apache License 2.0',
    author='Shakti Rao',
    author_email='shakti_rao@affirmednetworks.com',
    packages=find_packages(),
    py_modules=['alerta_elastalert'],
    install_requires=[],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.webhooks': [
          'elastalert = alerta_elastalert:ElastalertWebhook'
        ]
    }
)
