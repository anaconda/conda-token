from setuptools import setup
import versioneer

requirements = [
    "anaconda-auth>=0.10.0",
]

setup(
    name='conda-token',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Set repository access token and configure default_channels",
    license="BSD",
    author="Albert DeFusco",
    author_email='adefusco@anaconda.com',
    url='https://github.com/Anaconda/conda-token',
    packages=['conda_token'],
    install_requires=requirements,
    keywords='conda-token',
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
