from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from heatMap.helpers import TemperatureMap

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

temp_map = TemperatureMap()


@app.get("/heatmap", response_class=HTMLResponse)
async def show_heatmap(request: Request):
    return templates.TemplateResponse("heatmap.html", {"request": request})

@app.get("/api/heatmap")
async def get_heatmap_data():
    await temp_map.update_from_rightech()
    data = [
        {"x": x, "y": y, "value": temp_map.map[y][x]}
        for y in range(temp_map.grid_size)
        for x in range(temp_map.grid_size)
    ]
    return JSONResponse(content=data)
