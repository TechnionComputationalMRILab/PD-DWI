from pkg_resources import parse_requirements
from setuptools import setup

with open('requirements.txt', 'r') as fp:
    requirements = [str(requirement) for requirement in parse_requirements(fp)]

setup(
    entry_points={
        'console_scripts': [
            'pd-dwi=pd_dwi.scripts.cli:pd_dwi_cli'
        ]
    },
    install_requires=requirements
)
