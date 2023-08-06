from setuptools import setup



VERSION="0.5.5"


with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wybsel',


    packages = ['wybsel','wybsel.drivers'] ,
    version = VERSION , 
    long_description = long_description , 
    install_requires = ['selenium','selenium-wire'] , 
    package_data = {'' : [r'drivers/*']},
    description = 'Web Browser automation and testing library for python with more features and simpler api than selenium' ,
    author = 'Kwest J. Arcade' ,
    url = 'https://github.com/questjay/wybsel',
    author_email = 'arcadesalmon@gmail.com' ,
    keywords=['wyblsel', 'selenium' , 'autoweb','automate' , 'automation','pyttsx3','bs4' , 'beautiful soup' ,'web' , 'autoweb' , 'auto' , 'pyauto', 'pyautogui'],
    classifiers = [
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'License :: OSI Approved :: MIT License' , 
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'
          ] 

)
