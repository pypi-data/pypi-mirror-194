from distutils.core import setup

setup(name='Supbot-api',
        version='0.1',
        description='Supbot is a customer service bot can be integrated with any website',
        author='Supbot L.T.D',
        author_email="yousef.gamal.2951@gmail.com",
        install_requires=['requests', 'torch'],
        packages=['supbot-api'],
        classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],)

