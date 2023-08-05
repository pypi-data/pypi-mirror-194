# Author: MetariumProject

# local libraries
from .base import SubstrateScribeUpdater


class SubstrateScribeAdderAsRoot(SubstrateScribeUpdater):

    FUNCTION_CALL = "force_add_node_to_scribe_set"


class SubstrateScribeRemoverAsRoot(SubstrateScribeUpdater):

    FUNCTION_CALL = "force_remove_node_from_scribe_set"