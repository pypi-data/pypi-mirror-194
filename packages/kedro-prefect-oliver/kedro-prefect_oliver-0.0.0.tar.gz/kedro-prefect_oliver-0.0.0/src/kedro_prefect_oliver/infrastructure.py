from prefect.infrastructure.kubernetes import KubernetesJob


def create_infrastructure(docker_image: str, 
                          package_name: str, 
                          image_pull_policy: str = "Always",
                          finished_job_ttl: int = 43200,
                          pod_watch_timeout_seconds: int = 360,
                          container_memory: str = "3Gi",
                          container_cpu: str = "1",
                          container_storage: str = "4096Mi"
                          ):
    package_name = package_name.replace("-", "_").replace(" ", "_")
    kubernetes_job = KubernetesJob(
        image=docker_image,
        image_pull_policy=image_pull_policy,
        finished_job_ttl=finished_job_ttl,
        pod_watch_timeout_seconds=pod_watch_timeout_seconds,
        namespace="prefect2",
        env={
            "PREFECT_LOGGING_EXTRA_LOGGERS": "kedro,kedro.io.data_catalog,kedro.framework.session.session,"
                                             f"kedro.pipeline.node,{package_name}",
        },
        job={
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {"labels": {}},
            "spec": {
                "template": {
                    "spec": {
                        "parallelism": 1,
                        "completions": 1,
                        "restartPolicy": "Never",
                        "containers": [
                            {
                                "name": "prefect-job",
                                "resources": {
                                    "requests": {
                                        "memory":container_memory,
                                        "cpu":container_cpu,
                                        "ephemeral-storage":container_storage,
                                    },
                                },
                                "env": [],
                            }
                        ],
                    }
                }
            },
        }
    )
    kubernetes_job.save(f"{package_name}-prefect2-kubernetes-job", overwrite=True)


if __name__ == "__main__":
    create_infrastructure()
