# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_webhooks', 'drf_webhooks.tests', 'drf_webhooks.tests.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.1,<5.0',
 'celery>=5.2,<6.0',
 'djangorestframework-xml>=2.0,<3.0',
 'djangorestframework>=3.14,<4.0',
 'httpx>=0.23,<0.24',
 'inflection>=0.5,<0.6',
 'pendulum>=2.1,<3.0',
 'pytimeparse>=1.1,<2.0',
 'xmltodict>=0.13,<0.14']

setup_kwargs = {
    'name': 'drf-webhooks',
    'version': '0.2.0',
    'description': 'Setup webhooks using existing DRF Serializers',
    'long_description': '# Django Rest Framework - Webhooks\n**Configurable webhooks for DRF Serializers**\n\n## Goals:\n- [x] Use existing DRF Serializers from REST API to serialize data in webhooks\n    - [x] Consistent data formatting\n    - [x] Reusable OpenAPI schemas\n- [x] Configurable webhooks that simply work *(by way of django signals magic)* without the developer having to keep track of where to trigger them\n    - [x] Still allow for "manual" triggering of webhooks\n        - This is useful because signals aren\'t always triggered\n        - For example: `QuerySet.update` does not trigger signals\n- [x] Disable webhooks using context managers\n    - This can be useful when syncing large chunks of data\n    - or with a duplex sync (when two systems sync with each other) to avoid endless loops\n- [x] **Webhook Signal Session**\n    - [x] A context manager gathers all models signals and at the end of the session only triggers the resulting webhooks\n        - [x] If a model instance is both `created` and `deleted` within the session, then no webhook is sent for that model instance\n        - [x] If a model instance is `created` and then also `updated` within the session, then a `created` event is sent with the data from the last `updated` signal. Only one webhook even is sent\n        - [x] If a models instance is `updated` multiple times within the session, then only one webhook event is sent\n    - [x] Middleware wraps each request in **Webhook Signal Session** context\n        - **NOTE:** The developer will have to call the context manager in code that runs outside of requests (for example in celery tasks) manually\n- [x] Automatically determine which nested models need to be monitored for changes\n\n## Examples:\n\n```python\nfrom django.db import models\nfrom drf_webhooks import ModelSerializerWebhook, register_webhook\nfrom rest_framework import serializers\n\n\nclass MyModel(models.Model):\n    name = models.CharField(max_lenght=100)\n\n\nclass MyModelSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = MyModel\n        fields = [\'id\', \'name\']\n\n\n# Automatic:\nregister_webhook(MyModel)()\n\n# ---- OR ----\n# If you need more configuration:\n@register_webhook(MyModel)\nclass MyModelWebhook(ModelSerializerWebhook):\n    base_name = \'core.my_model\'\n```\n\n# Documentation:\n\n## Quckstart:\n\n### Install `drf-webhooks`\n```bash\npoetry add drf-webhooks\n# ... or ...\npip install drf-webhooks\n```\n\n### Update `settings.py`:\n```python\nINSTALLED_APPS = [\n    # ...\n    \'drf_webhooks\',\n]\n\nMIDDLEWARE = [\n    # ...\n    \'drf_webhooks.middleware.WebhooksMiddleware\',\n]\n\n# This is required if you don\'t want your database to fill up with logs:\nCELERY_BEAT_SCHEDULE = {\n    \'clean-webhook-log\': {\n        \'task\': \'drf_webhooks.tasks.auto_clean_log\',\n        \'schedule\': 60,\n        \'options\': {\'expires\': 10},\n    },\n}\n```\n\n### Create a new django app\nRecommended app name: `webhooks`\n\n```python\n# ----------------------------------------------------------------------\n#  apps.py\n# ----------------------------------------------------------------------\nfrom django.apps import AppConfig\n\n\nclass WebhooksAppConfig(AppConfig):\n    name = "<your module name>"\n    label = "webhooks"\n\n\n# ----------------------------------------------------------------------\n#  models.py\n# ----------------------------------------------------------------------\nfrom django.contrib.auth import get_user_model\nfrom django.db import models\nfrom django.utils.translation import gettext_lazy as _\n\nfrom drf_webhooks.models import AbstractWebhook, AbstractWebhookLogEntry\n\n\nclass Webhook(AbstractWebhook):\n    # This can also be a group or an organization that the user belongs to:\n    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)\n\n    def __str__(self):\n        return \'id=%s, events=%s, owner=%s\' % (\n            str(self.id),\n            \', \'.join(self.events),\n            str(self.owner),\n        )\n\n\nclass WebhookLogEntry(AbstractWebhookLogEntry):\n    # This can also be a group or an organization that the user belongs to:\n    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)\n```\n',
    'author': 'Arnar Yngvason',
    'author_email': 'arnar@reon.is',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/demux/drf-webhooks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
