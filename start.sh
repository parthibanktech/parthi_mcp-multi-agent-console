#!/bin/bash

# Start the Finance MCP Server in the background
echo "Starting Finance MCP Server on port 8010..."
python finance_mcp_server.py &

# Start the HR MCP Server in the background
echo "Starting HR MCP Server on port 8011..."
python hr_mcp_server.py &

# Wait a few seconds to ensure servers are up
sleep 5

# Start the Streamlit app in the foreground
# Render sets the PORT environment variable, which Streamlit should use.
echo "Starting Streamlit Client on port $PORT..."
streamlit run client_agent.py --server.port $PORT --server.address 0.0.0.0
