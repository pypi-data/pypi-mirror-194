from setuptools import setup, find_packages

setup(
    name='ocrCommonApi',
    version='0.0.2',
    description='Description.',
    author='testPyPI_1',
    author_email='testPyPI@163.com',
    package_dir={"": "src"},  # 打包目录
    packages=find_packages(where='src')  # 搜索存在__init__.py打包文件夹
    # install_requires=[
    #     'requests',
    #     'importlib-metadata; python_version == "3.8"',
    # ],
)
