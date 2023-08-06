
from distutils.core import setup
setup(
  name = 'ptmodels',         # How you named your package folder (MyLib)
  packages = ['ptmodels'],   # Chose the same as "name"
  version = '0.0.10',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Pre-trained models image classifier',   # Give a short description about your library
  author = 'MD Rafsun sheikh',                   # Type in your name
  author_email = '201614123@student.mist.ac.bd',      # Type in your E-Mail
  url = 'https://github.com/rafsunsheikh/ptmodels',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/rafsunsheikh/ptmodels/archive/refs/tags/0.0.10.tar.gz',    # I explain this later on
  keywords = ['Image', 'Classification', 'Pre-trained Model'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'tensorflow',
          'sklearn',
          'keras',
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
    'Programming Language :: Python :: 3.10',
  ],
)
