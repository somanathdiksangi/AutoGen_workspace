from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMessageTermination,MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
import asyncio

from dotenv import load_dotenv
load_dotenv()
import os

api_key=os.getenv("GAMINI_API_KEY")
model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-flash-8b",
    api_key=api_key,
)
dsa_solver=AssistantAgent(
    name="dsa_solver",
    model_client=model_client,
    system_message="you give me code in c++ to solve complex dsa problem"
)

code_reviewer=AssistantAgent(
    name="recviewer",
    model_client=model_client,
    system_message="you review the code by the dsa_solver "\
    "is code is crrect please say 'Terminate'"
)
code_editer=AssistantAgent(
    name="code_editer",
    model_client=model_client,
    system_message="you make the code easy to understand and add comment of the code "\
    "is code is crrect please say 'Terminate'"

) 

team=RoundRobinGroupChat(
    participants=[dsa_solver,code_reviewer,code_editer],
    max_turns=1
)


async def main():
    task="write a code for printing hello word"
    while True:
     stream=team.run_stream(task=task)
     await Console(stream)
     feedback=input("give me a feedback if you want to exit please enter exit keyword")
     
     if(feedback.lower().strip()=='exit'):
        break
    task=feedback

if(__name__=="__main__"):
    asyncio.run(main())
