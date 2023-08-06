# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adrf']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.1', 'djangorestframework>=3.14.0']

setup_kwargs = {
    'name': 'adrf',
    'version': '0.1.1',
    'description': 'Async support for Django REST framework',
    'long_description': '# Async Django REST framework\n\n**Async support for Django REST framework**\n\n# Requirements\n\n* Python 3.8+\n* Django 4.1\n\nWe **highly recommend** and only officially support the latest patch release of\neach Python and Django series.\n\n# Installation\n\nInstall using `pip`...\n\n    pip install adrf\n\nAdd `\'adrf\'` to your `INSTALLED_APPS` setting.\n```python\nINSTALLED_APPS = [\n    ...\n    \'adrf\',\n]\n```\n\n# Examples\n\n# Async Views\n\nWhen using Django 4.1 and above, this package allows you to work with async class and function based views.\n\nFor class based views, all handler methods must be async, otherwise Django will raise an exception. For function based views, the function itself must be async.\n\nFor example:\n\n```python\nfrom adrf.views import APIView\n\nclass AsyncView(APIView):\n    async def get(self, request):\n        return Response({"message": "This is an async class based view."})\n\nfrom adrf.decorators import api_view\n\n@api_view([\'GET\'])\nasync def async_view(request):\n    return Response({"message": "This is an async function based view."})\n```\n# Async ViewSets\n\nFor viewsets, all handler methods must be async too.\n\nviews.py\n```python\nfrom django.contrib.auth import get_user_model\nfrom rest_framework.response import Response\n\nfrom adrf.viewsets import ViewSet\n\n\nUser = get_user_model()\n\n\nclass AsyncViewSet(ViewSet):\n\n    async def list(self, request):\n        return Response(\n            {"message": "This is the async `list` method of the viewset."}\n        )\n\n    async def retrieve(self, request, pk):\n        user = await User.objects.filter(pk=pk).afirst()\n        return Response({"user_pk": user and user.pk})\n\n```\n\nurls.py\n```python\nfrom django.urls import path, include\nfrom rest_framework import routers\n\nfrom . import views\n\nrouter = routers.DefaultRouter()\nrouter.register(r"async_viewset", views.AsyncViewSet, basename="async")\n\nurlpatterns = [\n    path("", include(router.urls)),\n]\n\n```\n',
    'author': 'Enrico Massa',
    'author_email': 'enrico.massa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/em1208/adrf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
