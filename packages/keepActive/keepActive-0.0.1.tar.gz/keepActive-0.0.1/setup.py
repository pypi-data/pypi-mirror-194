from setuptools import setup, find_packages

classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    ]

setup(
    name='keepActive',
    version='0.0.1',
    description='Keeps the computer active',
    long_description= open ('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    author='art_bat',
    author_email='art_bat0@icloud.com',
    classifiers= classifiers,
    keywords= ['idle', 'python', 'active'],
    packages=find_packages(),
    install_requires=['pyautogui'],
)