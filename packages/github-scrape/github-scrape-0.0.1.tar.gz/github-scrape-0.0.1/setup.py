from distutils.core import setup

setup(
  name = 'github-scrape',
  packages = ['akinyeleib'],
  version = '0.0.1',
  license='MIT',
  description = 'A program to scrape github followers',
  author = 'Akinyele Ibrahim',
  author_email = 'iakinyele3@gmail.com',
  
  url = 'https://github.com/akinyeleib/github-followers-scrape',

#   download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  
  keywords = ['Github', 'scrape', 'check followers'],
  
  install_requires=[
          'bs4',
          'requests',
          'beautifulsoup4',
      ],

  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],

)

