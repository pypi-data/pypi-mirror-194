import os
from typing import Any, Dict, List, Optional

import click
import yaml

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client import ComputeTemplate, ProductionJob
from anyscale.controllers.base_controller import BaseController
from anyscale.controllers.job_controller import JobController
from anyscale.formatters.service_formatter import (
    format_service_config,
    format_service_config_v2,
)
from anyscale.models.service_model import ServiceConfig
from anyscale.project import infer_project_id
from anyscale.util import get_endpoint, is_anyscale_workspace
from anyscale.utils.runtime_env import override_runtime_env_for_local_working_dir


def _is_v2_service_id(service_id: str) -> bool:
    return service_id.startswith("service2")


class ServiceController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log
        self.job_controller = JobController(
            initialize_auth_api_client=initialize_auth_api_client
        )

    def _get_service_id_from_name(
        self, service_name: str, project_id: Optional[str]
    ) -> str:
        """Get the ID for a service by name.

        If project_id is specified, filter to that project, else use the default infer_project_id logic.

        Raises an exception if there are zero or multiple services with the given name.
        """
        if project_id is None:
            project_id = infer_project_id(
                project_id, self.anyscale_api_client, self.log
            )

        results = self.api_client.list_services_api_v2_services_v2_get(
            project_id=project_id, name=service_name,
        ).results

        if len(results) == 0:
            raise click.ClickException(
                f"No service with name '{service_name}' was found. "
                "Please verify that this service exists and you have access to it."
            )
        elif len(results) > 1:
            raise click.ClickException(
                f"There are multiple services with name '{service_name}'. "
                "Please specify the --service-id instead."
            )

        return results[0].id

    def get_service_id(
        self,
        service_id: Optional[str],
        service_name: Optional[str],
        service_config_file: Optional[str],
    ) -> str:
        """Get the service ID given the ID, name, or config file.

        This is a utility used by multiple CLI commands to standardize mapping these options
        to a service_id.

        The precedence is: service_id > service_name > service_config_file.

        If the service_config_file is provided and it has a project_id, that will be used to
        filter the query. Else this uses the infer_project_id default logic.
        """
        if service_id is not None:
            if service_name is not None or service_config_file is not None:
                raise click.ClickException(
                    "Only one of service ID, name, or config file should be specified."
                )
        elif service_name is not None:
            if service_config_file is not None:
                raise click.ClickException(
                    "Only one of service ID, name, or config file should be specified."
                )
            service_id = self._get_service_id_from_name(service_name, None)
        elif service_config_file is not None:
            service_config: ServiceConfig = self._read_service_config_file(
                service_config_file
            )
            service_id = self._get_service_id_from_name(
                service_config.name, service_config.project_id
            )
        else:
            raise click.ClickException(
                "Service ID, name, or config file must be specified."
            )

        return service_id

    def deploy(  # noqa: PLR0913
        self,
        service_config_file: str,
        name: Optional[str],
        description: Optional[str],
        healthcheck_url: Optional[str] = None,
        is_entrypoint_cmd: Optional[bool] = False,
        entrypoint: Optional[List[str]] = None,
    ) -> None:
        entrypoint = entrypoint or []
        if is_anyscale_workspace() and is_entrypoint_cmd:
            entrypoint = [service_config_file, *entrypoint]
            config = self.generate_config_from_entrypoint(
                entrypoint, name, description, healthcheck_url=healthcheck_url
            )
            project_id = infer_project_id(
                config.project_id, self.anyscale_api_client, self.log
            )

            config.runtime_env = override_runtime_env_for_local_working_dir(
                config.runtime_env
            )
            config.project_id = project_id
            self.deploy_from_config(config)
        elif len(entrypoint) == 0:
            # Assume that service_config_file is a file and submit it.
            config = self.generate_config_from_file(
                service_config_file, name, description, healthcheck_url=healthcheck_url,
            )
            project_id = infer_project_id(
                config.project_id, self.anyscale_api_client, self.log
            )

            config.runtime_env = override_runtime_env_for_local_working_dir(
                config.runtime_env
            )
            config.project_id = project_id
            self.deploy_from_config(config)
        elif len(entrypoint) != 0:
            msg = (
                "Within an Anyscale Workspace, `anyscale service deploy` takes either a file, or a command. To submit a command, use `anyscale service deploy -- my command`."
                if is_anyscale_workspace()
                else "`anyscale service deploy` takes one argument, a YAML file configuration. Please use `anyscale service deploy my_file`."
            )
            raise click.ClickException(msg)

    def generate_config_from_entrypoint(
        self,
        entrypoint: List[str],
        name: Optional[str],
        description: Optional[str],
        healthcheck_url: Optional[str] = "/healthcheck",
    ) -> ServiceConfig:
        config_dict = {
            "entrypoint": " ".join(entrypoint),
            "name": name,
            "description": description,
            "healthcheck_url": healthcheck_url,
        }
        return self._populate_service_config(config_dict)

    def generate_config_from_file(
        self,
        service_config_file,
        name: Optional[str] = None,
        description: Optional[str] = None,
        healthcheck_url: Optional[str] = None,
        version: Optional[str] = None,
        canary_percent: Optional[int] = None,
    ) -> ServiceConfig:
        service_config: ServiceConfig = self._read_service_config_file(
            service_config_file
        )
        if name:
            service_config.name = name

        if description:
            service_config.description = description

        if healthcheck_url:
            service_config.healthcheck_url = healthcheck_url

        if version:
            service_config.version = version

        if canary_percent:
            service_config.canary_weight = canary_percent

        return service_config

    def deploy_from_config(self, service_config: ServiceConfig):
        apply_service_config = format_service_config(service_config)
        # TODO: shawnp. Change to the new Services API
        # once the new endpoint works for both Service v1 and v2.
        create_production_service = apply_service_config.service_v1_config
        if create_production_service:
            service = self.api_client.apply_service_api_v2_decorated_ha_jobs_apply_service_put(
                create_production_service
            ).result
        else:
            # TODO: shawnp. This condition should never occur
            raise RuntimeError("The Service configuration is missing")
        service_id = service.id
        current_state = service.state.current_state

        maximum_uptime_minutes = self._get_maximum_uptime_minutes(service)
        self.log.info(
            f"Maximum uptime is {self._get_maximum_uptime_output(maximum_uptime_minutes)} for clusters launched by this service."
            f"{self._get_additional_log_if_maximum_uptime_enabled(maximum_uptime_minutes)}"
        )

        self.log.info(
            f"Service {service_id} has been deployed. Current state of service: {current_state}."
        )
        self.log.info(
            f"Query the status of the service with `anyscale service list --service-id {service.id}`."
        )
        self.log.info(
            f'View the service in the UI at {get_endpoint(f"/services/{service.id}")}.'
        )

    def _get_maximum_uptime_minutes(self, service: ProductionJob) -> Optional[int]:
        compute_config: ComputeTemplate = self.api_client.get_compute_template_api_v2_compute_templates_template_id_get(
            service.config.compute_config_id
        ).result
        return compute_config.config.maximum_uptime_minutes

    def _get_maximum_uptime_output(self, maximum_uptime_minutes: Optional[int]) -> str:
        if maximum_uptime_minutes and maximum_uptime_minutes > 0:
            return f"set to {maximum_uptime_minutes} minutes"
        return "disabled"

    def _get_additional_log_if_maximum_uptime_enabled(
        self, maximum_uptime_minutes: Optional[int]
    ) -> str:
        if maximum_uptime_minutes and maximum_uptime_minutes > 0:
            return " This may cause disruptions. To disable, update the compute config."
        return ""

    def _populate_service_config(self, config_dict: Dict[str, Any]) -> ServiceConfig:
        if (
            "ANYSCALE_EXPERIMENTAL_WORKSPACE_ID" in os.environ
            and "ANYSCALE_SESSION_ID" in os.environ
        ):
            cluster = self.anyscale_api_client.get_cluster(
                os.environ["ANYSCALE_SESSION_ID"]
            ).result
            # If the job configs are not specified, infer them from the workspace:
            if "build_id" not in config_dict and "cluster_env" not in config_dict:
                config_dict["build_id"] = cluster.cluster_environment_build_id
            if "project_id" not in config_dict:
                config_dict["project_id"] = cluster.project_id
            if (
                "compute_config" not in config_dict
                and "compute_config_id" not in config_dict
            ):
                config_dict["compute_config_id"] = cluster.cluster_compute_id
        service_config = ServiceConfig.parse_obj(config_dict)
        return service_config

    def _read_service_config_file(self, service_config_file: str) -> ServiceConfig:
        if not os.path.exists(service_config_file):
            raise click.ClickException(f"Config file {service_config_file} not found.")

        with open(service_config_file) as f:
            config_dict = yaml.safe_load(f)

        return self._populate_service_config(config_dict)

    def rollout(
        self,
        service_config_file: str,
        name: Optional[str] = None,
        version: Optional[str] = None,
        canary_percent: Optional[int] = None,
    ):
        """
        Deploys a Service 2.0.
        """
        config = self.generate_config_from_file(
            service_config_file,
            name=name,
            version=version,
            canary_percent=canary_percent,
        )
        config.runtime_env = override_runtime_env_for_local_working_dir(
            config.runtime_env
        )
        service_v2_config = format_service_config_v2(config)
        service = self.api_client.apply_service_v2_api_v2_services_v2_apply_put(
            service_v2_config
        ).result

        self.log.info(
            f"Service {service.id} has been deployed. Service is transitioning towards: {service.goal_state}."
        )
        self.log.info(
            f'View the service in the UI at {get_endpoint(f"/services/{service.id}")}.'
        )

    def list(  # noqa: PLR0913
        self,
        include_all_users: bool,
        include_archived: bool,
        name: Optional[str],
        service_id: Optional[str],
        project_id: Optional[str],
        max_items: int,
    ) -> None:
        self.job_controller.list(
            include_all_users,
            name,
            service_id,
            project_id,
            include_archived=include_archived,
            max_items=max_items,
            is_service=True,
        )

    def archive(self, service_id: str):
        if _is_v2_service_id(service_id):
            raise click.ClickException(
                "archive is not currently supported for v2 services."
                "Please contact Anyscale support for more information."
            )

        self.job_controller.archive(service_id, None, is_service=True)

    def rollback(self, service_id: str) -> None:
        if not _is_v2_service_id(service_id):
            raise click.ClickException(
                "rollback is only supported for v2 services."
                "Please contact Anyscale support for more information."
            )

        service = self.api_client.rollback_service_api_v2_services_v2_service_id_rollback_post(
            service_id
        ).result

        self.log.info(f"Service {service.id} rollback initiated.")
        self.log.info(
            f'View the service in the UI at {get_endpoint(f"/services/{service.id}")}.'
        )

    def terminate(self, service_id: str) -> None:
        if _is_v2_service_id(service_id):
            self.api_client.terminate_service_api_v2_services_v2_service_id_terminate_post(
                service_id
            )
        else:
            self.job_controller.terminate(service_id, None, is_service=True)
