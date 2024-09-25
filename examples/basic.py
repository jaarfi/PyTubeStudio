import PyTubeStudio.client as pts
import VtsModels.models as models
import asyncio

vts = pts.PyTubeStudio()

async def connect():
    await vts.connect()
    await vts.authenticate()
    answer = await vts.request(models.APIStateRequest())
    print(answer)
    await vts.close()

asyncio.run(connect())
