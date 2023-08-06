from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'Simplified Earth magnetosheath model'
LONG_DESCRIPTION = 'README'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="Mshpy",
        version=VERSION,
        author="Jaewoong Jung",
        author_email="<jjung11@alaska.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/x-rst',
        packages=find_packages(),
        install_requires=[], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
