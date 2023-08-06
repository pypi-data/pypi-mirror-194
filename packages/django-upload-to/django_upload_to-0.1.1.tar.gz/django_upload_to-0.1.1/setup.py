# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['upload_to']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.0']

setup_kwargs = {
    'name': 'django-upload-to',
    'version': '0.1.1',
    'description': 'It generates dynamically a directory path and a file name for Django FileField',
    'long_description': '# django-upload-to\n\n[![codecov](https://codecov.io/github/valbertovc/django-upload-to/branch/main/graph/badge.svg?token=2R5S5GTS0X)](https://codecov.io/github/valbertovc/django-upload-to)\n\nIt generates dynamically a directory path and a secure file name for Django FileField.\n\nMain options:\n- Ready to use generators.\n- Generate secure file name without especial characters.\n- Generate file name using a uuid value.\n- Dynamically generate paths from the model instance.\n- Generate paths using Python datetime formats.\n\n## Get started\nInstall the django-upload-to in your virtual environment\n```bash\n$ pip install django-upload-to\n```\nImport it in your models file and add it as a `upload_to` argument in the `FileField` \n```python\n# my_app/models.py\nfrom upload_to import UploadTo\nfrom django.db import models\n\n\nclass MyModel(models.Model):\n    attachment = models.FileField(upload_to=UploadTo("attachments"))\n```\nThe path and file name generated will be like this:\n```text\n"attachments/the-file-name-uploaded.pdf"\n```\n\n## How to use the ready-to-use classes\n\nConsider the scenario below:\n```python\nimport upload_to\nfrom django.db import models\n\n\nclass MyUser(models.Model):\n    username = models.CharField(...)\n    avatar = models.FileField(upload_to=<generator>)\n\ninstance = MyUser(username=\'user@email.com\')\n```\nReplace the `<generator>` fragment by the generators as showed below:\n#### File in root folder\n```python\n>>> generator = upload_to.UploadTo()\n>>> generator(instance, "file.pdf")\n"file.pdf"\n\n```\n#### Define a folder structure\n```python\n>>> generator = upload_to.UploadTo(prefix=["files", "documents"])\n>>> generator(instance, "file.pdf")\n"files/documents/file.pdf"\n```\n#### Generate a folder name using datetime formats from Python\n```python\n>>> generator = upload_to.UploadTo(prefix=["pictures", "%Y"])\n>>> generator(instance, "file.png")\n"pictures/2023/file.png"\n```\n#### Replace the file name by an hexadecimal uuid value\n```python\n# 4. replace file name by a uuid value\n>>> generator = upload_to.UuidUploadTo()\n>>> generator(instance, "file.pdf")\n"b189dfdf25e640b2ba5c497472c20962.pdf"\n```\n#### Generate the folder path using the instance\'s attributes\n```python\n>>> generator = upload_to.AttrUploadTo(attrs=["username"])\n>>> generator(instance, "file.pdf")\n"useremailcom/file.pdf"\n```\n#### Generate the folder path using the app_label and the model_name from the instance\'s meta options\n```python\n>>> generator = upload_to.ModelUploadTo()\n>>> generator(instance, "file.pdf")\n"my_app/user/file.pdf"\n```\n\n## Customize your upload paths\n\n```python\n# my_app/models.py\nimport upload_to\nfrom django.db import models\n\n\ndef my_upload_generator(instance, filename):\n    filename = upload_to.uuid_filename(filename)\n    path = upload_to.options_from_instance(instance)\n    return upload_to.upload_to(path, filename)\n\nclass MyProfile(models.Model):\n    user = models.OneToOneField(...)\n    avatar = models.FileField(upload_to=my_upload_generator)\n```',
    'author': 'Valberto Carneiro',
    'author_email': 'valbertovc@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/valbertovc/django-upload-to',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
