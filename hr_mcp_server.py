
from mcp.server.fastmcp import FastMCP

# Server with instructions
mcp = FastMCP(
    name="HRServer",
    instructions="""
        This server provides human resources tools.
        - Call get_employee_details(employee_id) to fetch an employee's information.
        - Call check_leave_balance(employee_id) to view the available leave balance for an employee.
    """,
    port=8011
)

@mcp.tool()
def get_employee_details(employee_id: str) -> dict:
    return {
        "employee_id": employee_id,
        "name": "Alice Johnson",
        "role": "Software Engineer",
        "department": "Tech"
    }

@mcp.tool()
def check_leave_balance(employee_id: str) -> dict:
    return {
        "employee_id": employee_id,
        "leave_balance": 12
    }

if __name__ == "__main__":
    print("Starting HR MCP Server...")
    mcp.run(transport="streamable-http")
