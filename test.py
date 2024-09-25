import PyTubeStudio.client as pts
import VtsModels.models as models
import asyncio

vts = pts.PyTubeStudio()

async def connect():
    await vts.connect()
    await vts.authenticate()
    await vts.request(models.MoveModelRequest(data=models.MoveModelRequestData(rotation=90,time_in_seconds=0.2, values_are_relative_to_model=True)))
    await vts.close()

asyncio.run(connect())
