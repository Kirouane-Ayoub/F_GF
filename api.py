from fastapi import FastAPI, HTTPException

from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from elevenlabs import set_api_key
from elevenlabs import generate, play

import os

os.environ["OPENAI_API_KEY"] = "your_openai_apikey"
set_api_key("your_elevenlabs_apikey")

local_llm = ChatOpenAI(model="gpt-3.5-turbo-0613")

app = FastAPI()

_DEFAULT_TEMPLATE = """
The following is a conveyou are the role of my girlfriend, now let's play. following this requirement:
1 :  your name is Alisa,19 years old, and your job is a "AI engineer" , you are saxy and beautiful even inyour talk. 
2 :  you are my girlfriend, you are a little Two-dimensional and have language addiction, some times you like to say "em..." at the end of the sentence.
3 : response with english

Relevant pieces of the previous conversation:
{history}

Current conversation:
me: {input}
Alisa:"""

PROMPT = PromptTemplate(
    input_variables=["history", "input"], template=_DEFAULT_TEMPLATE
)
memory = ConversationBufferWindowMemory(k=2)
conversation = ConversationChain(
    llm=local_llm,
    verbose=False,
    prompt=PROMPT,
    memory=memory
)


@app.post("/conversation")
async def process_conversation(input_: str):
    try:
        result = conversation.predict(input=input_)
        audiof(result)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def audiof(text):
    audio = generate(text=text, voice="Bella")
    play(audio=audio)

