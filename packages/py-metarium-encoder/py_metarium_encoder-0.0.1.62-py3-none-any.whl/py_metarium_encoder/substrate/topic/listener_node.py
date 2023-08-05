# Author: MetariumProject

# local libraries
from ...utils import ServiceAlreadyExistsError
from ..base import SubstrateBaseEncoder
from .hasher import Hasher


class SubstrateStatusUpdaterAsTopicListenerNode(SubstrateBaseEncoder, Hasher):

    FUNCTION_CALL = "topic_listener_node_status_updated"

    def is_valid_data(self, data: dict = {}):
        assert "topic_id" in data and isinstance(data["topic_id"], int)
        assert "status" in data and isinstance(data["status"], str)# blake3 hash of the status file
        assert "rff" in data and isinstance(data["rff"], str)# IPFS cid of the rff file
        # return true
        return True

    def compose_call(self, data:dict={}):
        if data["status"]:
            data["status"] = self._create_hash(
                data={"type": "file", "content": data["status"]}
            )
        print(f"Updating service status:\n\n{data['status'] = }\n{data['rff'] = }")
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                "topic_id": str(data["topic_id"]),
                'status_file': data["status"],
                'rff_file': data["rff"]
            }
        )