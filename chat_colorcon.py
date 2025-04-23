import streamlit as st
import requests

# --- UI CONFIGURATION ---
st.set_page_config(page_title="ColorCon - MiraAI Powered Agent", page_icon="🤖", layout="centered")
st.title("🤖 ColorCon - MiraAI Powered Agent")
st.caption("Chat with your AI Agent connected to your knowledge and data sources.")

# --- SESSION STATE INIT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
# if "access_key" not in st.session_state:
#     st.session_state.access_key = ""
# if "token" not in st.session_state:
#     st.session_state.token = ""

# --- SIDEBAR OR CONFIG PANEL ---
# with st.expander("🔐 Agent Configuration", expanded=False):
#     st.session_state.access_key = st.text_input("Access Key", value=st.session_state.access_key, type="password")
#     st.session_state.token = st.text_area("Bearer Token", value=st.session_state.token, height=100)

# --- AGENT CONFIG ---
API_URL = "https://mira-demo.miraclesoft.ai/api/modelVsModel?environment=agent&projectId=BA39374A-9861-4DF0-BA6A-D2AFE54678BE"
HEADERS = {
    "access-key": "920eb7d2db26622b1147ddc613d510c1",
    "Content-Type": "application/json",
    "token": ""
}
AGENT_ID = "BA39374A-9861-4DF0-BA6A-D2AFE54678BE"

# --- FUNCTION TO SEND QUERY TO AGENT ---
def query_agent(user_query):
    headers = {
        "access-key": st.session_state.access_key,
        "Content-Type": "application/json",
        "token": st.session_state.token
    }

    payload = [{
        "query": user_query,
        "Id": 1,
        "agentId": AGENT_ID,
        "chatCompletionsBaseModel": "gpt-4",
        "files": [],
        "formData": {
            "Title": "Default",
            "SystemPrompt": None,
            "PersonalityPrompt": None,
            "PersonalityPromptTitle": None,
            "QueryPrompt": "Query: [[QUERY]] \\n You are an AI assistant designed to help users find information using the following functions: [[SOURCES]] \\n You will receive user queries and need to analyze them to select the most relevant function, Note: You should follow the response whatever provided in steps \\n Do not Include single quotes in responses:  Step 1: Receive the User Query, Identify the user query. Step 2: Determine if the Query is a Greeting (e.g., \"how are you\", \"hello\", \"hi\"). Construct a JSON response for a greeting in the format: \\n [{ \"function_name\": \"greet_user\", \"greeting\": \"Hello!\", \"source\": \"system\", \"your_response\": \"Hi there! How can I assist you today?\" }] \\n Step 3: If the Query is Not a Greeting: Analyze the query, If the query is matched with the available functions descriptions, respond available functions in the below format : [{ \"function_name\": \"...\", \"<ID_KEY>\": \"...\", \"source\": \"...\", \"create_yourPrompt\": \"...\", \"ConfigJson\": \"...\" }], Replace <ID_KEY> with the appropriate key based on the context of the matched function. Use \"ProjectId\" if the function is related to a \"KS\", \"CoreId\" if it pertains to a \"Core\", and \"ConnectionId\" if it involves a \"DS\". If the context is unclear or cannot be determined, default to using \"ProjectId\". Step 4: If the query is not matched with the available functions descriptions, respond [{ \"function_name\": \"NA\", \"<ID_KEY>\": \"NA\", \"source\": \"NA\" }]. Step 5: Validate the Response provided by [[Myassistant response]] Step 6: Check if the [[Myassistant response]] satisfies the user query. If yes, respond with {\"status\":\"[[completed]]\"}. If no, use one of the provided functions or respond with: [{ \"function_name\": \"...\", \"<ID_KEY>\": \"...\", \"source\": \"...\", \"create_yourPrompt\": \"...\", \"ConfigJson\": \"...\" }]",
            "RepetationMin": 1,
            "frequencyPenalty": 0,
            "maxLength": 3000,
            "presencePenalty": 0,
            "stop": [],
            "stopDefault": [],
            "streamDefault": False,
            "temperature": 0,
            "topK": 40,
            "topP": 0
        },
        "sources": [
            {
                "Id": "B9B1435D-F86C-4477-9189-5E212FE11FC4",
                "AgentId": AGENT_ID,
                "Description": "Colorcon coatings like Acryl-EZE, Opadry, Opatint...",
                "Name": "Colorcon Product Brochures",
                "ProjectId": "34BBC4CE-F6DA-4FD5-9A4F-064A7946765E",
                "Source": "KS"
            },
            {
                "Id": "583A332A-5D5E-4093-8646-C2654F3FC383",
                "AgentId": AGENT_ID,
                "ConnectionId": "677E89D8-38DA-4F3C-AD3B-6916A50173A1",
                "Description": "Database for inventory, sales, and orders",
                "Name": "Colorcon Data",
                "Source": "DS"
            }
        ]
    }]
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# --- STARTING MESSAGE ---
with st.chat_message("assistant"):
    st.markdown("Hi! Ask me anything about Colorcon's products or data.")

# --- RENDER CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT ---
user_input = st.chat_input("Type your question...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        try:
            agent_reply = query_agent(user_input)
            try:    
                reply_content = agent_reply["results"][0]["value"]["FinalResponse"]["response"]
            except Exception as e:
                reply_content = f" Error parsing response: {str(e)}"

        except Exception as e:
            reply_content = f" Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply_content})
    with st.chat_message("assistant"):
        st.markdown(reply_content)
