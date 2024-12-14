from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from ..models.o1_loader import O1ModelLoader

def create_base_chain():
    llm = O1ModelLoader()
    prompt = PromptTemplate(
        input_variables=["query"],
        template="Please process the following query: {query}"
    )
    return LLMChain(llm=llm, prompt=prompt)
