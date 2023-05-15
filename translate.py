import os
import openai
from dotenv import load_dotenv
import re

primer = """os.environ["maze"] = "maze"]"""

# Takes code as a string and returns the translated python code
def translate(code, maze):
    start = (2 ,2)
    end = (5, 5)
    path_taken =  [(5, 5), (4, 5), (3, 5), (2, 5), (2, 4), (2, 3), (2 ,2)]
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]
    # openai.organization_id = os.environ["ORGANIZATION_ID"]

    #Here is where  the code is translated from pseudo-code to python
    #Primed the model with understanding the language
    #TODO Translate the maze to python which can then be used in exec() in evaluate.py

    # Read the content of the "pseudo_lang.txt" file
    with open("pseudo_lang.txt", "r", encoding="utf-8") as file:
        pseudo_structure = file.read()
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
            {"role": "system", "content": """You are a helpful translator that translates a from pseudo language to python language to generically solve a maze. Return the python code so that I can extract it like this '```python(.*?)```'."""},
            {"role": "user", "content": f"""This is the structure of the pseudo code that will be given: {pseudo_structure_2}. 
            The user is in a maze, the start point is {start}, end point is {end}, the maze looks similiar to this {maze}.'0' being walls and '1' being walkable paths.
            Main goal of the game: player writes a pseudo code so that the player walks from the start point to end point.
            Convert the following pseudo code into generic python and package it into a function called execute_labyrinth() that returns the path that the pseudo instructions take and has the following format: {path_taken}. 
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