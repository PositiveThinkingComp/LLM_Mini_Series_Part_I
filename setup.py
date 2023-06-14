from setuptools import setup, find_packages

setup(
    name='databricks_llm', # name of your package
    version='0.0.1', # version number
    py_modules=['databricks_llm', 'app'], # list all .py files used to build your package
    install_requires=[
        'Click',
    ],
    packages = find_packages(),
    include_package_data=True,
    package_data={"app": ["dbr_api_docs/*.txt", "llm.yaml"]},
    entry_points='''
        [console_scripts]
        databricks_llm=databricks_llm:cli
    ''',
)