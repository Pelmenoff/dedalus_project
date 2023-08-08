from setuptools import setup, find_namespace_packages

setup(
    name='personal assistant',
    version='1.1',
    description='Perosanl assistant that works with contacts and notes',
    url='https://github.com/Pelmenoff/dedalus_project',
    authors='Pelmenoff' 'Nikita-devel' 'Victor3637' 'candy-panda-v',
    author_email='victorpiznak@gmail.com' 'brseven90@gmail.com' 'likhachiovvl@gmail.com' 'Titanfall@ukr.net',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['difflib',
                      'datetime',
                      'requests',
                      'subprocess'],
    entry_points=({'console_scripts': ['runbot = dedalus_project.bot:main']})
)
