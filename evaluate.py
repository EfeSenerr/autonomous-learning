import os
import openai
from dotenv import load_dotenv
import re

def evaluate(code, maze):
    # Here is where you will evaluate the code and return the results
    # start bottom right, end top left
    start = (2 ,2)
    end = (5, 5)
    map_part = maze[0]['map']
    path_taken =  [(5, 5), (4, 5), (3, 5), (2, 5), (2, 4), (2, 3), (2 ,2)]
    namespace = {'maze': maze, 'start': start, 'end': end}
    
    # Predefined functions
    with open("functions.txt", "r", encoding="utf-8") as file:
        functions_predefined = file.read()

    parameters = f"""start_point = {start}
end_point = {end}
maze = {map_part}
current_position = start_point
direction = "up"
"""

    full_code = parameters + "\n" + functions_predefined + "\n" + code #  + "\nresult = execute_labyrinth()"
    print("Full code:")
    print(full_code)

    result_path = path_taken  #TODO change this later
    try:
        exec(full_code, {}, namespace)
        result_path = namespace["result"]
        print("Result Path:")
        print(result_path)
    except Exception as e:
        error_message = str(e)
        print("Error occurred during execution: ", error_message)
        # result_path = path_taken
        # print("Result path replaced with the correct path.")

    # Check if the result is correct
    if (result_path[0] == end):
        result = True
    else:
        result = False
    
    # Call to OpenAI to get the feedback and score
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # OpenAI API call
    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing feedback and a score for the given python code."},
            {"role": "user", "content": f"I am going to give you a python code which was previously translated from the pseudo code, so it is also normal that there is no comment in the code. Assume that the defined functions without the code inside are defined correctly and working correctly. Focus on the usage & results of the functions. Main goal of this code is the player in the car tries to travel from start point {start} to end point {end} in this specific maze: {maze}. This code is not a general algorithm, but a specific one to solve this maze. One direction forward means going from (5, 5) to (4, 5)."},
            {"role": "assistant", "content": "I understand. The player tries to get from the start point to the end point in the maze. I will assume that the defined functions are implemented corretly and focus on the usage of the functions and results of these functions."},
            {"role": "user", "content": f"Please provide a short feedback and a score (0-100) of the given code. Also try to understand if the player can get from start point to end point using that python code and provide a percentage of success. Example solution would seems like this {path_taken}. Most importantly please give the feedback, score and the percentage so that I will extract them as 'Score:\s*(\d+)', 'Feedback:\s*(.*)' and 'Percentage:\s*(\d+)'."},
            {"role": "assistant", "content": "I will give a short feedback, a score out of 100 and a success percentage of the player for the given code. Please provide the Python code."},
            {"role": "user", "content": f"Here is the Python code: {code}"},
        ]
    )

    # Extract the answer from the API response
    answer = response['choices'][0]['message']['content']
    print("Answer from OpenAI - Feedback:")
    print(answer)

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