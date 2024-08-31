import openai

from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.llms import ChatMessage

from constants import Constants

openai.api_key = Constants.OPENAI_API_KEY

llm = OpenAI(
    model="gpt-4o",
    temperature=0.5,
    max_tokens=512,
    streaming=True
)

documents = SimpleDirectoryReader("./rag").load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = index.as_retriever()


def check_reset_strings(input_string, keywords):
    return int(any(substring in input_string for substring in keywords))


def run_completion(messages):
    user_query = messages[-1]["content"]
    if check_reset_strings(user_query, Constants.RESET_KEYWORDS_USER):
        return Constants.RESET_MESSAGE, 1
    _messages = [
        ChatMessage(
            role=item['role'],
            content=item['content']
        ) 
        for item in messages
    ]

    nodes = retriever.retrieve(user_query)
    context = "\n".join([node.node.text for node in nodes])
    _messages[0].content = Constants.SYSTEM_PROMPT.replace("{{context}}", context)

    response_text = ""
    response_stream = llm.stream_chat(_messages)
    for response in response_stream:
        response_text += response.delta

    return response_text, check_reset_strings(response_text, Constants.RESET_KEYWORDS_ASSISTANT)


def run_completion_simple(messages):
    user_query = messages[-1]["content"]
    if check_reset_strings(user_query, Constants.RESET_KEYWORDS_USER):
        return Constants.RESET_MESSAGE, 1

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    assistant_text = response.choices[0].message.content
    return assistant_text, check_reset_strings(assistant_text, Constants.RESET_KEYWORDS_ASSISTANT)
