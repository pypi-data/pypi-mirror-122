from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'armour365'
LONG_DESCRIPTION = 'This is a voicebiometric api to authenticate your voice with gnani VoiceBiometric service'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="armour365",
        version=VERSION,
        author="gnani.ai",
        author_email="<api.service@gnani.ai>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        package_data={'armour365.audio': ['*.wav'], 'armour365': ['*.pem', '*.md','*.log']},
        include_package_data=True,
        install_requires=['requests','pytz'],
        keywords=['python', 'Voicebiometric service'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
