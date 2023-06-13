from typing import List
from fastapi import FastAPI, Request, Body
import sys
sys.path.append('..')
from evaluate import evaluate
from translate import translate
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="three-maze")
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["http://localhost:9000", "localhost:9000"]

# origins = [
#     "https://it-learning-programming.vercel.app/",
#     "it-learning-programming.vercel.app"
# ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/codecheck")
async def codecheck(maze_id: int = Body(...), code: str = Body(...)):
    maze = await get_maze(maze_id)
    translated_pseudo_code = translate(code, maze)
    result, score, feedback, path_taken = evaluate(
        translated_pseudo_code, maze
    )
    return {
        "result": result, #Boolean, True if the maze was solved
        "score": score, #Integer, score from 0 to 100
        "feedback": feedback, #String, feedback from the evaluation
        "path_taken": path_taken, #List of tuples, the path taken by the algorithm [(1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4)]
        "translated_pseudo_code": translated_pseudo_code, #String, the translated pseudo code,
        "code": code #String, the original cod
    }


@app.get("/maze/{maze_id}")
async def get_maze(maze_id: int):
    return mock_mazes[maze_id]

#Mock for testing of UI
@app.post("/mock_codecheck")
async def codecheck(maze_id: int = Body(...), code: str = Body(...)):

    #Test Backend
    maze = await get_maze(maze_id) # await added
    translated_pseudo_code = translate(code, maze)
    result, score, feedback, path_taken = evaluate(
        translated_pseudo_code, maze
    )
    ###
    return {
            "result": result, # False, #Boolean, True if the maze was solved
            "score": score, #Integer, score from 0 to 100
            "feedback": feedback, #"You did well on the labyrinth, but you can improve a lot in Area X", #String, feedback from the evaluation
            "path_taken": path_taken, #[(5, 5), (4, 5), (3, 5), (2, 5), (2, 4), (2, 3), (2 ,2)], #List of tuples, the path taken by the algorithm [(1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4)]
            "translated_pseudo_code": translated_pseudo_code, #String, the translated pseudo code,
            "code": code #String, the original code
        }

mock_mazes = [

    [
        { # 1
            "map": [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0], # start point is always right bottom corner
                [0, 0, 0, 0, 0],
            ],
            "side": 4,
            "end_x": 3, # You can do it like this for the rest of the mazes
            "end_y": 2,
            "start": (3, 3),
            "end": (3, 2),
            "animation_x": -1,
            "animation_y": 0,
        }
    ],
    [
        { # 2
            "map": [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 1, 0], # start point is always right bottom corner
                [0, 0, 0, 0, 0],
            ],
            "side": 4,
            "end_x": 2, # You can do it like this for the rest of the mazes
            "end_y": 2,
            "start": (3, 3),
            "end": (2, 2),
            "animation_x": 0,
            "animation_y": 0,
        }
    ],
    [
        { # 3
            "map": [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 0, 1, 0], # start point is always right bottom corner
                [0, 0, 0, 0, 0],
            ],
            "side": 4,
            "end_x": 2, # You can do it like this for the rest of the mazes
            "end_y": 2,
            "start": (3, 3),
            "end": (2, 2),
            "animation_x": 0,
            "animation_y": 0,
        }
    ],
    [  
        { # 4
            "map": [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
            "side": 6, #size of the maze - 1
            "end_x": 2,
            "end_y": 5,
            "start": (5, 5),
            "end": (2, 5),
            "animation_x": 1,
            "animation_y": -2,
        }
    ],
    [ 
        { # 5
            "map": [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
            "side": 6, #size of the maze - 1
            "end_x": 4,
            "end_y": 3,
            "start": (5, 5),
            "end": (3, 2),
            "animation_x": 1,
            "animation_y": 1,
        }
    ],
    [ 
        { # 6
            "map": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "side": 8, #size of the maze - 1
            "end_x": 5,
            "end_y": 4,
            "start": (7, 7),
            "end": (5, 4),
            "animation_x": -1,
            "animation_y": 0,
        }
    ],
    [
        {
            "map": [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
            "side": 6,
            "end_x": 2,
            "end_y": 2,
            "start": (5, 5),
            "end": (2, 2),
            "animation_x": 1,
            "animation_y": 1,
        }
    ],


]
