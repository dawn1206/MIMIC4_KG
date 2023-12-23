import os
from graphdatascience import GraphDataScience

# Get Neo4j DB URI and credentials from environment if applicable
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_AUTH = None
if os.environ.get("NEO4J_USER") and os.environ.get("NEO4J_PASSWORD"):
    NEO4J_AUTH = (
        os.environ.get("neo4j"),
        os.environ.get("xyt020122"),
    )

gds = GraphDataScience(NEO4J_URI, auth=NEO4J_AUTH)

# We define how we want to project our database into GDS
node_projection = ["Omr", "DiagnoseDetail"]
relationship_projection = {"BUYS": {"orientation": "UNDIRECTED", "properties": "amount"}}

# Before actually going through with the projection, let's check how much memory is required
result = gds.graph.project.estimate(node_projection, relationship_projection)

print(f"Required memory for native loading: {result['requiredMemory']}")

gds.graph.project