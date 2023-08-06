import time

from typing import Optional, Dict, Any

from ai_dashboard.api import endpoints, helpers
from ai_dashboard.dashboard import dashboard

from ai_dashboard import constants
from ai_dashboard import errors


class Client:
    def __init__(self, token: str) -> None:

        self._credentials = helpers.process_token(token)
        self._token = token
        self._endpoints = endpoints.Endpoints(credentials=self._credentials)

        try:
            response = self.list_deployables()
        except:
            raise errors.AuthException
        else:
            self._deployables = sorted(
                response["deployables"], key=lambda x: x["insert_date_"]
            )
            print(constants.WELCOME_MESSAGE.format(self._credentials.project))

    @property
    def deployables(self):
        response = self.list_deployables()
        self._deployables = sorted(
            response["deployables"], key=lambda x: x["insert_date_"]
        )
        return self._deployables

    def _find_config(
        self,
        dataset_id: str = None,
        project_id: str = None,
        deployable_name: str = None,
    ):
        for deployable_json in self.deployables:
            if dataset_id is not None:
                dataset_id_match = deployable_json.get("dataset_id") == dataset_id
            else:
                dataset_id_match = True

            if project_id is not None:
                project_id_match = deployable_json.get("project_id") == project_id
            else:
                project_id_match = True

            if deployable_name is not None:
                deployable_config = deployable_json.get("configuration", {})
                deployable_name_match = (
                    deployable_config.get("deployable_name") == deployable_name
                )
            else:
                deployable_name = True

            if dataset_id_match and deployable_name_match and project_id_match:
                dataset_id = deployable_json["dataset_id"]
                project_id = deployable_json["project_id"]
                deployable_id = deployable_json["deployable_id"]
                return dataset_id, project_id, deployable_id, deployable_config

        raise ValueError(
            f"No deployable found that matches `dataset_id`={dataset_id} and/or `project_id`={project_id} and/or `deployablable_name`={deployable_name}"
        )

    def load_dashboard(
        self,
        deployable_name: str = None,
        dataset_id: str = None,
        project_id: str = None,
    ) -> dashboard.Dashboard:
        dataset_id, deployable_id, project_id, configuration = self._find_config(
            dataset_id=dataset_id,
            project_id=project_id,
            deployable_name=deployable_name,
        )
        return dashboard.Dashboard(
            endpoints=self._endpoints,
            dataset_id=dataset_id,
            deployable_id=deployable_id,
            project_id=project_id,
            configuration=configuration,
        )

    def recent(self) -> dashboard.Dashboard:
        try:
            configuration = self.deployables[-1]
        except IndexError:
            raise IndexError("You have no dashboards")
        else:
            dataset_id = configuration.get("dataset_id")
            deployable_id = configuration.get("deployable_id")
            project_id = configuration.get("project_id")
            return dashboard.Dashboard(
                endpoints=self._endpoints,
                dataset_id=dataset_id,
                deployable_id=deployable_id,
                configuration=configuration["configuration"],
                project_id=project_id,
            )

    def list_deployables(self, page_size: int = 1000):
        return self._endpoints._list_deployables(page_size=page_size)

    def create_deployable(
        self,
        dataset_id: Optional[str] = None,
        deployable_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        if deployable_id is None:
            if name is not None:
                configs = [
                    d
                    for d in self.deployables
                    if d["configuration"].get("deployable_name", "") == name
                    and d.get("dataset_id") == dataset_id
                ]
                try:
                    deployable_id = configs[0]["deployable_id"]
                except:
                    pass
                else:
                    return self._endpoints._get_deployable(
                        deployable_id=deployable_id,
                    )

            if config is None:
                config = {
                    "private": False,
                    "tabs": {},
                    "filters": {},
                    "dataset_name": dataset_id,
                    "type": "explorer",
                    "filterToggles": {},
                    "deployable_name": name,
                    "cacheTimestamp": int(time.time() * 1000),
                    "api_key": "",
                    "project_id": self._credentials.project,
                    "tabOrder": [],
                    "deployable_id": "",
                    "read_key": "",
                }
            return self._endpoints._create_deployable(
                dataset_id=dataset_id,
                config=config,
            )
        else:
            return self._endpoints._get_deployable(
                deployable_id=deployable_id,
            )

    def delete_deployable(self, deployable_id: str) -> None:
        return self._endpoints._delete_deployable(deployable_id=deployable_id)

    def Dashboard(
        self,
        dataset_id: Optional[str] = None,
        deployable_id: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> dashboard.Dashboard:
        assert (
            dataset_id is not None or deployable_id is not None
        ), "Set either `dataset_id` and `config` or `deployable_id`"
        response = self.create_deployable(
            dataset_id=dataset_id,
            deployable_id=deployable_id,
            config=config,
            name=name,
        )
        return dashboard.Dashboard(endpoints=self._endpoints, **response)

    def insert_temp_local_media(self, file_path: str):
        """
        Insert temporary local media.
        """
        data = self._endpoints._get_temp_file_upload_url()
        upload_url = data["upload_url"]
        download_url = data["download_url"]
        with open(file_path, "rb") as fn_byte:
            media_content = bytes(fn_byte.read())
        self._endpoints._upload_temporary_media(
            presigned_url=upload_url,
            media_content=media_content,
        )
        return {"download_url": download_url}
