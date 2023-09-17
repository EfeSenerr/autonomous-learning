# Autonomous Learning

Repo of the practical course named "IT-Based Learning" at Technical University of Munich (TUM).

## Abstract of our paper

In a rapidly digitizing world, the significance of Information Technology (IT) and digital solutions is evident in driving societal and economic transfor-mations.

This paper discusses the importance of equipping the next generation with programming knowledge and addresses the challenges educational institutions face in updating their curriculum to match the pace of AI advancements.
The paper introduces "Autonomous Learning", an educational software that utilizes AI to teach basic programming skills.
By enabling users to express coding concepts in natural language, which is then translated into Python code, the software offers an innovative approach to learning.

This approach not only simplifies the introduction to programming but also teaches handling large language models, specifically GPT-4.
The game's objectives are mapped using Bloom's Taxonomy, ensuring a structured and progressive learning experience.
The backend is driven by the FastAPI and OpenAI's GPT-4 model, ensuring efficient translation of natural language in-to code.
Feedback from high school students during a pilot test provided val-uable insights into the software's effectiveness and potential areas of im-provement.

## Backend of this project

- main.py: This is the entry point of the backend and is responsible for API end-point definitions. It imports the Python modules, saves the levels, and sets up FastAPI.
- translate.py: It holds the translate function that uses GPT-4 to translate natural language into Python code. A detailed prompt is given, which provides context for the model. We believe that the ability to translate natural language into Python code significantly lowers the entry barrier for new learners.
- evaluate.py: The file contains the evaluate function, which takes Python code and a maze configuration as inputs. It utilizes helper functions from the func-tions.py to execute the code within the maze and checks if the endpoint is reached. Helper functions are pre-defined so that the execut-ed code can fail only if the input code is wrong. So, we expect users to use these helper functions to solve the maze problem. The executed function will help the user move in the maze to reach the endpoint. If the endpoint is reached, the player can continue to the next level. If not, the player has to start from the beginning to solve the problem.
- functions.py: This file contains utility functions like detect_wall, go_forward, turn_left, and turn_right that are used in the code evalua-tion process. The users are expected to use these functions.
- pseudo_lang.txt: Defines a formal pseudo language that serves as a guide for translating natural language to Python code. We expect users to use this pseudo language, instead of the natural language, in the more chal-lenging levels of the game. You can find more information on this pseu-do language in the previous section.

## Frontend of this project

The technological foundation of the frontend relies on the combination of HTML, CSS, and Javascript. The Three.js library was used for the 3D representa-tion. Despite our experience with the basics of Javascript, HTML, and CSS, choosing between Javascript 3D libraries such as Three.js, Babylon.js, D3.js, and WebGL posed a new challenge. The decision was eventually made in favor of Three.js, based on the availability of an open-source skeleton for a maze game.

For more information, you can read our paper.
