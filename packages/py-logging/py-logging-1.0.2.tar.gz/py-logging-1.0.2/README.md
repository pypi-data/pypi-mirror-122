<div align="center">
<h1>py-logging</h1>
<h4>Configurable and easy extendable python logger</h4>
<img src="https://forthebadge.com/images/badges/made-with-python.svg" alt="Build with python">
<img src="https://forthebadge.com/images/badges/it-works-why.svg" alt="That works?">
</div>

## Status:

| Branch  | Tests | Code Quality |
|--------|-------|--------------|
| master  | [![buddy pipeline](https://app.buddy.works/kamilszczurowski/py-logging/pipelines/pipeline/352790/badge.svg?token=6dda2c8e079657e0791becb1d6378b1339e08c37c5051d3ee2a5509352835489 "buddy pipeline")](https://app.buddy.works/kamilszczurowski/py-logging/pipelines/pipeline/352790) | ![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/szczurowsky/py-logging/master?style=for-the-badge) |

## Usage
### Basic

```python
from pylogging.logger import Logger
from pylogging.log_level import LogLevel

logger = Logger()

logger.log(LogLevel.INFO, "Connection initialized")
logger.log(LogLevel.WARNING, "The rat bit your cables")
logger.log(LogLevel.ERROR, "The plague of rats in the server room")
```
<img alt="showcase" src="https://i.imgur.com/TXzrEHN.png">

### Formatters
<details>
<summary>Scope</summary>

```python
from pylogging.logger import Logger
from pylogging.log_level import LogLevel

logger = Logger()
logger.set_options({"scope": True})

logger.log(LogLevel.ERROR, "Cannot connect to host")

```
<img alt="showcase" src="https://i.imgur.com/z7diH85.png">

</details>

<details>
<summary>List</summary>

```python
from pylogging.logger import Logger
from pylogging.log_level import LogLevel

logger = Logger()

logger.log(LogLevel.INFO, ["List", "List"])
```
<img alt="showcase" src="https://i.imgur.com/ZqhmITb.png">

</details>

<details>
<summary>Dictionary</summary>

```python
from pylogging.logger import Logger
from pylogging.log_level import LogLevel

logger = Logger()

logger.log(LogLevel.INFO, {"1": "Value1", "2": "Value2"})

```
<img alt="showcase" src="https://i.imgur.com/ved6NSs.png">

</details>


