# Author: MetariumProject

# standard libraries
from blake3 import blake3
# local libraries
from ...utils import AriKuriAlreadyExistsError
from ..base import SubstrateBaseEncoder


class SubstrateAriKuriAdderAsTopicCommitterNode(SubstrateBaseEncoder):

    FUNCTION_CALL = "arikuri_added"

    VALID_KURI_TYPES = ["file", "text", "image", "video", "audio", "application", "message", "other"]

    def is_valid_data(self, data:dict={}):
        # check if data has the required keys
        assert "topic_id" in data and isinstance(data["topic_id"], int)
        assert "type" in data and data["type"] in self.__class__.VALID_KURI_TYPES
        assert "content" in data
        # return true
        return True

    def compose_call(self, data:dict={}):
        # prepare the kuri
        kuri = self.__prepare_kuri(data=data)
        query_result = self.metarium_node.query(
            module=self.__class__.SUBSTRATE_EXTRINSIC,
            storage_function="Arikuris",
            params=[str(data["topic_id"]), kuri],
        )
        if query_result.serialize() is not None:
            raise AriKuriAlreadyExistsError(f"Arikuri already exists: {kuri}")
        print(f"Uploading Kuri: {kuri} ...")
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                "topic_id": str(data["topic_id"]),
                'kuri': kuri,
            }
        )

    def __blake3_hash(self, data:dict={}):
        # Create a Blake3 hash object
        hasher = blake3(max_threads=blake3.AUTO)
        # hash text
        if data["type"] == "text":
            content = bytes(data["content"], 'utf-8')
            # Update the hash with the data
            hasher.update(content)
        # hash file
        elif data["type"] in ["file", "image", "video", "audio", "application", "message", "other"]:
            with open(data["content"], "rb") as f:
                counter = 0
                while True:
                    counter += 1
                    content = f.read(1024)
                    if not content:
                        break
                    hasher.update(content)
            # print(f"Hashed {counter} chunks of 1024 bytes")
        # Return the hexadecimal representation of the hash
        return hasher.hexdigest()

    def __create_hash(self, data:dict={}):
        # create a blake3 hash of the data
        data_hash = self.__blake3_hash(data=data)
        # return the hash
        return data_hash
    
    def __prepare_kuri(self, data:dict={}):
        # create a blake3 hash of the data
        data_hash = self.__create_hash(data=data)
        # return the kuri
        return f"|>blake3|{data_hash}"
        # return f"{data_hash}"