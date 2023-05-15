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
            {"role": "system", "content": "You are a helpful assistant converting pseudo language to python language."},
            {"role": "user", "content": f"In the future I want you to convert the given pseudo code in python language. This is the structure of the pseudo code that will be given: {pseudo_structure_2}. And also consider this structure to see how to translate the code to python: {pseudo_structure} "},
            {"role": "assistant", "content": "Thanks for the pseudo code structure. I will use it to convert the given pseudo code to python code."},
            {"role": "user", "content": f"Main goal is that a game is being played. The user is in a maze, the start point is {start}, end point is {end}, the maze is {maze}.'0' being walls and '1' being walkable paths. Main goal of the game: player writes a pseudo code so that the player walks from the start point to end point for this specific maze."},
            {"role": "assistant", "content": "I understand. The player tries to get from the start point to the end point in the maze. The player writes a pseudo code to do so. I will convert the pseudo code to python code considering this."},
            {"role": "user", "content": f"Translate this code to python, use these predefined functions: {functions_predefined}. Keep the code simple and understandable, also write start and end points and the maze itself in the python code. Just define the functions without writing the code and assume that they will work fine and then comment '#Translated Pseudo Code' and translate the code in python. At the end print path the player has to take as the result. Example solution would seems like this {path_taken}. Just give the converted python code so that I can extract it like this '```python(.*?)```': {code}"},
            #{"role": "user", "content": f"Translate this code to python, keep the code simple and understandable, also write start and end points and the maze itself in the python code so that it would work by itself. At first define the functions and then comment '#Translated Pseudo Code' and translate the code in python. At the end print the result. Example solution would seems like this {path_taken}. Just give the converted python code as the result so that I can extract it like this '```python(.*?)```': {code}"},

        ]
    )


    
    # Extract the answer from the API response
    answer = response['choices'][0]['message']['content']

    # Extract the Python code from the output
    code_pattern = re.compile(r'```python(.*?)```', re.DOTALL)
    python_code = code_pattern.search(answer)
    if python_code:
        extracted_code = python_code.group(1).strip()
    else:
        extracted_code = "" #TODO Handle this error

    return extracted_code