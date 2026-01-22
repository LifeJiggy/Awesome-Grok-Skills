"""
Backend Agent
Backend development and API automation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class APIFramework(Enum):
    FASTAPI = "fastapi"
    EXPRESS = "express"
    SPRING = "spring"
    DJANGO = "django"


@dataclass
class Endpoint:
    path: str
    method: str
    description: str
    params: Dict
    response_schema: Dict


class APIBuilder:
    """API endpoint builder"""
    
    def __init__(self):
        self.endpoints = []
        self.middleware = []
    
    def add_endpoint(self,
                    path: str,
                    method: str,
                    description: str,
                    params: Dict = None,
                    response_schema: Dict = None) -> Endpoint:
        """Add API endpoint"""
        endpoint = Endpoint(
            path=path,
            method=method,
            description=description,
            params=params or {},
            response_schema=response_schema or {}
        )
        self.endpoints.append(endpoint)
        return endpoint
    
    def generate_openapi(self) -> Dict:
        """Generate OpenAPI specification"""
        return {
            "openapi": "3.0.0",
            "info": {"title": "API", "version": "1.0.0"},
            "paths": {
                e.path: {
                    e.method.lower(): {
                        "summary": e.description,
                        "parameters": [{"name": k, "in": "query"} for k in e.params],
                        "responses": {"200": {"description": "OK"}}
                    }
                }
                for e in self.endpoints
            }
        }
    
    def generate_routes(self, framework: APIFramework = APIFramework.FASTAPI) -> str:
        """Generate route code"""
        if framework == APIFramework.FASTAPI:
            return self._generate_fastapi_routes()
        elif framework == APIFramework.EXPRESS:
            return self._generate_express_routes()
        return ""
    
    def _generate_fastapi_routes(self) -> str:
        lines = ["from fastapi import APIRouter", "", "router = APIRouter()", ""]
        for e in self.endpoints:
            lines.append(f"@router.{e.method.lower()}('{e.path}')")
            lines.append(f"async def {e.path.replace('/', '_').strip('_')}_handler():")
            lines.append(f"    # {e.description}")
            lines.append('    return {"status": "ok"}')
            lines.append("")
        return "\n".join(lines)
    
    def _generate_express_routes(self) -> str:
        lines = ["const express = require('express');", "const router = express.Router();", ""]
        for e in self.endpoints:
            lines.append(f"router.{e.method.lower()}('{e.path}', async (req, res) => {{")
            lines.append(f"    // {e.description}")
            lines.append('    res.json({ status: "ok" });')
            lines.append("});")
            lines.append("")
        return "\n".join(lines)


class DatabaseManager:
    """Database operations"""
    
    def __init__(self):
        self.connections = {}
        self.models = {}
    
    def add_connection(self, name: str, db_type: str, connection_str: str):
        """Add database connection"""
        self.connections[name] = {"type": db_type, "connection": connection_str}
    
    def create_model(self, name: str, fields: Dict):
        """Create data model"""
        self.models[name] = {
            "fields": fields,
            "table": name.lower() + "s"
        }
    
    def generate_migrations(self, model_name: str) -> str:
        """Generate migration SQL"""
        model = self.models.get(model_name)
        if not model:
            return ""
        
        fields = []
        for field_name, field_type in model["fields"].items():
            sql_type = "TEXT" if field_type == "str" else "INTEGER" if field_type == "int" else "TIMESTAMP"
            fields.append(f"    {field_name} {sql_type}")
        
        return f"""
CREATE TABLE {model["table"]} (
    id SERIAL PRIMARY KEY,
{chr(10).join(fields)},
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
"""


class CacheManager:
    """Caching layer"""
    
    def __init__(self):
        self.cache = {}
        self.ttl_default = 3600
    
    def get(self, key: str) -> Optional[Dict]:
        """Get cached value"""
        if key in self.cache:
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Dict, ttl: int = None):
        """Set cached value"""
        self.cache[key] = value
    
    def invalidate(self, key: str):
        """Invalidate cache"""
        if key in self.cache:
            del self.cache[key]
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate by pattern"""
        import re
        for key in list(self.cache.keys()):
            if re.match(pattern, key):
                del self.cache[key]


class QueueManager:
    """Message queue operations"""
    
    def __init__(self):
        self.queues = {}
    
    def add_queue(self, name: str, worker_count: int = 1):
        """Add message queue"""
        self.queues[name] = {
            "worker_count": worker_count,
            "messages": [],
            "processed": 0
        }
    
    def enqueue(self, queue_name: str, message: Dict):
        """Add message to queue"""
        if queue_name in self.queues:
            self.queues[queue_name]["messages"].append(message)
    
    def dequeue(self, queue_name: str) -> Optional[Dict]:
        """Get message from queue"""
        if queue_name in self.queues and self.queues[queue_name]["messages"]:
            return self.queues[queue_name]["messages"].pop(0)
        return None
    
    def get_stats(self, queue_name: str) -> Dict:
        """Get queue statistics"""
        if queue_name not in self.queues:
            return {}
        q = self.queues[queue_name]
        return {
            "pending": len(q["messages"]),
            "processed": q["processed"],
            "workers": q["worker_count"]
        }


class GraphQLGenerator:
    """GraphQL schema generator"""
    
    def __init__(self):
        self.types = {}
        self.queries = []
        self.mutations = []
    
    def add_type(self, name: str, fields: Dict):
        """Add GraphQL type"""
        self.types[name] = fields
    
    def add_query(self, name: str, return_type: str, resolver: str):
        """Add query"""
        self.queries.append({"name": name, "return_type": return_type, "resolver": resolver})
    
    def add_mutation(self, name: str, input_type: str, return_type: str):
        """Add mutation"""
        self.mutations.append({"name": name, "input": input_type, "return": return_type})
    
    def generate_schema(self) -> str:
        """Generate GraphQL schema"""
        lines = ["type Query {"]
        for q in self.queries:
            lines.append(f"  {q['name']}: {q['return_type']}")
        lines.append("}")
        lines.append("")
        lines.append("type Mutation {")
        for m in self.mutations:
            lines.append(f"  {m['name']}(input: {m['input']}): {m['return']}")
        lines.append("}")
        lines.append("")
        for type_name, fields in self.types.items():
            lines.append(f"type {type_name} {{")
            for field_name, field_type in fields.items():
                lines.append(f"  {field_name}: {field_type}")
            lines.append("}")
            lines.append("")
        return "\n".join(lines)


if __name__ == "__main__":
    api = APIBuilder()
    api.add_endpoint("/users", "GET", "Get all users")
    api.add_endpoint("/users/{id}", "GET", "Get user by ID")
    api.add_endpoint("/users", "POST", "Create user")
    
    db = DatabaseManager()
    db.create_model("User", {"name": "str", "email": "str", "age": "int"})
    
    cache = CacheManager()
    cache.set("user:1", {"name": "John", "email": "john@example.com"})
    
    queue = QueueManager()
    queue.add_queue("notifications")
    queue.enqueue("notifications", {"type": "email", "to": "user@example.com"})
    
    graphql = GraphQLGenerator()
    graphql.add_type("User", {"id": "ID", "name": "String", "email": "String"})
    graphql.add_query("getUser", "User", "resolveUser")
    
    print(f"API endpoints: {len(api.endpoints)}")
    print(f"Models: {list(db.models.keys())}")
    print(f"Cached items: {len(cache.cache)}")
    print(f"Queue messages: {queue.get_stats('notifications')['pending']}")
    print(f"GraphQL types: {list(graphql.types.keys())}")
