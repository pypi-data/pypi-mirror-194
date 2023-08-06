from distutils.core import setup

setup(
    name = 'aggdirect_price_calculator',         # How you named your package folder (MyLib)
    packages = ['aggdirect_price_calculator'],
    version = '0.1',
    description = 'Price Calculator functions',
    author = 'Karan Kadakia',
    author_email = '',
    url = '',   # Provide either the link to your github or to your website
    keywords = ['Price Calculator', 'AGGDIRECT'],   # Keywords that define your package best

    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    ],
)