import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from helpers import TemperatureMap

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

temp_map = TemperatureMap()


@app.get("/", include_in_schema=False)
async def redirect_to_heatmap():
    return RedirectResponse(url="/heatmap")


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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")), log_config=None)
