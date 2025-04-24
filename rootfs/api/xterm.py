import json
import uuid

import copy
from django.conf import settings
from asgiref.sync import sync_to_async
from kubernetes.stream import stream as kube_stream
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException


class Xterm(object):
    _kubernetes = None
    _pod_template = None

    def __init__(self, app, user, token, endpoint):
        self.app = app
        self.name = f"xterm-{uuid.uuid4()}"
        self.manifest = self.pod_template()
        self.manifest["metadata"]["name"] = self.name
        self.manifest["metadata"]["labels"] = {
            "app": self.app,
            "pod": self.name,
            "heritage": "drycc",
            "app_type": "xterm",
        }
        self.user = user
        self.token = token
        self.endpoint = endpoint

    @classmethod
    def kubernetes(cls):
        if cls._kubernetes is None:
            with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as token_file:
                token = token_file.read()
            config = Configuration(host=settings.SCHEDULER_URL)
            config.api_key = {"authorization": "Bearer " + token}
            config.verify_ssl = settings.K8S_API_VERIFY_TLS
            if config.verify_ssl:
                config.ssl_ca_cert = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
            Configuration.set_default(config)
            cls._kubernetes = core_v1_api.CoreV1Api()
        return cls._kubernetes

    @classmethod
    def clean_all(cls):
        manifest = cls.pod_template()
        namespace = manifest["metadata"]["namespace"]
        kubernetes = cls.kubernetes()
        label_selector = "heritage=drycc,app_type=xterm"
        kubernetes.delete_collection_namespaced_pod(
            namespace,
            label_selector=label_selector,
            field_selector="status.phase=Failed",
        )
        kubernetes.delete_collection_namespaced_pod(
            namespace,
            label_selector=label_selector,
            field_selector="status.phase=Succeeded",
        )

    @classmethod
    def pod_template(cls):
        if cls._pod_template is None:
            with open("/etc/drycc/manager/xterm-pod-template.json") as pod_template_file:
                cls._pod_template = json.load(pod_template_file)
        return copy.deepcopy(cls._pod_template)

    async def status(self):
        try:
            pod = await sync_to_async(self.kubernetes().read_namespaced_pod)(
                self.name, self.manifest["metadata"]["namespace"])
            return pod.status.phase
        except ApiException as e:
            if e.status != 404:
                raise
        return "Unknown"

    async def create(self):
        self.manifest["spec"]["containers"][0]["env"] = [
            {
                "name": "TIMEOUT",
                "value": str(settings.XTERM_POD_TIMEOUT),
            },
            {
                "name": "DRYCC_APP",
                "value": self.app,
            },
            {
                "name": "DRYCC_USER",
                "value": self.user,
            },
            {
                "name": "DRYCC_TOKEN",
                "value": self.token,
            },
            {
                "name": "DRYCC_ENDPOINT",
                "value": self.endpoint,
            },
        ]
        await sync_to_async(self.kubernetes().create_namespaced_pod)(
            namespace=self.manifest["metadata"]["namespace"], body=self.manifest)

    async def stream(self):
        namespace = self.manifest["metadata"]["namespace"]
        args = (self.kubernetes().connect_get_namespaced_pod_exec, self.name, namespace)
        kwargs = {
            "tty": True,
            "stdin": True,
            "stderr": True,
            "stdout": True,
            "command": ["bash"],
            "_preload_content": False,
        }
        return await sync_to_async(kube_stream)(*args, **kwargs)

    async def clean(self):
        try:
            label_selector = f"app={self.app},heritage=drycc,app_type=xterm"
            namespace = self.manifest["metadata"]["namespace"]
            await sync_to_async(self.kubernetes().delete_collection_namespaced_pod)(
                namespace, label_selector=label_selector, field_selector="status.phase=Failed",
            )
            await sync_to_async(self.kubernetes().delete_collection_namespaced_pod)(
                namespace, label_selector=label_selector, field_selector="status.phase=Succeeded",
            )
            return True
        except ApiException as e:
            if e.status != 404:
                raise
        return False
