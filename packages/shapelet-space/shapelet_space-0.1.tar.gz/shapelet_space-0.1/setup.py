from distutils.core import setup
setup(
  name = 'shapelet_space',         # How you named your package folder (MyLib)
  packages = ['shapelet_space'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  author = 'Ajitesh Srivastava',                   # Type in your name
  author_email = 'your.email@domain.com',      # Type in your E-Mail
  url = 'https://www.ajitesh-srivastava.com/home',   # Provide either the link to your github or to your website
  keywords = ['SHAPELETS', 'FORECAST'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'scipy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)