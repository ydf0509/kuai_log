# coding=utf-8
from setuptools import setup, find_packages

filepath = 'README.md'
print(filepath)

setup(
    name='kuai_log',  #
    version="0.4",
    description=(
        "kuai_log is most fast python log"
    ),
    keywords=['logging','log','logger','loguru','nb_log','rotate file'],
    # long_description=open('README.md', 'r',encoding='utf8').read(),
    long_description_content_type="text/markdown",
    long_description=open(filepath, 'r', encoding='utf8').read(),
    # data_files=[filepath],
    author='bfzs',
    author_email='ydf0509@sohu.com',
    maintainer='ydf',
    maintainer_email='ydf0509@sohu.com',
    license='BSD License',
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    url='https://github.com/ydf0509/kuai_log',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=['tzlocal']
)
"""
打包上传
python setup.py sdist upload -r pypi


python setup.py sdist & python -m twine upload dist/kuai_log-0.4.tar.gz


python -m pip install kuai_log --upgrade -i https://pypi.org/simple
"""
