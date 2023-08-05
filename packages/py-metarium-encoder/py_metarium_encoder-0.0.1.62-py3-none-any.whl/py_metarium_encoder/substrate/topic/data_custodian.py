# Author: MetariumProject

# local libraries
from ...utils import ServiceAlreadyExistsError
from ..base import SubstrateBaseEncoder


class SubstrateTopicCreatorAsDataCustodian(SubstrateBaseEncoder):

    FUNCTION_CALL = "topic_added"

    def is_valid_data(self, data: dict = {}):
        assert "topic_id" in data and isinstance(data["topic_id"], int)# topic id
        assert "committer_nodes" in data and isinstance(data["committer_nodes"], list)# list of scribes authorized to the topic
        # return true
        return True
    
    def compose_call(self, data:dict={}):
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                'topic_id': str(data["topic_id"]),
                'topic_committer_nodes': data["scribes"]
            }
        )


class SubstrateTopicAccessSettingAddressModifierAsDataCustodian(SubstrateBaseEncoder):

    FUNCTION_CALL = "topic_configuration_node_changed"

    def is_valid_data(self, data: dict = {}):
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
                'new_topic_configuration_node': data["node"]
            }
        )