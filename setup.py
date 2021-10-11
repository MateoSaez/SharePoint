from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='SFTP',
    url='https://github.com/MateoSaez/SharePoint',
    author='Mateo Saez',
    author_email='mateo.saez@outlook.es',
    # Needed to actually package something
    packages=['SharePoint'],
    # Needed for dependencies
    install_requires=['Office365-REST-Python-Client'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Manejar operaciones con SharePoint',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
