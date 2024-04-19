import asyncio
import PyTubeStudio.models as models
import PyTubeStudio.jaarfivts as jaarfivts
import time

myvts = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")


async def timeIt(func):
    t1 = time.time()
    result = await func
    t2 = time.time()
    diff = t2 - t1  #
    print("The function", func.__name__, "took", diff, "seconds")
    return result


async def connect(vts: jaarfivts.JaarfiVts):
    await timeIt(vts.connect())
    await timeIt(vts.authenticate(models.AuthenticationTokenRequest()))
   
    request = models.PostProcessingUpdateRequest(data=models.PostProcessingUpdateRequestData(randomize_all=True))
    response = await vts.request(request)
    response = models.PostProcessingUpdateResponse.model_validate(response)

asyncio.run(connect(myvts))
