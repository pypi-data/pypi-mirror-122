from distutils.core import setup
setup(
  name = 'PyROA',         # How you named your package folder (MyLib)
  packages = ['PyROA'],   # Chose the same as "name"
  version = '3.0.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'PyROA is tool to model quasar lightcurves based on a running optimal average that allows inter-lightcurve time delays to be measured using MCMC sampling of the joint posterior parameter distributions.',   # Give a short description about your library
  author = 'Fergus R. Donnan',                   # Type in your name
  author_email = 'frd3@st-andrews.ac.uk',      # Type in your E-Mail
  url = 'https://github.com/FergusDonnan',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/FergusDonnan/PyROA/archive/refs/tags/v3.0.0.tar.gz',   
  keywords = ['methods: data analysis', 'gravitational lensing: strong', 'quasars:genera'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'matplotlib',
          'scipy',
          'emcee',
          'tqdm',
          'tabulate',
          'corner',
          'astropy',
          'numba',
          'SciencePlots',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)

