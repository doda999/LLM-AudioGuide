from langchain.chat_models import ChatOpenAI
from langchain.chains import SimpleSequentialChain, LLMChain
from langchain.prompts import PromptTemplate

def get_caption_from_info(title, painter):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

    # 質問LLM
    q_template = """Tell me about the historical or cultural background which influenced {input} and 
    explain briefly about the art techniques and its effects in the picture by mentioning where in the picture each technique is used."""
    q_prompt = PromptTemplate(input_variables=["input"], template=q_template)
    q_chain = LLMChain(llm=chat, prompt=q_prompt)
    
    # 要約LLM
    s_template = """Summarize the sentences below.
    {input}
    """
    s_prompt = PromptTemplate(input_variables=["input"], template=s_template)
    s_chain = LLMChain(llm=chat, prompt=s_prompt)
    
    # 2つのLLMを連結
    seq_chain = SimpleSequentialChain(
        chains=[q_chain, s_chain]
    )
    
    painting = f"{title} by {painter}"
    result = seq_chain(painting)
    return result["output"]