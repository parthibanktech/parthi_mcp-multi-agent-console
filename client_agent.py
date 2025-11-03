import streamlit as st
import asyncio
import socket
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Load env variables
load_dotenv()

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Parthi Multi-Agent MCP Console", page_icon="🤖", layout="wide")

st.sidebar.title("⚙️ MCP Configuration")
st.sidebar.markdown("Connected Servers:")
st.sidebar.success("💰 Finance Server → http://localhost:8010/mcp")
st.sidebar.success("👩‍💼 HR Server → http://localhost:8011/mcp")

OPENAI_API_KEY = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
st.sidebar.divider()

dark = st.sidebar.checkbox("🌙 Dark Theme", value=True)
if dark:
    st.markdown("""
        <style>
        body {background-color: #0e1117; color: #f5f5f5;}
        .stTextInput, .stTextArea {background-color: #1b1f24 !important; color: #fff !important;}
        </style>
    """, unsafe_allow_html=True)

st.title("🤝 Multi-Agent MCP Console")
st.caption("Interact with both Finance & HR MCP Agents through LangChain + Streamlit.")

# ---------------- Helper Functions ----------------
def is_port_in_use(port: int) -> bool:
    """Check if port is open (server is running)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

async def query_agents(prompt):
    """Send query to both Finance & HR MCP Servers."""
    local_ip = socket.gethostbyname(socket.gethostname())

    if not is_port_in_use(8010) or not is_port_in_use(8011):
        return "⚠️ One or more MCP servers are not running. Please start them first."

    client = MultiServerMCPClient({
        "finance": {"url": f"http://{local_ip}:8010/mcp", "transport": "streamable_http"},
        "hr": {"url": f"http://{local_ip}:8011/mcp", "transport": "streamable_http"},
    })

    tools = await client.get_tools()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)
    agent = create_react_agent(model=llm, tools=tools)

    result = await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
    return result["messages"][-1].content

def run_async(func, *args):
    """Safely run async code in Streamlit."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(func(*args))

# ---------------- Chat UI ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type a request (e.g. 'Generate invoice for customer 123')")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Querying Multi-Agent MCP..."):
            try:
                response = run_async(query_agents, prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"⚠️ {e}")
