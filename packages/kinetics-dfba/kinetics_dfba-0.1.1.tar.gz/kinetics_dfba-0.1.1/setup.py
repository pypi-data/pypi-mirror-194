from setuptools import setup, find_packages

setup(
    name = 'kinetics_dfba',
    version = '0.1.1',
    keywords='dfba with kinetics',
    description = 'dfba algorithm with kinetics to simulate metabolic activities of microbiota',
    license = 'MIT License',
    url = 'https://gitee.com/Xu_Billy/d-fba-package',
    author = 'Xu Billy',
    author_email = 'xu_tian@stu.scu.edu.cn',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)
