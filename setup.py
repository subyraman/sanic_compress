from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace("\r", "")
except:
    long_description = ''

setup(
    name='sanic_compress',
    version='0.1.1',
    description='An extension which allows you to easily gzip your Sanic responses.',
    long_description=long_description,
    url='http://github.com/subyraman/sanic_session',
    author='Suby Raman',
    license='MIT',
    packages=['sanic_compress'],
    install_requires=('sanic'),
    zip_safe=False,
    keywords=['sanic', 'gzip'],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Session',
    ]
)
