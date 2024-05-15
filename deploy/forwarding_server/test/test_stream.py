# It's a test file! Not for use!
import time
from openai import Client
# Example of an OpenAI ChatCompletion request with stream=True
# https://platform.openai.com/docs/api-reference/streaming#chat/create-stream

# record the time before the request is sent
start_time = time.time()

# target output client
# client = Client(base_url="http://localhost:9879/v1", api_key="lm-studio")
# test output client
client = Client(base_url="http://localhost:9880/v1", api_key="lm-studio")



# send a ChatCompletion request to count to 100
response = client.chat.completions.create(
    model='Qwen/Qwen1.5-1.8B-Chat-GGUF/qwen1_5-1_8b-chat-q2_k.gguf',
    messages=[
        {'role': 'user', 'content': 'Count to 10, with a comma between each number and no newlines. E.g., 1, 2, 3, ...'}
    ],
    temperature=0,
    stream=True  # again, we set stream=True
)
# create variables to collect the stream of chunks
collected_chunks = []
collected_messages = []
# iterate through the stream of events
chunk_time = 0
for chunk in response:
    chunk_time = time.time() - start_time  # calculate the time delay of the chunk
    collected_chunks.append(chunk)  # save the event response
    chunk_message = chunk.choices[0].delta.content  # extract the message
    collected_messages.append(chunk_message)  # save the message
    print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text

# print the time delay and text received
print(f"Full response received {chunk_time:.2f} seconds after request")
# clean None in collected_messages
collected_messages = [m for m in collected_messages if m is not None]
full_reply_content = ''.join(collected_messages)
print(f"Full conversation received: {full_reply_content}")
