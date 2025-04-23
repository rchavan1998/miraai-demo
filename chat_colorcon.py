import streamlit as st
import requests
import uuid

# --- UI CONFIGURATION ---
st.set_page_config(page_title="ColorCon - MiraAI Powered Agent", page_icon="🤖", layout="centered")
st.title("🤖 ColorCon - MiraAI Powered Agent")
st.caption("Chat with your AI Agent connected to your knowledge and data sources.")

# --- SESSION STATE FOR CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AGENT CONFIG ---
API_URL = "https://mira-demo.miraclesoft.ai/api/modelVsModel?environment=agent&projectId=BA39374A-9861-4DF0-BA6A-D2AFE54678BE"
HEADERS = {
    "access-key": "920eb7d2db26622b1147ddc613d510c1",
    "Content-Type": "application/json",
    "token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJuOEwyNFZZRGRFVUNnay1INEE1X3pYSWVNb0kyUENldm1XYUUyUXRJanNnIn0.eyJleHAiOjE3NDUzODQ4MjEsImlhdCI6MTc0NTM2MzIyMSwiYXV0aF90aW1lIjoxNzQ1MzYzMDM1LCJqdGkiOiJkYThkYTI1Yi1lZTA2LTQ0Y2EtYjVkZi05NTA0NWJlMTUxN2YiLCJpc3MiOiJodHRwczovL2tleWNsb2FrLWFiZW41cmkyb2EtdWUuYS5ydW4uYXBwL3JlYWxtcy9taXJhLWFpLW5wcm9kIiwiYXVkIjpbInJlYWxtLW1hbmFnZW1lbnQiLCJhY2NvdW50Il0sInN1YiI6IjZiYjc1NjNmLTIzN2QtNDkyNS1hZTQ0LTI0N2RiZDMxZGVlYiIsInR5cCI6IkJlYXJlciIsImF6cCI6Im1pcmFncHRDbGllbnQiLCJub25jZSI6ImU1NDUyNTEwLTBiNWUtNGUxZi04ODdlLTkzZGQ2ZjQzNTVmYSIsInNlc3Npb25fc3RhdGUiOiI4MDM2ZDlkMi00MGU4LTQ1ZjktYWNiOC0zMTYzYzVhZjQyMjEiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbInRlc3QiLCJkZWZhdWx0LXJvbGVzLW1pcmEtYWktbnByb2QiXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbInZpZXctcmVhbG0iLCJ2aWV3LWlkZW50aXR5LXByb3ZpZGVycyIsIm1hbmFnZS1pZGVudGl0eS1wcm92aWRlcnMiLCJpbXBlcnNvbmF0aW9uIiwicmVhbG0tYWRtaW4iLCJjcmVhdGUtY2xpZW50IiwibWFuYWdlLXVzZXJzIiwicXVlcnktcmVhbG1zIiwidmlldy1hdXRob3JpemF0aW9uIiwicXVlcnktY2xpZW50cyIsInF1ZXJ5LXVzZXJzIiwibWFuYWdlLWV2ZW50cyIsIm1hbmFnZS1yZWFsbSIsInZpZXctZXZlbnRzIiwidmlldy11c2VycyIsInZpZXctY2xpZW50cyIsIm1hbmFnZS1hdXRob3JpemF0aW9uIiwibWFuYWdlLWNsaWVudHMiLCJxdWVyeS1ncm91cHMiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiI4MDM2ZDlkMi00MGU4LTQ1ZjktYWNiOC0zMTYzYzVhZjQyMjEiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByb2ZpbGUiOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0lnT2lBaVNsZFVJaXdpYTJsa0lpQTZJQ0p1T0V3eU5GWlpSR1JGVlVObmF5MUlORUUxWDNwWVNXVk5iMGt5VUVObGRtMVhZVVV5VVhSSmFuTm5JbjAuZXlKbGVIQWlPakUzTkRRd05EUTJNREVzSW1saGRDSTZNVGMwTkRBeU5qWXdNU3dpWVhWMGFGOTBhVzFsSWpveE56UTBNREkyTlRrMkxDSnFkR2tpT2lJeE9EZ3haakZoWmkwNVpqSXdMVFEyWmprdFlUZzJOUzAyT1dJd05qYzVNalV6T0RNaUxDSnBjM01pT2lKb2RIUndjem92TDJ0bGVXTnNiMkZyTFdGaVpXNDFjbWt5YjJFdGRXVXVZUzV5ZFc0dVlYQndMM0psWVd4dGN5OXRhWEpoTFdGcExXNXdjbTlrSWl3aVlYVmtJam9pYldseVlXZHdkRU5zYVdWdWRDSXNJbk4xWWlJNklqSmhORGcxWVRaa0xXVm1PVGd0TkROaU5TMWlaVEUyTFRkaE9USmlZekEzWWpRMVpDSXNJblI1Y0NJNklrbEVJaXdpWVhwd0lqb2liV2x5WVdkd2RFTnNhV1Z1ZENJc0ltNXZibU5sSWpvaVlqYzNPR0ZqWkRJdE1XWmtaUzAwWXpZd0xUZ3hZbVF0TXpNellqSmpOMk0yTkdFMElpd2ljMlZ6YzJsdmJsOXpkR0YwWlNJNkltSTBPREkyTnpZekxXUmxNV010TkRFNFlpMWlOVE5rTFdFek9XSm1ORFV3Tmprd05TSXNJbUYwWDJoaGMyZ2lPaUp5VVZkWVZ6aHVaR0pqV0dFMWRVUmtUbkF3WDBkQklpd2lZV055SWpvaU1TSXNJbk5wWkNJNkltSTBPREkyTnpZekxXUmxNV010TkRFNFlpMWlOVE5rTFdFek9XSm1ORFV3Tmprd05TSXNJbVZ0WVdsc1gzWmxjbWxtYVdWa0lqcG1ZV3h6WlN3aVpXMWhhV3dpT2lKNWEybHNZWEJoY25Sb2FVQnRhWEpoWTJ4bGMyOW1kQzVqYjIwaWZRLm9STHBJV19wdDlqVUR6OHRzanRaYW9KVV9tTy04Mlp1YzJWYklNLXlxTlhrZmVrZFVNeV9rbDRZRU51WTlQdEQ4QkVYeVZzSF84RGZrYVpESm4tVTJ3VC05bGJEcnhKdjJ4R0FfaXV0UlRHQncwOEM4bWJONVdBVW5XTUVobGI3dnAzRDNvZ1Y2bTliUEU0bVdSRnhvekNIdEgyUVhuTkdCdmVXbzVseTRkaGFWRGhtYXNzUkVpam1QaHZlNWRkMmdhMTZsTlAybl9rSXlGTGpXWTJuZmJIS01ldGU2TzVwaHpjeU5pRmlhMUl1YTl0b1VINUwxcm04bXlmTEdMbTg1TmJyb3Q4TGh1UlFOSmNfSkd5bFdiVUhuSXBwU0dCUzQ5a2NlaDYyLU9YNGhUVWc1NDJ5a2o1em1lc2lJeGJCRVV2SDNUVGhTUEFrd1VTZXg3ZlZkZyIsIm5hbWUiOiJhZG1pbiIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluIiwiZ2l2ZW5fbmFtZSI6ImFkbWluIiwiZW1haWwiOiJhZG1pbkBtaXJhY2xlc29mdC5jb20iLCJwaWN0dXJlIjoiaHR0cHM6Ly9pbWFnZXMubWlyYWNsZXNvZnQuY29tL2VtcGxveWVlLXByb2ZpbGUtcGljcy9jbG9rYW0ucG5nP2RhdGU9TW9uJTIwQXByJTIwMDclMjAyMDI1JTIwMTk6MzQ6MTAlMjBHTVQrMDUzMCUyMChJbmRpYSUyMFN0YW5kYXJkJTIwVGltZSkifQ.g3eBga8p1ZpzqobIEmrAOpVVOROw-YRgU6-wxyDLttOEL3rdZMo1mRQb_89aP5t9nrZ8r_R9l-oO0Qw4WGxNHhWv_LwB3mq4zkeEJT-sUHKwJFSnP8eIGd2zj44GEFPRuvuGBFqo8HpStwz5qul6Z3gQahn6nWgc-RrMhz1jqHShPDOKTeq-UzcPLlkm3_Dcmg2iI0tBLo-K2RXj3bT0yQzdAhXKvJxI2APUhYC0cc6AJ5OILhbErt9X_O1b67gN1N-q0bGgnQeGEN9I86yx7_UXPMj9LOOYHVrGSd-KYP4xSSJR3-nir6_BBh5QgeDVvH1sr3nkC2vsHHHojdUlOQ"
}
AGENT_ID = "BA39374A-9861-4DF0-BA6A-D2AFE54678BE"

# --- FUNCTION TO SEND QUERY TO AGENT ---
def query_agent(user_query):
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
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

# --- CHAT UI ---
with st.chat_message("assistant"):
    st.markdown("Hi! Ask me anything about Colorcon's products or data.")

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your question...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        try:
            agent_reply = query_agent(user_input)
            reply_content = agent_reply[0] if isinstance(agent_reply, list) else str(agent_reply)
        except Exception as e:
            reply_content = f"❌ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply_content})
    with st.chat_message("assistant"):
        st.markdown(reply_content)
