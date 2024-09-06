class Agent:

    def format_prompt(self, context):
        return self.PROMPT.format(question=self.QUESTION, context=context)
    
    def get_question(self):
        return self.QUESTION

    def generate_response(self, context):
        raise NotImplementedError()