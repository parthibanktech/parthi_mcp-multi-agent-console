from mcp.server.fastmcp import FastMCP
import socket


def is_port_in_use(port: int) -> bool:
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0
    
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
    # Sample employee database (you can expand later)
    employees = {
        "E001": {
            "employee_id": "E001",
            "name": "Alice Johnson",
            "role": "Software Engineer",
            "department": "Tech"
        },
        "E002": {
            "employee_id": "E002",
            "name": "Michael Smith",
            "role": "Senior Accountant",
            "department": "Finance"
        },
        "E003": {
            "employee_id": "E003",
            "name": "Priya Sharma",
            "role": "HR Manager",
            "department": "Human Resources"
        },

         "E004": {
            "employee_id": "E004",
            "name": "Priya Sharma4",
            "role": "HR Manager4",
            "department": "Human Resources4"
        }
    }

    # Return employee if exists, otherwise return message
    return employees.get(employee_id, {
        "error": f"No employee found with id {employee_id}"
    })


@mcp.tool()
def check_leave_balance(employee_id: str) -> dict:
    return {
        "employee_id": employee_id,
        "leave_balance": 12
    }

if __name__ == "__main__":
    print("Starting HR MCP Server...")
    
    # Prevent double-start on same port 
    if is_port_in_use(8011):
        print("⚠️  Port 8011 already in use — skipping server start.")
    else:
        mcp.run(transport="sse", port=8011)