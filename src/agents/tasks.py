import ollama
import re
from src.settings import MODEL
from src.agents.agent import Agent


class Tasks(Agent):

    QUESTION = """
        From previous context and thinking like an experienced developer, your job is to divide the following user storie, from a certain context, in smalls, atomics, testables and independents tasks.
        User Storie: {user_storie}
        Tasks should cover all required functionality and should be written in the format: 'Task [number] - [action]'. 
        Make sure that the tasks follows this aspects:
        - Atomic: Each tasks need to be the smaller unit of work possible.
        - Independent: Each tasks don't need to depend from others tasks.
        - Testable: Each tasks need to be testable by the responsable developer.
        - Clarety: Each tasks need to be described clearly and objectively
        The answer need to be in the list format and the answer need to be in english.
    """

    REVIEWER_PROMPT = """
        Thinking like an experienced developer, your job is to review this list of tasks, remove any duplicate or 
        any tasks outside the context and if necessary, divide into more atomic tasks. 
        Tasks should be written in the format: 'Task [number] - [action]'. 
        Make sure that the tasks follows this aspects:
        - Atomic: Each tasks need to be the smaller unit of work possible.
        - Independent: Each tasks don't need to depend from others tasks.
        - Testable: Each tasks need to be testable by the responsable developer.
        - Clarety: Each tasks need to be described clearly and objectively 
        The answer need to be in the list format, with only the text of the tasks and only the tasks. Also the answer need to be in english.

        List of tasks: {context}

        Examples:
        Task 1 - Create the table on database to store informations of the product.
        Task 2 - Implement the function to clean the search bar.
        Task 3 - Create the API endpoint to receive the search requisitions.
    """

    PROMPT = """
        Context: {context}
        
        {question}
        
        Examples:
        Task 1 - Create the table on database to store informations of the product.
        Task 2 - Implement the function to clean the search bar.
        Task 3 - Create the API endpoint to receive the search requisitions.
    """

    TASK_REGEX = r"^Task \d{1,3} - (?P<task>.+)"

    def format_question(self, user_storie):
        self.QUESTION = self.QUESTION.format(user_storie=user_storie)

    def generate_response(self, context):
        tasks = []
        message = {'role': 'user', 'content': self.format_prompt(context)}
        pre_response = ollama.chat(model=MODEL, messages=[message])
        reviewer_message =  {'role': 'user', 'content': self.REVIEWER_PROMPT.format(context=pre_response['message']['content'])}
        response = ollama.chat(model=MODEL, messages=[reviewer_message])
        lines = response["message"]["content"].split('\n')
        for line in lines:
            regex = re.search(self.TASK_REGEX, line)
            if regex:
                tasks.append(regex.group('task'))
        return tasks