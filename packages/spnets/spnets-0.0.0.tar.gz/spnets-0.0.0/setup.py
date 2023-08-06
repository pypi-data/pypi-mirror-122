from setuptools import setup, find_packages

setup(
    name='spnets',
    version='0.0.0',
    author='yrqUni',
    keywords=['SA-ConvLSTM', 'PredRNN', 'Spatiotemporal'],
    license='MIT License',
    author_email='yrqUni@gmail.com',
    url='https://github.com/yrqUni',
    description='A spatiotemporal network benchmark.',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'SACL=spnets.SaConvLSTM:hello',
            'STL=spnets.STLSTM:hello'
        ]
    }
)