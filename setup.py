from setuptools import setup, find_packages

setup(
    name='i3QuickLaunch',
    version='0.1.0',
    packages=find_packages(),
    scripts=['launcher.py'],
    entry_points={
        'console_scripts': [
            'i3quicklaunch=launcher:main',
        ],
    },
    install_requires=[
        # List dependencies here. For example:
        'PyGObject',
    ],
    author='gnar Rip',
    author_email='gnar.rip@proton.me',
    description='A lightweight program launcher for i3 window manager on Arch Linux.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gnar-rip/i3QuickLaunch',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
