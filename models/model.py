from interface.llmService import LlmService
class model(LlmService):
    def __init__(self):
        super().__init__()
        #self.llm=chose your model
    def prompt(self,method:str):
        #self.llm.send 