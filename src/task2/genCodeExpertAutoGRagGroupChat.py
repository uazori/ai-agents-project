import os
import autogen

from typing_extensions import Annotated
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from dotenv import load_dotenv
from dotenv import find_dotenv
from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent
from fileTools import list_files_recursive
from fileTools import create_test_file_from_code
from fileTools import remove_texts
from fileTools import remove_texts_with_line
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.contrib.vectordb.chromadb import ChromaVectorDB
# Accepted file formats for that can be stored in
# a vector database instance
from autogen.retrieve_utils import TEXT_FORMATS



print("Loading environment variables...")
load_dotenv(find_dotenv(),verbose=True)
print("Environment variables loaded.")
file_path = "/Users/vadymo/code/chessrating/chess-rating-server/"
fileFormat = [".java"]
nameNotHasText = ["Test"]
name_has_text = ["Imp"]
filesList = list_files_recursive(file_path,fileFormat,nameNotHasText,name_has_text)
for codeFilePath in filesList:
        if "PlayerServiceImp.java" in codeFilePath:
            filesList=[codeFilePath]
            break
for file in filesList:
    print("file - ", file)



llm_config = {
    "config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}],
}
# llm_config = {
#     "config_list": [{"model": "moonshotai/Kimi-K2-Instruct", "api_key": os.environ["HF_TOKEN"]}],
# }


def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

reviwerMsg = """You are a code reviewer, review code of unit test providev by Senior Java Engineer, and add advice to extend test.
You need to improve the quality of the unit tests and give recommendations, based on the following criteria:
- Make sure code is compileable and runnable
- Ensure that the tests cover all possible edge cases
- Ensure that the tests are meaningful and actually test the functionality of the code
- Ensure that the tests are easy to read and understand
- Ensure that the tests are maintainable and easy to modify in the future
- Ensure that the tests follow best practices for unit testing
- Usage of mocks and meaningful data (add context about dependencies) 
- Provide good samples depending on the file type (controller, service, repository code samples) """

codeReviewer = autogen.AssistantAgent(
    name="Code_Reviewer",
    is_termination_msg=termination_msg,
    system_message=reviwerMsg,
    llm_config=llm_config,
    description="Code Reviewer who can review the code.",
)

developerMsg = """You are a java developer you write code with unit test. Reviewer will review code.
 Modify code according reviewer recomendation.Return only code, no other text."""

coder = autogen.AssistantAgent(
    name="Senior_Java_Engineer",
    is_termination_msg=termination_msg,
    system_message=developerMsg,
    llm_config=llm_config,
    description="Senior Java Engineer who can write code to solve problems and answer questions.",
)

seniorDeveloper = RetrieveUserProxyAgent(
    name="Senior_Developer",
    human_input_mode="NEVER",
    is_termination_msg=termination_msg,
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "code",
        "docs_path": filesList,
        "chunk_token_size": 2000,
        "model": "gpt-3.5-turbo",
        "vector_db": "chroma",
        "overwrite": True,  # set to True if you want to overwrite an existing collection
        "get_or_create": True,  # set to False if don't want to reuse an existing collection
    },
    code_execution_config=False, 
    description="Senior Engineer who can write code to solve problems and answer questions.", # set to False if you don't want to execute the code
)

PROBLEM = "PLease create tests for PlayerServiceImpl.java class"
# reset the assistant. Always reset the assistant before starting a new conversation.
def _reset_agents():
    codeReviewer.reset()
    coder.reset()
    seniorDeveloper.reset()

def rag_chat():
    _reset_agents()
    groupchat = autogen.GroupChat(
        agents=[seniorDeveloper, coder ,codeReviewer], messages=[], max_round=5, speaker_selection_method="round_robin"
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with boss_aid as this is the user proxy agent.
    chat_result = seniorDeveloper.initiate_chat(
        manager,
        message=seniorDeveloper.message_generator,
        problem=PROBLEM,
        n_results=5,
    )
    final_message = chat_result.chat_history[-1]
    print("final message:", final_message)
    for codeFilePath in filesList:
        if "PlayerServiceImp.java" in codeFilePath:
            resCleanCode = remove_texts_with_line(final_message,["```java","```"])
            create_test_file_from_code (codeFilePath,resCleanCode,"java")
            print("test file generated:")


rag_chat()