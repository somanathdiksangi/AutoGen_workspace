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

assistance=AssistantAgent(
    name="assitane",
    model_client=model_client,
    system_message="you are helpful assitance "
)

use_agent=UserProxyAgent(
    name="user",
    description="a proxi agent that repretance human",
    input_func=input
)

termination_condition=TextMessageTermination("APPROVE")

team=RoundRobinGroupChat(
    participants=[assistance,use_agent],
    termination_condition=termination_condition
)

stream=team.run_stream(task="write porm about india")

async def main():
    await Console(stream)

if(__name__=="__main__"):
    asyncio.run(main())
