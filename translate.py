import os
import openai
from dotenv import load_dotenv
import re

primer = """os.environ["maze"] = "maze"]"""

# Takes code as a string and returns the translated python code
def translate(code, maze):
    # Extract the map
    map_part = maze[0]['map']
    # Now map_part contains the map array
    print(map_part)

    end = (2 ,2)
    start = (5, 5)
    path_taken =  [(5, 5), (4, 5), (3, 5), (2, 5), (2, 4), (2, 3), (2 ,2)]
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]
    # openai.organization_id = os.environ["ORGANIZATION_ID"]

    parameters = f"""start_point = {start}
end_point = {end}
maze = {map_part}
current_position = start_point
direction = "up"
result = []
result.append(current_position)
"""

    #Here is where  the code is translated from pseudo-code to python
    #Primed the model with understanding the language
    #TODO Translate the maze to python which can then be used in exec() in evaluate.py

    # Read the content of the "pseudo_lang.txt" file
    with open("pseudo_lang_2.txt", "r", encoding="utf-8") as file:
        pseudo_structure_2 = file.read()
    with open("functions.txt", "r", encoding="utf-8") as file:
        functions_predefined = file.read()

    # test_code = "while ($i < 8) { print($i); $i++; } name2 = "Max";"
    # OpenAI API call

    # General response
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": """You are a helpful translator that translates a from pseudo language to python language to generically solve a maze."""},
            {"role": "user", "content": f"""This is the structure of the pseudo code that will be given: {pseudo_structure_2}. 
            The user is in a maze, the start point is {start}, end point is {end}, the maze looks similiar to this {map_part}.'0' being walls and '1' being walkable paths.
            The main goal of the game is to use pseudo code to guide a player from the start point to the end point in a maze. I also have these predefined python functions that correspond to the commands in the pseudo code: {functions_predefined}.
            Please convert the following pseudo code into python. Due to the execution time, I don't need the full execution script, just the translated part. 
            Package the converted python code and return the path in a variable called 'result' which will return the path that the pseudo instructions take and has the following format: {path_taken}. 
            Later I will add the predefined functions at the beginning of the script like this {parameters}, which will be executed. 
            Just return the python code so that I can extract it like this '```python(.*?)```'. This is the pseudo code: {code}
            """},
        ]
    )
    #You have these predefined functions available: {functions_predefined}.
    # Extract the answer from the API response
    answer = response['choices'][0]['message']['content']
    print(answer)

    # Extract the Python code from the output
    code_pattern = re.compile(r'```python(.*?)```', re.DOTALL)
    python_code = code_pattern.search(answer)
    if python_code:
        extracted_code = python_code.group(1).strip()
    else:
        extracted_code = "" #TODO Handle this error

    return extracted_code