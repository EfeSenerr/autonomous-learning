import os
import openai
from dotenv import load_dotenv
import re

def evaluate(code, maze):
    # Here is where you will evaluate the code and return the results
    # start bottom right, end top left
    start = (2 ,2)
    end = (5, 5)
    path_taken =  [(5, 5), (4, 5), (3, 5), (2, 5), (2, 4), (2, 3), (2 ,2)]
    namespace = {'maze': maze, 'start': start, 'end': end}
    #exec(code, {}, namespace)
    # result = namespace["result"]
    result = False
    
    # Call to OpenAI to get the feedback and score
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]
    # openai.organization_id = os.environ["ORGANIZATION_ID"]
    with open("pseudo_lang.txt", "r", encoding="utf-8") as file:
        pseudo_structure = file.read()
    with open("pseudo_lang_2.txt", "r", encoding="utf-8") as file:
        pseudo_structure_2 = file.read()

    # OpenAI API call
    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing feedback and a score for the given python code."},
            {"role": "user", "content": f"I am going to give you a python code which was previously translated from the pseudo code, so it is also normal that there is no comment in the code. Assume that the defined functions without the code inside are defined correctly and working correctly. Focus on the usage & results of the functions. Main goal of this code is the player in the car tries to travel from start point {start} to end point {end} in this specific maze: {maze}. This code is not a general algorithm, but a specific one to solve this maze. One direction forward means going from (5, 5) to (4, 5)."},
            {"role": "assistant", "content": "I understand. The player tries to get from the start point to the end point in the maze. I will assume that the defined functions are implemented corretly and focus on the usage of the functions and results of these functions."},
            {"role": "user", "content": f"Please provide a short feedback and a score (0-100) of the given code. Also try to understand if the player can get from start point to end point using that python code and provide a percentage of success. Example solution would seems like this {path_taken}. At the end of the feedback, write the path that the player took executing the python code. Give the answer so that I will extract them as 'Score:\s*(\d+)', 'Feedback:\s*(.*)' and 'Percentage:\s*(\d+)'."},
            {"role": "assistant", "content": "I will give a short feedback, a score out of 100 and a success percentage of the player for the given code. Please provide the Python code."},
            {"role": "user", "content": f"Here is the Python code: {code}"},
        ]
    )

    # MVP response
    # response = openai.ChatCompletion.create(
    # model="gpt-4",
    # messages=[
    #         {"role": "system", "content": "You are a helpful assistant understanding pseudo language."},
    #         {"role": "user", "content": f"In the future I want you to understand the given pseudo code. This is the structure of the pseudo code that will be given: {pseudo_structure_2}"},
    #         {"role": "assistant", "content": "Thanks for the pseudo code structure."},
    #         {"role": "user", "content": f"Main goal is that a game is being played. The player's car is in a maze, the start point is {start}, end point is {end}, the maze is {maze}.'0' being walls and '1' being walkable paths. Main goal of the game: player writes a pseudo code so that the car drives from the start point to end point for this specific maze. This code is not a general algorithm, but a specific one to solve this maze."},
    #         {"role": "assistant", "content": "I understand. The player tries to get from the start point to the end point in the maze. The player writes a pseudo code to do so."},
    #         {"role": "user", "content": f"This is the {code}. Please provide a short feedback and a score (0-100) of the given pseudo code, considering the start point '{start}', end point '{end}' and the maze '{maze}'is given. One direction forward means going from (5, 5) to (4, 5). Also try to understand if the player can get from start point to end point using that code and provide a percentage of success. Example solution would seems like this {path_taken}. At the end of the feedback, write the path that the player took given the pseudo code, even tough it might be wrong. Give the answer so that I will extract them as 'Score:\s*(\d+)', 'Feedback:\s*(.*)' and 'Percentage:\s*(\d+)'."},
    #         #{"role": "user", "content": f"Translate this code to python, keep the code simple and understandable, also write start and end points and the maze itself in the python code so that it would work by itself. At first define the functions and then comment '#Translated Pseudo Code' and translate the code in python. At the end print the result. Example solution would seems like this {path_taken}. Just give the converted python code as the result so that I can extract it like this '```python(.*?)```': {code}"},

    #     ]
    # )

    # TODO: Maze as 2d input
    ## Mock response
    # response = openai.ChatCompletion.create(
    # model="gpt-4",
    # messages=[
    #         {"role": "system", "content": "You are a helpful assistant understanding pseudo language."},
    #         {"role": "user", "content": f"In the future I want you to understand the given pseudo code. This is the structure of the pseudo code that will be given: {pseudo_structure}"},
    #         {"role": "assistant", "content": "Thanks for the pseudo code structure."},
    #         {"role": "user", "content": f"The player's car is in a maze, the start point is {start}, end point is {end}, the maze is {maze}.'0' being walls and '1' being walkable paths. Main goal of the game: player writes a pseudo code so that the car drives from the start point to end point for this specific maze. This code is not a general algorithm, but a specific one to solve this maze. This is the {code}. Please provide a short feedback and a score (0-100) of the given pseudo code, considering the start point '{start}', end point '{end}' and the maze is given. One direction forward means going from (5, 5) to (4, 5). Also try to understand if the player can get from start point to end point using that code and provide a percentage of success. Example solution would seems like this {path_taken}. At the end of the feedback, write the path that the player took given the pseudo code, even tough it might be wrong. Give the answer so that I will extract them as 'Score:\s*(\d+)', 'Feedback:\s*(.*)' and 'Percentage:\s*(\d+)'."}, 
    #         #{"role": "user", "content": f"Translate this code to python, keep the code simple and understandable, also write start and end points and the maze itself in the python code so that it would work by itself. At first define the functions and then comment '#Translated Pseudo Code' and translate the code in python. At the end print the result. Example solution would seems like this {path_taken}. Just give the converted python code as the result so that I can extract it like this '```python(.*?)```': {code}"},

    #     ]
    # )

    # Extract the answer from the API response
    answer = response['choices'][0]['message']['content']

    # Extract the score and feedback from the answer
    score_pattern = re.compile(r'Score:\s*(\d+)', re.IGNORECASE)
    feedback_pattern = re.compile(r'Feedback:\s*(.*)', re.IGNORECASE)
    percentage_pattern = re.compile(r'Percentage:\s*(\d+)', re.IGNORECASE)

    score_match = score_pattern.search(answer)
    feedback_match = feedback_pattern.search(answer)
    percentage_match = percentage_pattern.search(answer)

    if score_match:
        score = int(score_match.group(1))
    else:
        score = 31  # TODO: Handle this error

    if percentage_match:
        percentage = int(percentage_match.group(1))
    else:
        percentage = 31  # TODO: Handle this error

    if feedback_match:
        feedback = feedback_match.group(1).strip()
    else:
        feedback = "No feedback ^^"  # TODO: Handle this error

    # Add the percentage to the feedback
    feedback += f" Percentage of success: {percentage}%"

    # score = 100
    # feedback = "Nice work!"

    return result, score, feedback, path_taken