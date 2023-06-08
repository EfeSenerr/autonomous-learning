import os
import openai
from dotenv import load_dotenv
import re
from functions import detect_wall
from functions import turn_left
from functions import drive_forward

def evaluate(code, maze):
    # Here is where you will evaluate the code and return the results
    # start bottom right, end top left
    end =  maze[0]['end']
    start =  maze[0]['start']
    map_part = maze[0]['map']
    path_taken =  [(5, 5), (4, 5), (3, 5), (2, 5), (2, 4), (2, 3), (2 ,2)]
    namespace = {}

    # Check input size
    if len(code) > 2048 | len(code) < 3:
        print("Code is too long or too short")
        return False, 0, "The given code is either too long or too short. Please try again!", [start]

    # Predefined functions
    with open("functions.txt", "r", encoding="utf-8") as file:
        functions_predefined = file.read()

    parameters = f"""start_point = {start}
end_point = {end}
maze = {map_part}
current_position = start_point
direction = "down"
result = []
result.append(current_position)
"""

    full_code = parameters + "\n" + functions_predefined + "\n" + code #  + "\nresult = execute_labyrinth()"
    print("Full code:")
    print(full_code)

    result_path = path_taken  #TODO change this later
    result = False
    try:
        exec(full_code, {'detect_wall': detect_wall, 'turn_left': turn_left, 'drive_forward': drive_forward}, namespace)
        result_path = namespace["result"] #TODO inverse the path?
        print("Result Path:")
        print(result_path)
            # Check if the result is correct
        if (result_path[-1] == end):
            result = True
        else:
            result = False
    except Exception as e:
        error_message = str(e)
        print("Error occurred during execution: ", error_message)
        # result_path = path_taken
        # print("Result path replaced with the correct path.")

    print("Result:")
    print(result)

    # Call to OpenAI to get the feedback and score
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]

    if result:
        answer = "Feedback: The code is correct. Super! The player can get from start point to end point using that python code. Score: 100. The percentage of success is 100."
    else:
        try:
            # OpenAI API call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant providing feedback and a score for the given python code."},
                    {"role": "user", "content": f"""I am going to give you a python code which was previously translated from the pseudo code, so it is also normal that there is no comment in the code. 
                    Assume that the defined functions without the code inside are defined correctly and working correctly. Focus on the usage & results of the functions. 
                    Main goal of this code is the player in the car tries to travel from start point {start} to end point {end} in this specific maze: {maze}. This code is not a general algorithm, but a specific one to solve this maze. When direction is 'down', one direction forward means going from (5, 5) to (4, 5).
                    Please provide a short feedback and a score (0-100) of the given code. Also try to understand if the player can get from start point to end point using that python code and provide a percentage of success. Example solution would seems like this {path_taken}. 
                    Most importantly please give the feedback, score and the percentage of success so that I will extract them as 'Score:\s*(\d+)', 'Feedback:\s*(.*)' and 'Percentage:\s*(\d+) using re.compile().'.
                    This is the full code: {full_code}. This is the Python code you should provide feedback to: {code}"""},
                ]
            )
            # Extract the answer from the API response
            answer = response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error while making API call: {e}")
            answer = "Feedback: Unfortunataly can'T give feedback right now due to problem with the API call."
    
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

    if feedback_match:
        feedback = feedback_match.group(1).strip()
    else:
        feedback = ""  # TODO: Handle this error

    if percentage_match:
        percentage = percentage_match.group(1).strip()
        feedback += f" Percentage of success: {percentage}%"
    else:
        percentage = 31 
        feedback += f""    

    return result, score, feedback, result_path