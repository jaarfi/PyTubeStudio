A library for interacting with the [VTube Studio API](https://github.com/DenchiSoft/VTubeStudio).

# Overview
This library is intended to provide a way to interact with the VTubeStudio API while minimizing the amount of mistakes a user can make while forming Requests by having them be validated using Pydantic before.

# Installation

```shell
pip install PyTubeStudio
```

# How to Use
Start off by importing the library into your project.
Because the library provides two modules, you will have to import both.


```python
import PyTubeStudio.client as pts
import VtsModels.models as models
```

This basic example connects to your VTubeStudio instance, authorizes itself and asks for the current API State.

```python
vts = pts.PyTubeStudio()

async def connect():
    await vts.connect()
    await vts.authenticate()
    answer = await vts.request(models.APIStateRequest())
    print(answer)
    await vts.close()

asyncio.run(connect())
```

## Authorization
Every time an API client connects to your VTS instance, it will have to authorize itself. This happens via an **Authorization Token**. This token will be generated the first that a request is made and will be used on subsequent requests so the popup in VTS has to be accepted only once.

The token gets saved in ~/AppData/Local/PyTubeStudio/PyTubeStudio/token.txt (I dont know where the second PyTubeStudio came from). This path can be adjusted by passing another while creating the client.


```python
vts = pts.PyTubeStudio(token_path="path")
```

## Making Requests
All Requests are backed by corresponding Pydantic models.
Heavy reference to the original [VTube Studio API Reference](https://github.com/DenchiSoft/VTubeStudio) is needed. It describes which interactions are possible and what the values actually mean.

All request models are accessed via the VtsModels module.
Most requests will quickly lead to a confusing structure as they can have multiple layers of references to other models.


This is an example of injecting a singular value into a VTS parameter.

```python
await vts.request(models.InjectParameterDataRequest(
    data=models.InjectParameterDataRequestData(
        parameter_values=[
            models.ParameterValue(
                id = "injection",
                value=avg
                )
            ]
        )
    )
)
```

Because this is hard to read, it is reccommended to define functions for often used requests.


```python
async def injectValue(id, value):
    await vts.request(models.InjectParameterDataRequest(
        data=models.InjectParameterDataRequestData(
            parameter_values=[
                models.ParameterValue(
                    id = id,
                    value = value
                    )
                ]
            )
        )
    )

await injectValue("injection", 1)
```

This will maybe be added in the future, but currently we would rather provide a complete request feature set than one that is focused on readability.

## Getting responses
The responses have been modeled as well, making the accessing of singular fields possible. To do this, the JSON that is received upon requesting has to be validated using Pydantic.



```python
answer = await vts.request(models.APIStateRequest())

response = models.APIStateResponse.model_validate_json(answer)
print(response.data.v_tube_studio_version)
```

This way you can access the individual fields and receive IDE autocomplete suggestions, making accessing them easier.

## Rate Limit

# Tests
Currently WIP, there exists a basic Unittest that checks for positive/negative answers for all requests, however that one is specifically modeled to work with a model that I am not allowed to share, they will be adjusted to make use of the basic Hiyori model that gets shipped with VTS at some point.

# Disclaimer
This is my first ever Python library and it shows, however it is feature-complete regarding the Requests and Responses as of 26.09.2024. This may change whenever the API gets updated (and doesn't include any of the event based subscriptions yet). Feel free to take any issues up with me or contribute on your own, I would love if people make use of this.

# Special Thanks
I want to thank [Genteki](https://github.com/Genteki) for their work on [pyvts](https://github.com/Genteki/pyvts/tree/main), their own take on a Python library to interact with VTS that was heavily used and referenced in the beginning of development.
Special thanks to [ArkStructCodes](https://github.com/ArkStructCodes) for all the help they provided during development and a lot of helpful insight.