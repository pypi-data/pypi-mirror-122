from distutils.core import setup

setup(
    name='7d_demand_bundles',
    packages=['7d_demand_bundles'],
    version='0.0.0',
    description='My first Python library',
    author='Rafael Zanuto Bianchi',
    license='MIT',
    setup_requires=['nb_black==1.0.7', 'numpy==1.20.0',
                    'openpyxl==3.0.90','pandas==1.3.3',
                    'PuLP==2.5.0']
)
