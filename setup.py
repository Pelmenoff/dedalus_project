from setuptools import setup, find_namespace_packages

setup(
    name='dedalus project',
    version='1.2.4',
    description='Dedalus personal assistant that works with contacts and notes',
    url='https://github.com/Pelmenoff/dedalus_project',
    author='Pelmenoff' 'Nikita-devel' 'Victor3637' 'candy-panda-v',
    author_email='victorpiznak@gmail.com' 'brseven90@gmail.com' 'likhachiovvl@gmail.com' 'Titanfall@ukr.net',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['requests',
                      'phonenumbers'],
    entry_points=({'console_scripts': ['dedalusrun = dedalus_project.bot:main']})
)
