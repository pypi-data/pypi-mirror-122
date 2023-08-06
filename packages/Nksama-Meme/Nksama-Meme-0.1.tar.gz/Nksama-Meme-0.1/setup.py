from distutils.core import setup


setup(
  name = 'Nksama-Meme',         
  packages = ['Nksama-Meme'],   
  version = '0.1',      
  license='MIT',    
  description = 'Random Memes from reddit',   
  author = 'Nksama',                 
  author_email = 'nksama@protonmail.com',      
  url = 'https://github.com/Nksama',   
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    
  keywords = ['Meme', 'Reddit', 'Api'],   
  install_requires=[            
          'requests',

      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)