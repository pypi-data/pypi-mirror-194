import os
import sys
from itertools import chain

from setuptools import setup, find_packages


def generate_data_files():
    data_files = []
    data_dirs = (r'src\autoTestScheme\allure',)
    for path, dirs, files in chain.from_iterable(os.walk(data_dir) for data_dir in data_dirs):
        install_dir = os.path.join(sys.prefix, path)
        list_entry = (install_dir, [os.path.join(path, f) for f in files if not f.startswith('.')])
        data_files.append(list_entry)
        print(list_entry)
    return data_files


install_requires = [
    "locust",
    "redis-py-cluster",
    'pluggy==0.13.1',
    "loguru",
    "dingtalkchatbot",
    "allure-pytest",
    "pytest-ordering",
    "pymysql",
    "json_tools",
    "pytest~=6.2.5",
    "pako~=0.3.1",
    "websocket-client",
    "Faker",
    "pycryptodome",
    "dynaconf",
    "selenium",
    "webdriver_manager",
]

packages = find_packages("src")

long_description = "1.allure标签调整为在用例前运行，2.优化request结果在allure的显示"


setup(name='autoTestScheme',
      version='0.2.0.36',
      url='https://gitee.com/xiongrun/auto-test-scheme',
      author='wuxin',
      description='auto test scheme',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author_email='xr18668178362@163.com',
      install_requires=install_requires,
      project_urls={'Bug Tracker': 'https://gitee.com/xiongrun/auto-test-scheme/issues'},
      package_dir={'': 'src'},
      packages=packages,
      include_package_data=True,
      entry_points={'pytest11': ['pytest_autoTestScheme = autoTestScheme']},
      data_files=generate_data_files(),
      package_data={
          'demo': ['demo/*'],
          'autoTestScheme': ['allure'],
      },
      )

# python -m build
# python -m twine upload --repository pypi dist/*
# username = __token__
# password = pypi-AgEIcHlwaS5vcmcCJDkxMTNhMzQ0LWQ4MTEtNDRlMS1hMzdlLWRiYzA3NWUxZWM1ZgACP3sicGVybWlzc2lvbnMiOiB7InByb2plY3RzIjogWyJhdXRvdGVzdHNjaGVtZSJdfSwgInZlcnNpb24iOiAxfQAABiAUU3TYfhRQkBhV196fHm1r6NcHJG6uxf52OGwTARZAOw

# /root/client/interface/auto_test/venv1/bin/python -m pip install --upgrade autoTestScheme
