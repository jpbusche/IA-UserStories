import ollama
from src.settings import MODEL


class UserStories:

    QUESTION = """
        Thinking like a scrum master and experienced developer, your job is to create a list of atomic user stories for the development of a project. 
        User stories should cover all required functionality and should be written in the format: 'As a [type of user], I want [action], so that [benefit]'. 
        Make sure stories are independent, testable and have business value. 
        The answer need to be in the list format, with only the text of the user stories and only the user stories. Also the answer need to be in english.
    """

    PROMPT = """
        {question}
        
        Context: {context}

        Example of Answer:
        1. As a customer, I want to register in the store, so that I can save my details for future purchases.
        2. As an administrator, I want to add new products to the catalog so that customers can find them.
        3. As a customer, I want to add a product to my shopping cart so that I can checkout later.
    """

    REVIEWER_PROMPT = """
        Thinking like a scrum master ans experienced developer, your job is to review this list of user stories, remove any duplicate or 
        any user stories outside the context and if necessary, divide into more atomic user stories. 
        User stories should be written in the format: 'As a [type of user], I want [action], so that [benefit]'. 
        Make sure stories are independent, testable and have business value. 
        The answer need to be in the list format, with only the text of the user stories and only the user stories. Also the answer need to be in english.

        List of User Stories: {context}

        Example of Answer:
        1. As a customer, I want to register in the store, so that I can save my details for future purchases.
        2. As an administrator, I want to add new products to the catalog so that customers can find them.
        3. As a customer, I want to add a product to my shopping cart so that I can checkout later.
    """

    def format_prompt(self, context):
        return self.PROMPT.format(question=self.QUESTION, context=context)
    
    def get_question(self):
        return self.QUESTION

    def generate_user_stories(self, context):
        message = {'role': 'user', 'content': self.format_prompt(context)}
        pre_response = ollama.chat(model=MODEL, messages=[message])
        reviewer_message = {'role': 'user', 'content': self.REVIEWER_PROMPT.format(context=pre_response['message']['content'])}
        response = ollama.chat(model=MODEL, messages=[reviewer_message])
        return response['message']['content']