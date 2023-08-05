# Author: MetariumProject

# local libraries
from ...utils import ServiceAlreadyExistsError
from ..base import SubstrateBaseEncoder
from .hasher import Hasher


class SubstrateTopicPauseTogglerAsConfigurationNode(SubstrateBaseEncoder):

    FUNCTION_CALL = "topic_pause_toggled"

    def is_valid_data(self, data: dict = {}):
        assert "topic_id" in data and isinstance(data["topic_id"], int)# topic id
        assert "toggle_value" in data and isinstance(data["toggle_value"], bool)# toggle value
        # return true
        return True
    
    def compose_call(self, data:dict={}):
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                'topic_id': str(data["topic_id"]),
                'toggle_value': data["toggle_value"]
            }
        )


class SubstrateTopicCommitterAdderAsConfigurationNode(SubstrateBaseEncoder):

    FUNCTION_CALL = "node_added_to_topic_committer_set"

    def is_valid_data(self, data: dict = {}):
        print(f"\n\n{data = }")
        assert "topic_id" in data and isinstance(data["topic_id"], int)# topic id
        assert "node" in data and isinstance(data["node"], str)# new access setting address
        # return true
        return True
    
    def compose_call(self, data:dict={}):
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                'topic_id': str(data["topic_id"]),
                'committer_node_address': data["node"]
            }
        )


class SubstrateTopicCommitterRemoverAsConfigurationNode(SubstrateBaseEncoder):

    FUNCTION_CALL = "node_removed_from_topic_committer_set"

    def is_valid_data(self, data: dict = {}):
        print(f"\n\n{data = }")
        assert "topic_id" in data and isinstance(data["topic_id"], int)# topic id
        assert "node" in data and isinstance(data["node"], str)# new access setting address
        # return true
        return True
    
    def compose_call(self, data:dict={}):
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                'topic_id': str(data["topic_id"]),
                'committer_node': data["node"]
            }
        )


class SubstrateTopicListenerAdderAsConfigurationNode(SubstrateBaseEncoder, Hasher):

    FUNCTION_CALL = "node_added_to_topic_listener_set"

    def is_valid_data(self, data: dict = {}):
        assert "topic_id" in data and isinstance(data["topic_id"], int)# topic id
        assert "node" in data and isinstance(data["node"], str)# substrate address
        assert "id" in data and isinstance(data["id"], str)# service id, eg IPFS peer id
        assert "ip_address" in data and isinstance(data["ip_address"], str)# IP address
        assert "swarm_key" in data and isinstance(data["swarm_key"], str)# blake3 hash of the swarm key file
        assert "status" in data and isinstance(data["status"], str)# blake3 hash of the status file
        assert "rff" in data and isinstance(data["rff"], str)# IPFS cid of the rff file
        # return true
        return True
    
    def compose_call(self, data:dict={}):
        if data["status"]:
            data["status"] = self._create_hash(
                data={"type": "file", "content": data["status"]}
            )
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                'topic_id': str(data["topic_id"]),
                'listener_node_address': data["node"],
                'listener_node_id': data["id"],
                'listener_ip_address': data["ip_address"],
                'listener_swarm_key': data["swarm_key"],
                'listener_status_file': data["status"],
                'listener_rff_file': data["rff"]
            }
        )


class SubstrateTopicListenerRemoverAsConfigurationNode(SubstrateBaseEncoder):

    FUNCTION_CALL = "node_removed_from_topic_committer_set"

    def is_valid_data(self, data: dict = {}):
        print(f"\n\n{data = }")
        assert "topic_id" in data and isinstance(data["topic_id"], int)# topic id
        assert "node" in data and isinstance(data["node"], str)# new access setting address
        # return true
        return True
    
    def compose_call(self, data:dict={}):
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                'topic_id': str(data["topic_id"]),
                'listener_node_address': data["node"]
            }
        )