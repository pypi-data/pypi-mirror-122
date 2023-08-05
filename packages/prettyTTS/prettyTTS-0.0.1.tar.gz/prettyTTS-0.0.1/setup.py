
from setuptools import setup
with open("README.md",'r',encoding='utf-8') as fh:
    long_description = fh.read()
classifiers = [
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Customer Service',
    'Natural Language :: English',
    'Natural Language :: Japanese',
    'Natural Language :: Dutch',
    'Natural Language :: Arabic',
    'Natural Language :: Italian',
    'Natural Language :: Russian',
    'Natural Language :: Spanish',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Multimedia :: Sound/Audio :: Speech',
    'Natural Language :: French',
    'Development Status :: 1 - Planning',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]
keywords = ['tts','prettyTTS','pretty voices','gtts','speech','pyttsx3','freetts','voicemaker','text to pretty speech','ipa','internal phonetic alphabet']

provides = ['IPA','TTS']
setup(
    name='prettyTTS',
    version='0.0.1',
    description='This package has been migrated into mateco',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Joseph Quang',
    author_email='tquang.sdh20@hcmut.edu.vn',
    url='https://github.com/tquangsdh20/mateco',
    package_dir={'':'src'},
    #packages=['mateco'],
    license='MIT',
    include_package_data=True,
    classifiers=classifiers,
    install_requires=['mateco'],
    # extras_require=extras_require,
    keywords=keywords,
    provides=provides,
)
