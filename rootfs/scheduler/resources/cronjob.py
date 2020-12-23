from kubernetes.client import BatchV1beta1Api

from scheduler.resources import Resource


class Cronjob(Resource):
    batch = BatchV1beta1Api()

    @staticmethod
    def manifest(namespace, name, version=None, **kwargs):
        labels = {
            'heritage': 'drycc',
        }
        cfg = {
            'apiVersion': 'batch/v1',
            'kind': 'Cronjob',
            'metadata': {
                'name': name,
                'namespace': namespace,
                'labels': labels
            },
            'spec': {
                'schedule': kwargs.get('schedule'),
                'jobTemplate': {
                    'spec': {
                        'restartPolicy': 'OnFailure',
                        'containers': [{
                            'name': 'upload',
                            'image': kwargs.get('image'),
                            'command': kwargs.get('command'),
                        }]
                    }
                }
            }
        }
        if version:
            cfg["metadata"]["resourceVersion"] = version
        return cfg

    def create(self, namespace, name, **kwargs):
        cfg = self.manifest(namespace, name, **kwargs)
        res = self.batch.create_namespaced_cron_job(namespace=namespace,
                                                    body=cfg)
        return res

    def put(self, job, namespace, name, **kwargs):
        job.spec.template.spec.containers[0].image = kwargs.get('image')
        job.spec.schedule = kwargs.get('schedule')
        res = self.batch.patch_namespaced_cron_job(
            name=name,
            namespace=namespace,
            body=job)
        return res

    def get(self, namespace):
        job_list = self.batch.list_namespaced_cron_job(namespace=namespace)
        return job_list

    def delete(self, namespace, job_name):
        status = self.batch.delete_namespaced_cron_job(
            namespace=namespace,
            name=job_name,
            propagation_policy='Background',
        )
        return status
