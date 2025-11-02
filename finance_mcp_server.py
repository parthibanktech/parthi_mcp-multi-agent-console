
from mcp.server.fastmcp import FastMCP

# Server with instructions
mcp = FastMCP(
    name="FinanceServer",
    instructions="""
        This server provides finance-related tools.
        - Call generate_invoice(customer_id) to generate a new invoice for a customer.
        - Call get_budget_summary(department) to retrieve the budget overview of any department.
    """,
    port=8010
)

@mcp.tool()
def generate_invoice(customer_id: str) -> dict:
    return {
        "invoice_id": "INV-1001",
        "customer_id": customer_id,
        "amount": 2500,
        "status": "generated"
    }

@mcp.tool()
def get_budget_summary(department: str) -> dict:
    return {
        "department": department,
        "budget": 100000,
        "spent": 65432,
        "remaining": 34568
    }

if __name__ == "__main__":
    print("Starting Finance MCP Server...")
    mcp.run(transport="streamable-http")
