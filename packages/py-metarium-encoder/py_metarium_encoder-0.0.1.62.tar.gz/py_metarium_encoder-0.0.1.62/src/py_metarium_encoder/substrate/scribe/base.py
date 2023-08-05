# Author: MetariumProject

# local libraries
from ..base import SubstrateBaseEncoder


class SubstrateScribeUpdater(SubstrateBaseEncoder):

    def is_valid_data(self, data:dict={}):
        # check if data has the required keys
        assert "node" in data and isinstance(data["node"], str)
        # return true
        return True

    def compose_call(self, data:dict={}):
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                "scribe_node": data["node"]
            }
        )
