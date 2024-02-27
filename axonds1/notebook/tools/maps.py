import time
import json
import uuid
import logging
import pathlib as pl

import osparc
import osparc_client
from osparc_filecomms import handshakers

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("ToolsMap")

POLLING_WAIT = 1  # second
DISABLE_UUID_CHECK_STRING = "DISABLE_UUID_CHECK"


class oSparcFileMap:
    def __init__(
        self,
        map_file_path: pl.Path,
        caller_file_path: pl.Path,
        osparc_cfg,
        polling_interval: float = POLLING_WAIT,
        verbose_level=logging.ERROR,
    ) -> None:
        self.verbose_level = verbose_level
        logger.setLevel(self.verbose_level)

        logger.info("Creating caller map")
        self.uuid = str(uuid.uuid4())
        self.map_uuid = None
        logger.info(f"Optimizer uuid is {self.uuid}")

        self.polling_interval = polling_interval

        self.caller_file_path = caller_file_path
        if self.caller_file_path.exists():
            self.caller_file_path.unlink()
        self.map_file_path = map_file_path

        self.osparc_cfg = osparc_cfg

        self.handshaker = handshakers.FileHandshaker(
            self.uuid,
            self.map_file_path.parent,
            self.caller_file_path.parent,
            is_initiator=False,
            verbose_level=self.verbose_level,
            polling_interval=0.1,
            print_polling_interval=100,
        )
        self.map_uuid = self.handshaker.shake()

    def create_map_input_payload(self, tasks_uuid, params_sets):
        payload = {}
        payload["uuid"] = tasks_uuid
        payload["caller_uuid"] = self.uuid
        payload["map_uuid"] = self.map_uuid
        payload["command"] = "run"
        payload["tasks"] = params_sets

        return payload

    def read_map_output_payload(self, map_output_payload):
        tasks = map_output_payload["tasks"]

        objs_sets = []

        for task in tasks:
            if task["status"] != "SUCCESS":
                raise Exception(f"A task was not succesful: {task}")

            task_output = task["output"]

            objs_sets.append(task_output)

        return objs_sets

    def preprocess_params_set(self, input_params_set):
        with osparc.ApiClient(self.osparc_cfg) as api_client:
            for input_params in input_params_set:
                for input_key, input_param in input_params["input"].items():
                    if input_param["type"] == "upload_file":
                        local_file_path = input_param["value"]
                        uploaded_file = osparc.FilesApi(
                            api_client).upload_file(pl.Path(local_file_path))
                        input_param["type"] = "file"
                        input_param["value"] = json.dumps(
                            uploaded_file.to_dict())

        return input_params_set

    def postprocess_map_outputs(self, map_outputs):
        processed_outputs = []
        with osparc.ApiClient(self.osparc_cfg) as api_client:
            for map_output in map_outputs:
                processed_output = {}
                for probe_name, probe_dict in map_output.items():
                    file_dict = json.loads(probe_dict["value"])
                    osparc_file = osparc_client.models.file.File(**file_dict)
                    processed_output[probe_name] = osparc.FilesApi(
                        api_client).download_file(osparc_file.id)

                processed_outputs.append(processed_output)
        return processed_outputs

    def evaluate(self, params_set):
        logger.info(f"Evaluating: {params_set}")

        processed_params_set = self.preprocess_params_set(params_set)
        tasks_uuid = str(uuid.uuid4())
        map_input_payload = self.create_map_input_payload(
            tasks_uuid, processed_params_set
        )

        self.caller_file_path.write_text(
            json.dumps(map_input_payload, indent=4)
        )

        waiter = 0
        payload_uuid = ""
        while not self.map_file_path.exists() or payload_uuid != tasks_uuid:
            if self.map_file_path.exists():
                payload_uuid = json.loads(self.map_file_path.read_text())[
                    "uuid"
                ]
                if payload_uuid == DISABLE_UUID_CHECK_STRING:
                    break
                if waiter % 10 == 0:
                    logger.info(
                        "Waiting for tasks uuid to match: "
                        f"payload:{payload_uuid} tasks:{tasks_uuid}"
                    )
            else:
                if waiter % 10 == 0:
                    logger.info(
                        "Waiting for map results at: "
                        f"{self.map_file_path.resolve()}"
                    )
            time.sleep(self.polling_interval)
            waiter += 1

        map_output_payload = json.loads(self.map_file_path.read_text())

        objs_set = self.read_map_output_payload(map_output_payload)
        processed_objs_set = self.postprocess_map_outputs(objs_set)

        logger.info(f"Evaluation results: {processed_objs_set}")

        return processed_objs_set

    def map_function(self, *map_input):
        _ = map_input[0]
        params = map_input[1]

        return self.evaluate(params)

    def __del__(self):
        payload = {
            "command": "stop",
            "caller_uuid": self.uuid,
            "map_uuid": self.map_uuid,
        }

        self.caller_file_path.write_text(json.dumps(payload, indent=4))

        self.status = "stopping"
