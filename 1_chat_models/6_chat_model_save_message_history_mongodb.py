# Example Source: https://python.langchain.com/v0.2/docs/integrations/memory/google_firestore/

from dotenv import load_dotenv
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()

SESSION_ID = "user_session_new"  # This could be a username or a unique ID
DB_NAME = "chat_history"
COLLECTION_NAME = "message_store"

# Initialize MongoDB Chat Message History
print("Initializing MongoDB Chat Message History...")
chat_history = MongoDBChatMessageHistory(
    connection_string="mongodb://localhost:27017/",
    session_id=SESSION_ID,
    database_name=DB_NAME,
    collection_name=COLLECTION_NAME,
)

print("Chat History Initialized.")
print("Current Chat History:")
print(
    "\n".join(
        str(message.type) + ": " + str(message.content)
        for message in chat_history.messages
    )
)
print("-----------------------------")

# Initialize Chat Model
model = ChatOpenAI(model="gpt-4o-mini")

print("Start chatting with the AI. Type 'exit' to quit.")

while True:
    human_input = input("User: ")
    if human_input.lower() == "exit":
        break

    chat_history.add_user_message(human_input)

    ai_response = model.invoke(chat_history.messages)
    chat_history.add_ai_message(ai_response.content)

    print(f"AI: {ai_response.content}")
