from setuptools import setup, find_packages

VERSION = '0.0.11' 
DESCRIPTION = 'Justwicks package'
LONG_DESCRIPTION = 'contains shared features and functionality'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="jwpackage", 
        version=VERSION,
        author="Preetham Puttaswamy",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["PyJWT==2.6.0","fastapi==0.75.0"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'jwpackage'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)