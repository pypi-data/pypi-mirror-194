# py-metarium-encoder

# Usage


## 1. Virtual environment

### 1.1. Install virtual environment

```
pip3 install virtualenv
```

### 1.2. Create virtual environment for metarium

```
python3 -m venv virtualenv ~/venv-metarium-encoder
```

### 1.3. Activate metarium virtual environment

```
source ~/.venv-metarium-encoder/bin/activate
```

## 2. Install

### 2.1. Install metarium

```
pip install py-metarium==0.0.2.5
```

### 2.2. Install metarium-encoder

```
pip install py-metarium-encoder==0.0.1.5
```

### 2.3. Install substrate client

```
pip install substrate-interface==1.4.0
```

### 2.4. Install blake3

```
pip install blake3==0.3.3
```

### 2.5 Install dotenv
```
pip install python-dotenv==0.21.0
```

## 3. Example usage

### 3.1. Create a simple Uploader

#### 3.1.1. Environment file to store configuration

Create a `.env` file to store your secrets
```
MNEMONIC=your mnemonic here ...
NODE_URL=ws://127.0.0.1:9944
```

#### 3.1.2. Text Uploader script
Create a uploader script called `simple-text-uploader.py` with the following code block
```
from dotenv import dotenv_values

from py_metarium_encoder import (
    SubstrateAriKuriCreatorAsScribe,
)

MNEMONIC = None
NODE_URL = None

def set_secrets():
    config = dotenv_values(".env")

    MNEMONIC = config.get("MNEMONIC", None)
    NODE_URL = config.get("NODE_URL", None)

def create_kuris():
    assert MNEMONIC is not None, "Please set the MNEMONIC in your .env file"
    assert NODE_URL is not None, "Please set the NODE_URL in your .env file"
    e = SubstrateAriKuriCreatorAsScribe(url=NODE_URL, mnemonic=MNEMONIC)
    kuri_data = {
        "topic_id": 1,
        "type": "text",
        "content": "idhayam"
    }
    transaction_hash = e.encode(
        data=kuri_data,
        wait_for_inclusion=True,
        wait_for_finalization=False
    )
    print(f"Transaction hash: {transaction_hash}")

if __name__ == "__main__":
    set_secrets()
    create_kuris()
```
Run the uploader script
```
python simple-text-uploader.py
```

#### 3.1.3. KuriUploader script
Create a uploader script called `simple-kuri-uploader.py` with the following code block
```
import time
import os

from dotenv import dotenv_values

from py_metarium_encoder import (
    SubstrateAriKuriCreatorAsScribe,
)

MNEMONIC = None
NODE_URL = None

def set_secrets():
    config = dotenv_values(".env")

    MNEMONIC = config.get("MNEMONIC", None)
    NODE_URL = config.get("NODE_URL", None)

class Uploader(object):
    def __init__(self,
            url:str=None, mnemonic:str=None,
            folder_path:str=None):
        assert url is not None
        assert mnemonic is not None
        assert folder_path is not None
        self.folder_path = folder_path
        self.file_set = set()
        self.encoder = SubstrateAriKuriCreatorAsScribe(url=url, mnemonic=mnemonic)

    def upload(self, data:dict={}):
        return self.encoder.encode(
            data=data,
            wait_for_inclusion=True,
            wait_for_finalization=False
        )
    
    def watch_folder(self):
        print(f"Watching folder: {self.folder_path}")
        while True:
            time.sleep(2)
            for file in os.listdir(self.folder_path):
                if file.startswith("."):
                    continue
                if file not in self.file_set:
                    self.file_set.add(file)
                    print(f"New file: {file}")
                    self.upload(data={
                        "topic_id": 1,
                        "type": "file",
                        "content": os.path.join(self.folder_path, file)
                    })

if __name__ == "__main__":
    set_secrets()
    assert MNEMONIC is not None, "Please set the MNEMONIC in your .env file"
    assert NODE_URL is not None, "Please set the NODE_URL in your .env file"
    u = Uploader(url=NODE_URL, mnemonic=MNEMONIC, folder_path=FOLDER_PATH)
    u.watch_folder()
```
Run the uploader script
```
python simple-kuri-uploader.py
```

## 4. Teardown

Please remember to deactivate the virtual environment after usage

```
deactivate
```