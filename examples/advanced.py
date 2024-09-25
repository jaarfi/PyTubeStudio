import PyTubeStudio.client as pts
import VtsModels.models as models
import asyncio


async def spin():
    
    vts = pts.PyTubeStudio()
    await vts.connect()
    await vts.authenticate()
    for i in range(60):
        await vts.request(models.MoveModelRequest(
            data=models.MoveModelRequestData(
                time_in_seconds = 0,
                rotation = 6,
                values_are_relative_to_model = True
            )
        ))
    await vts.close()

async def rainbow():
    
    vts = pts.PyTubeStudio()
    await vts.connect()
    await vts.authenticate()

    increase = True
    colors = [0, 255, 0]
    change = 20
    for i in range(2):
        for color in range(3):
            for i in range(int(255 / change)):
                if increase:
                    colors[color] = colors[color] + change
                    if colors[color] > 255:
                        colors[color] = 255
                else:
                    colors[color] = colors[color] - change
                    if colors[color] < 0:
                        colors[color] = 0 #up to this point its mostly code to cycle through the colors

                request = models.ColorTintRequest(
                            data=models.ColorTintRequestData(
                                color_tint=models.ColorTint(
                                    color_r=colors[1],
                                    color_b=colors[2],
                                    color_g=colors[0],
                                ),
                                art_mesh_matcher=models.ArtMeshMatcher(tint_all=True),
                            )
                        )
                await vts.request(request)
            increase = not increase


loop = asyncio.get_event_loop()

async def create_tasks_func():
    tasks = list()
    tasks.append(loop.create_task(rainbow()))
    tasks.append(loop.create_task(spin()))
    await asyncio.wait(tasks)

loop.run_until_complete(create_tasks_func())
loop.close()
