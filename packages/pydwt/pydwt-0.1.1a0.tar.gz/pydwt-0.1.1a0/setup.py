# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydwt', 'pydwt.context', 'pydwt.core', 'pydwt.sql']

package_data = \
{'': ['*']}

install_requires = \
['dependency-injector>=4.41.0,<5.0.0',
 'dill>=0.3.6,<0.4.0',
 'matplotlib>=3.6.3,<4.0.0',
 'networkx>=3.0,<4.0',
 'pyyaml>=6.0,<7.0',
 'sqlalchemy>=2.0.1,<3.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pydwt = pydwt.app:app']}

setup_kwargs = {
    'name': 'pydwt',
    'version': '0.1.1a0',
    'description': '',
    'long_description': '# pydwt\n\nThe pydwt library provides a set of tools for orchestrating tasks of data processing in a directed acyclic graph (DAG). This DAG is composed of tasks that have dependencies between them and can be executed in parallel or sequentially, depending on their dependencies.\n\nIn this document, we will provide a brief explanation of the main modules of the pydwt library, which are:\n\n* `session.py`: module for interacting with a database and creating DataFrame objects to manipulate data.\n* `dataframe.py`: module for defining a DataFrame class for working with data.\n* `task.py`: module for defining tasks in the DAG.\n* `dag.py`: module for creating and traversing the DAG.\n* `workflow.py`: module for running the DAG.\n\n\n## Session\nThe `session.py` module is responsible for interacting with a database and creating DataFrame objects to manipulate data. To use this module, you need to create an instance of the Session class, passing an SQLAlchemy engine object and the schema of the database (if it has one). Then, you can use the table method to create a DataFrame object from a table in the database.\n\nHere is an example of how to create a Session object and use the table method to create a DataFrame object:\n\n```python\nfrom sqlalchemy import create_engine\nfrom pydwt.sql.session import Session\n\nengine = create_engine("postgresql://user:password@localhost/dbname")\nsession = Session(engine, schema="my_schema")\n\ndf = session.table("my_table")\n```\n\n## DataFrame\n\nThe `dataframe.py` module defines a DataFrame class for working with data. A DataFrame object is essentially a table with labeled columns and rows. You can use it to perform operations such as selecting, filtering, grouping, and aggregating data.\n\nYou can also materialize a DataFrame as a table or view in the database by calling the materialize method.\n\nHere is an example of how to create a DataFrame object and perform some operations on it:\n\n```python\nfrom pydwt.sql.session import Session\nfrom pydwt.sql.dataframe import DataFrame\n\nsession = Session(engine, schema="my_schema")\n\ndf = session.table("my_table")\n\n# select some columns\ndf = df.select(df.col1, df.col2)\n\n# filter rows based on a condition\ndf = df.where(df.col1 > 10)\n\n# group by a column and aggregate another column\ndf = df.group_by(df.col2, agg={df.col1: (func.sum, "sum_col1")})\n\n# show the resulting DataFrame\ndf.materialize("new_table", as_="table")\n\n```\n## Task\n\nThe `task.py` module defines a Task class for representing a task in the DAG. A Task object has a run method that is responsible for executing the task. You can also define the task\'s dependencies, schedule, and other parameters when creating the object.\n\nTo create a Task object, you can use the `@Task` decorator and define the run method. Here is an example of how to create a Task object:\n\n```python\nfrom pydwt.core.task import Task\n\n@Task()\ndef task_one():\n    df = session.table("features")\n    df = df.with_column("new_column", case((df.preds == "hw", "W")))\n    df.materialize("new_table", as_="table")\n\n\n@Task(depends_on=[task_one])\ndef task_two():\n    df = session.table("new_table")\n    df = df.where((df.new_column == "W"))\n    df = df.with_column("new_column", case((df.preds == "hw", "W")))\n    df.show()\n\n```\n\n## Create a new pydwt project:\n\n`pydwt new <my_project>`\n\nThis command will create a new project with the name "my_project" and the required file structure.\n```\nmy_project/\n    models/\n        example.py\n    dags/\nsettings.yml\n```\n\n* `project_name/models`: where you will put your tasks\n* `project_name/dags/`: where the corresponding dag PNG file will be\n* `project_name/settings.yml`: a configuration file for your project. This file includes the configuration options for your project, such as the path to your data directory.\n\n\n\n## Export the DAG\n\n`pydwt export-dag` \n\nwill export the current state of your dag in the `project_name/dags/` as PNG file with timestamp.\n\n## Run your project\n\n`pydwt run`\n\nwill run the current state of your DAG. It will process the tasks in the DAG by level and parrelise\nit with the `ThreadExecutor`\n\n## Configuration of your pydwt project\n\nThe `settings.yml` file is a configuration file for your pydwt project. It stores various settings such as the project name, database connection details, and DAG tasks.\n\n### connection\nThe connection section contains the configuration details for connecting to the database. The available options are:\n\n* `db`: the name of the database\n* `host`: the hostname or IP address of the database server\n* `user`: the username for the database connection\n* `password`: the password for the database connection\n* `port`: the port number to use for the database connection\n* `sql_alchemy_driver`: the SQLAlchemy driver to use for the database connection\n\n### project\nThe project section contains the project-related settings. The available options are:\n\n`name`: the name of the project\n\n### tasks\nThis section contains the configuration for each task defined in the pydwt project.  \n\nEach task is identified by its name, and the configuration is stored as a dictionary.  \n\nThe dictionary can contain any key-value pairs that the task implementation may need to use, but it must have a key named `materialize`.\n\n* The `materialize` key specifies how the task output should be stored. The value can be either `view` or `table`.\nThe value of the materialize key determines whether the task output should be stored as a SQL view or a SQL table. If the value is view, the output is stored as a SQL view. If the value is table, the output is stored as a SQL table.\n\nEach task implementation can access its configuration by injecting the config argument and specifying Provide[Container.config.tasks.<task_name>]. The injected config argument is a dictionary containing the configuration for the specified task. \n\nexample :\n\n```python\nfrom pydwt.core.task import Task\nfrom dependency_injector.wiring import inject, Provide\nfrom pydwt.core.containers import Container\n\n@Task()\n@inject\ndef task_one(config:dict = Provide[Container.config.tasks.task_one]):\n    print(config)\n\n@Task(depends_on=[task_one])\ndef task_two():\n    print("somme processing")\n```\n### sources\n\nThe sources section contains the database sources that can be used in the project. Each source must have a unique name and specify the schema and table to use for the source.\n## License\nThis project is licensed under GPL.',
    'author': 'gonza',
    'author_email': 'matgonzalez@hotmail.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
