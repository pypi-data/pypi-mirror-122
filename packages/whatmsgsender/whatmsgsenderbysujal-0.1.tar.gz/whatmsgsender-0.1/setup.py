import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
  name = 'whatmsgsender',        
  packages = ['whatmsgsender'],  
  version = '0.1',     
  license='MIT',       
  description = 'this module help to sheule whatsapp msg and send on time',   
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'sujal',                   
  author_email = 'sujalchaudhary63@gmail.com',      
  url = 'https://sujalnas.ml',    
  keywords = ['whatsapp', 'whatsapp sheduler', 'whatsapp messenger'],  
  install_requires=[            
          'pyautogui'],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)