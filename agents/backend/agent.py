"""
Backend Agent
Backend development and API automation
"""

from typing import Dict, Optional, List, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import time
import hashlib
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
import queue


class APIFramework(Enum):
    FASTAPI = "fastapi"
    EXPRESS = "express"
    SPRING = "spring"
    DJANGO = "django"
    FLASK = "flask"
    GRAPHQL = "graphql"


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class AuthType(Enum):
    NONE = "none"
    BEARER = "bearer"
    API_KEY = "api_key"
    BASIC = "basic"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    SESSION = "session"


class CacheStrategy(Enum):
    LRU = "lru"
    LFU = "lfu"
    TTL = "ttl"
    FIFO = "fifo"


@dataclass
class Endpoint:
    path: str
    method: str
    description: str
    params: Dict
    response_schema: Dict
    auth_required: bool = False
    auth_type: AuthType = AuthType.NONE
    rate_limit: Optional[int] = None
    cache_ttl: Optional[int] = None
    middleware: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    deprecated: bool = False
    version: str = "v1"
    request_body: Optional[Dict] = None
    error_responses: Dict = field(default_factory=dict)


@dataclass
class Middleware:
    name: str
    func: Callable
    priority: int = 0
    enabled: bool = True


@dataclass
class Route:
    path: str
    method: HTTPMethod
    handler: Callable
    middleware: List[Middleware] = field(default_factory=list)
    auth_required: bool = False
    rate_limit: Optional[int] = None
    cache_ttl: Optional[int] = None


@dataclass
class ModelField:
    name: str
    field_type: str
    nullable: bool = False
    primary_key: bool = False
    foreign_key: Optional[str] = None
    unique: bool = False
    index: bool = False
    default: Any = None
    max_length: Optional[int] = None
    choices: Optional[List[str]] = None


class APIBuilder:
    """Advanced API endpoint builder with comprehensive features"""
    
    def __init__(self, title: str = "API", version: str = "1.0.0", description: str = ""):
        self.endpoints: List[Endpoint] = []
        self.middleware: List[Middleware] = []
        self.router = Router()
        self.title = title
        self.version = version
        self.description = description
        self.base_path = "/api/v1"
        self.auth_config = {
            "type": AuthType.NONE,
            "secret_key": None,
            "algorithm": "HS256",
            "expiration": 3600
        }
        self.rate_limiter = RateLimiter()
        self.cache_manager = CacheManager()
        self.logger = logging.getLogger(__name__)
    
    def add_middleware(self, name: str, func: Callable, priority: int = 0):
        """Add middleware to the API"""
        middleware = Middleware(name=name, func=func, priority=priority)
        self.middleware.append(middleware)
        self.middleware.sort(key=lambda m: m.priority, reverse=True)
        return middleware
    
    def add_endpoint(self,
                    path: str,
                    method: str,
                    description: str,
                    params: Dict = None,
                    response_schema: Dict = None,
                    auth_required: bool = False,
                    auth_type: AuthType = AuthType.NONE,
                    rate_limit: Optional[int] = None,
                    cache_ttl: Optional[int] = None,
                    middleware: List[str] = None,
                    tags: List[str] = None,
                    deprecated: bool = False,
                    version: str = "v1",
                    request_body: Optional[Dict] = None,
                    error_responses: Dict = None) -> Endpoint:
        """Add API endpoint with comprehensive configuration"""
        endpoint = Endpoint(
            path=path,
            method=method.upper(),
            description=description,
            params=params or {},
            response_schema=response_schema or {},
            auth_required=auth_required,
            auth_type=auth_type,
            rate_limit=rate_limit,
            cache_ttl=cache_ttl,
            middleware=middleware or [],
            tags=tags or [],
            deprecated=deprecated,
            version=version,
            request_body=request_body,
            error_responses=error_responses or {}
        )
        self.endpoints.append(endpoint)
        self.router.add_route(Route(
            path=path,
            method=HTTPMethod[method.upper()],
            handler=self._create_handler(endpoint),
            auth_required=auth_required,
            rate_limit=rate_limit,
            cache_ttl=cache_ttl
        ))
        return endpoint
    
    def _create_handler(self, endpoint: Endpoint) -> Callable:
        """Create handler function for endpoint"""
        async def handler(**kwargs):
            self.logger.info(f"Handling {endpoint.method} {endpoint.path}")
            
            if endpoint.auth_required:
                if not self._authenticate_request(kwargs):
                    raise AuthenticationError("Authentication required")
            
            if endpoint.rate_limit:
                if not self.rate_limiter.allow_request(endpoint.path):
                    raise RateLimitError("Rate limit exceeded")
            
            cache_key = f"{endpoint.method}:{endpoint.path}:{json.dumps(kwargs)}"
            if endpoint.cache_ttl:
                cached = self.cache_manager.get(cache_key)
                if cached:
                    return cached
            
            result = {"status": "ok", "data": {}}
            
            if endpoint.cache_ttl:
                self.cache_manager.set(cache_key, result, ttl=endpoint.cache_ttl)
            
            return result
        
        return handler
    
    def _authenticate_request(self, kwargs: Dict) -> bool:
        """Authenticate request"""
        return True
    
    def generate_openapi(self) -> Dict:
        """Generate comprehensive OpenAPI specification"""
        paths = {}
        for e in self.endpoints:
            path_key = f"{self.base_path}{e.path}"
            if path_key not in paths:
                paths[path_key] = {}
            
            operation = {
                "summary": e.description,
                "tags": e.tags,
                "operationId": f"{e.method.lower()}_{e.path.replace('/', '_').strip('_')}",
                "deprecated": e.deprecated,
                "parameters": []
            }
            
            for param_name, param_info in e.params.items():
                param = {
                    "name": param_name,
                    "in": "query",
                    "required": param_info.get("required", False),
                    "schema": {
                        "type": param_info.get("type", "string")
                    }
                }
                if "description" in param_info:
                    param["description"] = param_info["description"]
                operation["parameters"].append(param)
            
            if e.request_body:
                operation["requestBody"] = {
                    "content": {
                        "application/json": {
                            "schema": e.request_body
                        }
                    }
                }
            
            responses = {"200": {"description": "Success", "content": {"application/json": {"schema": e.response_schema}}}}
            responses.update(e.error_responses)
            operation["responses"] = responses
            
            if e.auth_required:
                operation["security"] = [{self._get_security_scheme(): []}]
            
            paths[path_key][e.method.lower()] = operation
        
        return {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "version": self.version,
                "description": self.description
            },
            "paths": paths,
            "components": {
                "securitySchemes": self._get_security_schemes()
            }
        }
    
    def _get_security_scheme(self) -> str:
        """Get security scheme name"""
        if self.auth_config["type"] == AuthType.JWT:
            return "BearerAuth"
        elif self.auth_config["type"] == AuthType.API_KEY:
            return "ApiKeyAuth"
        return "BearerAuth"
    
    def _get_security_schemes(self) -> Dict:
        """Get security schemes"""
        if self.auth_config["type"] == AuthType.JWT:
            return {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        elif self.auth_config["type"] == AuthType.API_KEY:
            return {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key"
                }
            }
        return {}
    
    def generate_routes(self, framework: APIFramework = APIFramework.FASTAPI) -> str:
        """Generate route code for specified framework"""
        if framework == APIFramework.FASTAPI:
            return self._generate_fastapi_routes()
        elif framework == APIFramework.EXPRESS:
            return self._generate_express_routes()
        elif framework == APIFramework.SPRING:
            return self._generate_spring_routes()
        elif framework == APIFramework.DJANGO:
            return self._generate_django_urls()
        elif framework == APIFramework.FLASK:
            return self._generate_flask_routes()
        elif framework == APIFramework.GRAPHQL:
            return self._generate_graphql_schema()
        return ""
    
    def _generate_fastapi_routes(self) -> str:
        """Generate FastAPI routes"""
        lines = [
            "from fastapi import APIRouter, Depends, HTTPException, status",
            "from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials",
            "from pydantic import BaseModel, Field",
            "from typing import List, Optional, Dict, Any",
            "",
            "router = APIRouter()",
            "security = HTTPBearer()",
            ""
        ]
        
        for e in self.endpoints:
            func_name = e.path.replace('/', '_').strip('_').replace('{', '').replace('}', '')
            func_name = f"{e.method.lower()}_{func_name}"
            
            lines.append(f"@router.{e.method.lower()}('{e.path}', tags={e.tags})")
            if e.deprecated:
                lines.append(f"@router.deprecated()")
            if e.auth_required:
                lines.append(f"async def {func_name}(credentials: HTTPAuthorizationCredentials = Depends(security)):")
            else:
                lines.append(f"async def {func_name}():")
            lines.append(f"    \"\"\"{e.description}\"\"\"")
            
            if e.params:
                lines.append(f"    params = {{")
                for param_name, param_info in e.params.items():
                    lines.append(f"        '{param_name}': None,  # {param_info.get('type', 'any')}")
                lines.append(f"    }}")
            
            lines.append(f"    return {{'status': 'ok', 'data': {{}}}}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_express_routes(self) -> str:
        """Generate Express.js routes"""
        lines = [
            "const express = require('express');",
            "const router = express.Router();",
            "const auth = require('../middleware/auth');",
            "const rateLimiter = require('../middleware/rateLimiter');",
            "const cache = require('../middleware/cache');",
            ""
        ]
        
        for e in self.endpoints:
            middlewares = []
            if e.auth_required:
                middlewares.append("auth")
            if e.rate_limit:
                middlewares.append(f"rateLimiter({{max: {e.rate_limit}}})")
            if e.cache_ttl:
                middlewares.append(f"cache({{ttl: {e.cache_ttl}}})")
            
            middleware_str = ", ".join(middlewares) if middlewares else ""
            if middleware_str:
                middleware_str = f", {middleware_str}"
            
            lines.append(f"router.{e.method.lower()}('{e.path}'{middleware_str}, async (req, res) => {{")
            lines.append(f"    try {{")
            lines.append(f"        // {e.description}")
            lines.append(f"        const result = {{'status': 'ok', 'data': {{}}}};")
            lines.append(f"        res.json(result);")
            lines.append(f"    }} catch (error) {{")
            lines.append(f"        console.error('Error handling {e.method.lower()} {e.path}:', error);")
            lines.append(f"        res.status(500).json({{'error': 'Internal server error'}});")
            lines.append(f"    }}")
            lines.append(f"});")
            lines.append("")
        
        lines.append("module.exports = router;")
        return "\n".join(lines)
    
    def _generate_spring_routes(self) -> str:
        """Generate Spring Boot controllers"""
        lines = [
            "package com.example.api.controller;",
            "",
            "import org.springframework.web.bind.annotation.*;",
            "import org.springframework.http.ResponseEntity;",
            "import org.springframework.http.HttpStatus;",
            ""
        ]
        
        class_name = f"{self.title.replace(' ', '')}Controller"
        lines.append(f"@RestController")
        lines.append(f"@RequestMapping('/api/v1')")
        lines.append(f"public class {class_name} {{")
        lines.append("")
        
        for e in self.endpoints:
            func_name = e.path.replace('/', '_').strip('_').replace('{', '').replace('}', '')
            func_name = f"{e.method.lower()}{func_name.capitalize()}"
            
            http_method = e.method.upper()
            path = e.path
            
            annotations = {
                "GET": "@GetMapping",
                "POST": "@PostMapping",
                "PUT": "@PutMapping",
                "PATCH": "@PatchMapping",
                "DELETE": "@DeleteMapping"
            }
            
            lines.append(f"    {annotations.get(http_method, '@RequestMapping')}(\"{path}\")")
            if e.auth_required:
                lines.append(f"    @PreAuthorize(\"hasRole('USER')\")")
            lines.append(f"    public ResponseEntity<Map<String, Object>> {func_name}() {{")
            lines.append(f"        // {e.description}")
            lines.append(f"        Map<String, Object> result = new HashMap<>();")
            lines.append(f"        result.put(\"status\", \"ok\");")
            lines.append(f"        return ResponseEntity.ok(result);")
            lines.append(f"    }}")
            lines.append("")
        
        lines.append("}")
        return "\n".join(lines)
    
    def _generate_django_urls(self) -> str:
        """Generate Django URL patterns"""
        lines = [
            "from django.urls import path",
            "from . import views",
            ""
        ]
        
        lines.append("urlpatterns = [")
        for e in self.endpoints:
            func_name = e.path.replace('/', '_').strip('_').replace('{', '').replace('}', '')
            func_name = f"{e.method.lower()}_{func_name}"
            path_pattern = e.path.replace('{', '<').replace('}', '>')
            lines.append(f"    path('{path_pattern}', views.{func_name}, name='{func_name}'),")
        lines.append("]")
        return "\n".join(lines)
    
    def _generate_flask_routes(self) -> str:
        """Generate Flask routes"""
        lines = [
            "from flask import Blueprint, request, jsonify",
            "from functools import wraps",
            ""
        ]
        
        blueprint_name = f"{self.title.lower().replace(' ', '_')}_bp"
        lines.append(f"{blueprint_name} = Blueprint('{blueprint_name}', __name__)")
        lines.append("")
        
        for e in self.endpoints:
            func_name = e.path.replace('/', '_').strip('_').replace('{', '').replace('}', '')
            func_name = f"{e.method.lower()}_{func_name}"
            
            lines.append(f"@{blueprint_name}.route('{e.path}', methods=['{e.method.upper()}'])")
            if e.auth_required:
                lines.append(f"@login_required")
            if e.rate_limit:
                lines.append(f"@limiter.limit('{e.rate_limit} per hour')")
            lines.append(f"def {func_name}():")
            lines.append(f"    # {e.description}")
            lines.append(f"    return jsonify({{'status': 'ok', 'data': {{}}}}), 200")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_graphql_schema(self) -> str:
        """Generate GraphQL schema"""
        return self.graphql.generate_schema() if hasattr(self, 'graphql') else ""
    
    def validate_endpoints(self) -> List[Dict]:
        """Validate all endpoints for common issues"""
        issues = []
        
        for e in self.endpoints:
            if not e.description:
                issues.append({
                    "endpoint": f"{e.method} {e.path}",
                    "issue": "Missing description",
                    "severity": "P2"
                })
            
            if not e.response_schema:
                issues.append({
                    "endpoint": f"{e.method} {e.path}",
                    "issue": "Missing response schema",
                    "severity": "P1"
                })
            
            if e.method in ["POST", "PUT", "PATCH"] and not e.request_body:
                issues.append({
                    "endpoint": f"{e.method} {e.path}",
                    "issue": "Missing request body schema",
                    "severity": "P1"
                })
            
            if not e.error_responses:
                issues.append({
                    "endpoint": f"{e.method} {e.path}",
                    "issue": "No error responses defined",
                    "severity": "P2"
                })
        
        return issues
    
    def export_to_collection(self, format: str = "postman") -> Dict:
        """Export endpoints to API collection format"""
        if format == "postman":
            return self._export_postman()
        elif format == "insomnia":
            return self._export_insomnia()
        return {}
    
    def _export_postman(self) -> Dict:
        """Export to Postman collection format"""
        items = []
        for e in self.endpoints:
            item = {
                "name": f"{e.method} {e.path}",
                "request": {
                    "method": e.method.upper(),
                    "url": {
                        "raw": f"{{{{base_url}}}}{e.path}",
                        "host": ["{{base_url}}"],
                        "path": e.path.strip('/').split('/')
                    },
                    "description": e.description
                },
                "response": []
            }
            items.append(item)
        
        return {
            "info": {
                "name": self.title,
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "item": items
        }


class Router:
    """HTTP router with middleware support"""
    
    def __init__(self):
        self.routes: List[Route] = []
        self.middleware_stack: List[Middleware] = []
    
    def add_route(self, route: Route):
        """Add route to router"""
        self.routes.append(route)
    
    def add_middleware(self, middleware: Middleware):
        """Add middleware to router"""
        self.middleware_stack.append(middleware)
        self.middleware_stack.sort(key=lambda m: m.priority, reverse=True)
    
    def match(self, path: str, method: str) -> Optional[Route]:
        """Match request to route"""
        for route in self.routes:
            if route.path == path and route.method.value == method.upper():
                return route
        return None
    
    def apply_middleware(self, request: Dict) -> Dict:
        """Apply middleware chain to request"""
        result = request
        for middleware in self.middleware_stack:
            if middleware.enabled:
                result = middleware.func(result)
        return result


class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self, default_limit: int = 100, window: int = 60):
        self.default_limit = default_limit
        self.window = window
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()
    
    def allow_request(self, key: str, limit: Optional[int] = None) -> bool:
        """Check if request is allowed"""
        limit = limit or self.default_limit
        now = time.time()
        
        with self.lock:
            self.requests[key] = [
                t for t in self.requests[key]
                if now - t < self.window
            ]
            
            if len(self.requests[key]) >= limit:
                return False
            
            self.requests[key].append(now)
            return True
    
    def get_remaining(self, key: str, limit: Optional[int] = None) -> int:
        """Get remaining requests"""
        limit = limit or self.default_limit
        now = time.time()
        
        with self.lock:
            self.requests[key] = [
                t for t in self.requests[key]
                if now - t < self.window
            ]
            return max(0, limit - len(self.requests[key]))


class AuthenticationManager:
    """Authentication and authorization management"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.tokens: Dict[str, Dict] = {}
        self.logger = logging.getLogger(__name__)
    
    def create_token(self, user_id: str, expires_in: int = 3600) -> str:
        """Create JWT token"""
        import jwt
        
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=expires_in),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        self.tokens[token] = payload
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token"""
        try:
            import jwt
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid token")
            return None
    
    def revoke_token(self, token: str):
        """Revoke token"""
        self.tokens.pop(token, None)
    
    def hash_password(self, password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password"""
        return self.hash_password(password) == hashed


class DatabaseManager:
    """Advanced database operations manager"""
    
    def __init__(self):
        self.connections: Dict[str, Dict] = {}
        self.models: Dict[str, Dict] = {}
        self.connection_pools: Dict[str, Any] = {}
        self.query_log: List[Dict] = []
        self.logger = logging.getLogger(__name__)
    
    def add_connection(self, name: str, db_type: str, connection_str: str,
                      pool_size: int = 5, max_overflow: int = 10):
        """Add database connection with connection pooling"""
        self.connections[name] = {
            "type": db_type,
            "connection": connection_str,
            "pool_size": pool_size,
            "max_overflow": max_overflow,
            "active": 0,
            "idle": pool_size
        }
        self.connection_pools[name] = self._create_pool(pool_size)
    
    def _create_pool(self, size: int) -> List[Dict]:
        """Create connection pool"""
        return [{"id": i, "active": False} for i in range(size)]
    
    def get_connection(self, name: str) -> Optional[Dict]:
        """Get connection from pool"""
        if name not in self.connection_pools:
            return None
        
        pool = self.connection_pools[name]
        for conn in pool:
            if not conn["active"]:
                conn["active"] = True
                return conn
        return None
    
    def release_connection(self, name: str, conn: Dict):
        """Release connection back to pool"""
        conn["active"] = False
    
    def create_model(self, name: str, fields: Union[Dict, List[ModelField]],
                    table_name: Optional[str] = None,
                    indexes: List[Dict] = None,
                    constraints: List[Dict] = None):
        """Create data model with advanced options"""
        if isinstance(fields, list):
            fields_dict = {f.name: f for f in fields}
        else:
            fields_dict = fields
        
        self.models[name] = {
            "fields": fields_dict,
            "table": table_name or name.lower() + "s",
            "indexes": indexes or [],
            "constraints": constraints or [],
            "relationships": [],
            "created_at": datetime.now().isoformat()
        }
    
    def add_relationship(self, model_name: str, relationship_type: str,
                        target_model: str, foreign_key: str,
                        on_delete: str = "CASCADE"):
        """Add relationship between models"""
        if model_name in self.models:
            self.models[model_name]["relationships"].append({
                "type": relationship_type,
                "target": target_model,
                "foreign_key": foreign_key,
                "on_delete": on_delete
            })
    
    def generate_migrations(self, model_name: str) -> str:
        """Generate migration SQL"""
        model = self.models.get(model_name)
        if not model:
            return ""
        
        fields = []
        for field_name, field_info in model["fields"].items():
            if isinstance(field_info, ModelField):
                sql_type = self._map_field_type(field_info)
                nullable = "" if not field_info.nullable else " NULL"
                primary_key = " PRIMARY KEY" if field_info.primary_key else ""
                unique = " UNIQUE" if field_info.unique else ""
                default = f" DEFAULT {field_info.default}" if field_info.default is not None else ""
                
                field_def = f"    {field_name} {sql_type}{nullable}{primary_key}{unique}{default}"
                fields.append(field_def)
            else:
                sql_type = self._map_simple_type(field_info)
                fields.append(f"    {field_name} {sql_type}")
        
        migration = f"""
-- Migration: Create {model['table']}
-- Created: {datetime.now().isoformat()}

CREATE TABLE IF NOT EXISTS {model['table']} (
    id SERIAL PRIMARY KEY,
{chr(10).join(fields)},
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- Indexes
"""
        for idx in model.get("indexes", []):
            unique = "UNIQUE " if idx.get("unique") else ""
            columns = ", ".join(idx.get("columns", []))
            migration += f"CREATE {unique}INDEX idx_{model['table']}_{idx.get('name', 'idx')} ON {model['table']} ({columns});\n"
        
        for constraint in model.get("constraints", []):
            migration += f"ALTER TABLE {model['table']} ADD CONSTRAINT {constraint.get('name', 'constraint')} {constraint.get('definition', '')};\n"
        
        for rel in model.get("relationships", []):
            migration += f"\n-- Relationship: {model_name} -> {rel['target']}\n"
            migration += f"ALTER TABLE {model['table']} ADD CONSTRAINT fk_{model_name}_{rel['foreign_key']}\n"
            migration += f"    FOREIGN KEY ({rel['foreign_key']}) REFERENCES {rel['target'].lower()}s(id)\n"
            migration += f"    ON DELETE {rel['on_delete']};\n"
        
        return migration
    
    def _map_field_type(self, field: ModelField) -> str:
        """Map ModelField to SQL type"""
        type_mapping = {
            "str": f"VARCHAR({field.max_length or 255})",
            "int": "INTEGER",
            "float": "REAL",
            "bool": "BOOLEAN",
            "datetime": "TIMESTAMP",
            "date": "DATE",
            "time": "TIME",
            "uuid": "UUID",
            "json": "JSONB",
            "text": "TEXT",
            "blob": "BYTEA"
        }
        return type_mapping.get(field.field_type, "TEXT")
    
    def _map_simple_type(self, field_type: str) -> str:
        """Map simple type string to SQL type"""
        type_mapping = {
            "str": "VARCHAR(255)",
            "int": "INTEGER",
            "float": "REAL",
            "bool": "BOOLEAN",
            "datetime": "TIMESTAMP",
            "date": "DATE",
            "uuid": "UUID",
            "json": "JSONB",
            "text": "TEXT"
        }
        return type_mapping.get(field_type, "TEXT")
    
    def generate_models(self, framework: str = "sqlalchemy") -> str:
        """Generate ORM models"""
        if framework == "sqlalchemy":
            return self._generate_sqlalchemy_models()
        elif framework == "django":
            return self._generate_django_models()
        elif framework == "mongoose":
            return self._generate_mongoose_models()
        return ""
    
    def _generate_sqlalchemy_models(self) -> str:
        """Generate SQLAlchemy models"""
        lines = [
            "from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text",
            "from sqlalchemy.ext.declarative import declarative_base",
            "from sqlalchemy.orm import relationship",
            "from datetime import datetime",
            "",
            "Base = declarative_base()",
            ""
        ]
        
        for model_name, model in self.models.items():
            class_name = model_name.capitalize()
            lines.append(f"class {class_name}(Base):")
            lines.append(f"    __tablename__ = '{model['table']}'")
            lines.append("")
            
            for field_name, field_info in model["fields"].items():
                if isinstance(field_info, ModelField):
                    sa_type = self._map_to_sqlalchemy_type(field_info.field_type)
                    kwargs = []
                    if field_info.primary_key:
                        kwargs.append("primary_key=True")
                    if field_info.nullable:
                        kwargs.append("nullable=True")
                    if field_info.unique:
                        kwargs.append("unique=True")
                    if field_info.default is not None:
                        kwargs.append(f"default={field_info.default}")
                    
                    kwargs_str = ", ".join(kwargs)
                    lines.append(f"    {field_name} = Column({sa_type}, {kwargs_str})")
            
            lines.append("")
            
            for rel in model.get("relationships", []):
                rel_type = "one_to_many" if rel["type"] == "one_to_many" else "many_to_one"
                lines.append(f"    {rel['target'].lower()}s = relationship('{rel['target'].capitalize()}', back_populates='{model_name.lower()}s')")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _map_to_sqlalchemy_type(self, field_type: str) -> str:
        """Map field type to SQLAlchemy type"""
        type_mapping = {
            "str": "String(255)",
            "int": "Integer",
            "float": "Float",
            "bool": "Boolean",
            "datetime": "DateTime",
            "date": "Date",
            "text": "Text",
            "json": "JSON",
            "uuid": "String(36)"
        }
        return type_mapping.get(field_type, "String(255)")
    
    def _generate_django_models(self) -> str:
        """Generate Django models"""
        lines = [
            "from django.db import models",
            "from django.contrib.auth.models import User",
            ""
        ]
        
        for model_name, model in self.models.items():
            class_name = model_name.capitalize()
            lines.append(f"class {class_name}(models.Model):")
            lines.append("")
            
            for field_name, field_info in model["fields"].items():
                if isinstance(field_info, ModelField):
                    django_field = self._map_to_django_field(field_info)
                    lines.append(f"    {field_name} = {django_field}")
            
            lines.append("")
            lines.append("    class Meta:")
            lines.append(f"        db_table = '{model['table']}'")
            if model.get("indexes"):
                lines.append(f"        indexes = [")
                for idx in model["indexes"]:
                    lines.append(f"            models.Index(fields={idx.get('columns', [])}),")
                lines.append(f"        ]")
            lines.append("")
        
        return "\n".join(lines)
    
    def _map_to_django_field(self, field: ModelField) -> str:
        """Map ModelField to Django field"""
        args = []
        
        if field.field_type == "str":
            field_type = f"models.CharField(max_length={field.max_length or 255})"
        elif field.field_type == "int":
            field_type = "models.IntegerField()"
        elif field.field_type == "bool":
            field_type = "models.BooleanField()"
        elif field.field_type == "datetime":
            field_type = "models.DateTimeField(auto_now_add=True)"
        elif field.field_type == "text":
            field_type = "models.TextField()"
        else:
            field_type = "models.CharField(max_length=255)"
        
        if not field.nullable:
            args.append("null=False")
        else:
            args.append("null=True")
        
        if field.unique:
            args.append("unique=True")
        
        if field.default is not None:
            args.append(f"default={field.default}")
        
        args_str = ", ".join(args)
        return f"{field_type}({args_str})" if args_str else field_type
    
    def _generate_mongoose_models(self) -> str:
        """Generate Mongoose models"""
        lines = [
            "const mongoose = require('mongoose');",
            "const Schema = mongoose.Schema;",
            ""
        ]
        
        for model_name, model in self.models.items():
            class_name = model_name.capitalize()
            lines.append(f"const {model_name}Schema = new Schema({{")
            lines.append("  // Fields")
            
            for field_name, field_info in model["fields"].items():
                if isinstance(field_info, ModelField):
                    mongo_type = self._map_to_mongoose_type(field_info.field_type)
                    lines.append(f"  {field_name}: {{ type: {mongo_type}")
                    if field_info.required and not field_info.nullable:
                        lines.append(f"    required: true")
                    if field_info.unique:
                        lines.append(f"    unique: true")
                    if field_info.default is not None:
                        lines.append(f"    default: {field_info.default}")
                    lines.append(f"  }},")
            
            lines.append(f"}}, {{")
            lines.append(f"  timestamps: true,")
            lines.append(f"}});")
            lines.append("")
            lines.append(f"module.exports = mongoose.model('{class_name}', {model_name}Schema);")
            lines.append("")
        
        return "\n".join(lines)
    
    def _map_to_mongoose_type(self, field_type: str) -> str:
        """Map field type to Mongoose type"""
        type_mapping = {
            "str": "String",
            "int": "Number",
            "float": "Number",
            "bool": "Boolean",
            "datetime": "Date",
            "date": "Date",
            "text": "String",
            "json": "Schema.Types.Mixed",
            "uuid": "String"
        }
        return type_mapping.get(field_type, "String")
    
    def generate_query_builder(self, model_name: str) -> str:
        """Generate query builder for model"""
        model = self.models.get(model_name)
        if not model:
            return ""
        
        lines = [
            f"class {model_name.capitalize()}QueryBuilder:",
            f"    def __init__(self, db):",
            f"        self.db = db",
            f"        self.table = '{model['table']}'",
            f"        self.query = ''",
            f"        self.params = []",
            f"        self._filters = []",
            f"        self._order_by = None",
            f"        self._limit = None",
            f"        self._offset = None",
            ""
        ]
        
        lines.append(f"    def filter(self, **kwargs):")
        lines.append(f"        for key, value in kwargs.items():")
        lines.append(f"            self._filters.append(f'{{key}} = %s')")
        lines.append(f"            self.params.append(value)")
        lines.append(f"        return self")
        ""
        
        lines.append(f"    def order_by(self, field: str, direction: str = 'ASC'):")
        lines.append(f"        self._order_by = f'{{field}} {{direction}}'")
        lines.append(f"        return self")
        ""
        
        lines.append(f"    def limit(self, count: int):")
        lines.append(f"        self._limit = count")
        lines.append(f"        return self")
        ""
        
        lines.append(f"    def offset(self, count: int):")
        lines.append(f"        self._offset = count")
        lines.append(f"        return self")
        ""
        
        lines.append(f"    def build(self) -> str:")
        lines.append(f"        query = f'SELECT * FROM {{self.table}}'")
        lines.append(f"        if self._filters:")
        lines.append(f"            query += f' WHERE {{' AND '.join(self._filters)}}'")
        lines.append(f"        if self._order_by:")
        lines.append(f"            query += f' ORDER BY {{self._order_by}}'")
        lines.append(f"        if self._limit:")
        lines.append(f"            query += f' LIMIT {{self._limit}}'")
        lines.append(f"        if self._offset:")
        lines.append(f"            query += f' OFFSET {{self._offset}}'")
        lines.append(f"        self.query = query")
        lines.append(f"        return query")
        ""
        
        lines.append(f"    def execute(self):")
        lines.append(f"        query = self.build()")
        lines.append(f"        return self.db.execute(query, self.params)")
        ""
        
        return "\n".join(lines)


class CacheManager:
    """Advanced caching layer with multiple strategies"""
    
    def __init__(self, strategy: CacheStrategy = CacheStrategy.TTL, default_ttl: int = 3600):
        self.cache: Dict[str, Dict] = {}
        self.strategy = strategy
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.logger = logging.getLogger(__name__)
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value with strategy support"""
        if key not in self.cache:
            self.misses += 1
            return None
        
        entry = self.cache[key]
        
        if self.strategy == CacheStrategy.TTL:
            if entry.get("expires_at") and datetime.now() > entry["expires_at"]:
                del self.cache[key]
                self.misses += 1
                self.evictions += 1
                return None
        
        self.hits += 1
        return entry.get("value")
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set cached value with TTL"""
        ttl = ttl or self.default_ttl
        entry = {
            "value": value,
            "created_at": datetime.now().isoformat(),
            "accessed_at": datetime.now().isoformat(),
            "access_count": 0
        }
        
        if self.strategy == CacheStrategy.TTL:
            entry["expires_at"] = datetime.now() + timedelta(seconds=ttl)
        
        self.cache[key] = entry
    
    def invalidate(self, key: str):
        """Invalidate cache entry"""
        if key in self.cache:
            del self.cache[key]
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate by pattern"""
        import re
        keys_to_delete = [
            key for key in self.cache.keys()
            if re.match(pattern, key)
        ]
        for key in keys_to_delete:
            del self.cache[key]
            self.evictions += 1
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "hit_rate": round(hit_rate, 2),
            "strategy": self.strategy.value
        }
    
    def cleanup_expired(self):
        """Remove expired entries"""
        if self.strategy != CacheStrategy.TTL:
            return
        
        now = datetime.now()
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.get("expires_at") and now > entry["expires_at"]
        ]
        
        for key in expired_keys:
            del self.cache[key]
            self.evictions += 1


class QueueManager:
    """Advanced message queue operations"""
    
    def __init__(self):
        self.queues: Dict[str, Dict] = {}
        self.dead_letter_queues: Dict[str, List] = defaultdict(list)
        self.workers: Dict[str, List] = defaultdict(list)
        self.logger = logging.getLogger(__name__)
    
    def add_queue(self, name: str, worker_count: int = 1,
                 max_retries: int = 3, visibility_timeout: int = 30):
        """Add message queue with advanced configuration"""
        self.queues[name] = {
            "worker_count": worker_count,
            "messages": [],
            "processed": 0,
            "failed": 0,
            "max_retries": max_retries,
            "visibility_timeout": visibility_timeout,
            "created_at": datetime.now().isoformat()
        }
    
    def enqueue(self, queue_name: str, message: Dict,
                priority: int = 0, delay: int = 0) -> bool:
        """Add message to queue with priority and delay support"""
        if queue_name not in self.queues:
            self.logger.error(f"Queue {queue_name} does not exist")
            return False
        
        message_entry = {
            "id": hashlib.md5(f"{queue_name}{time.time()}".encode()).hexdigest(),
            "body": message,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "retry_count": 0,
            "status": "pending"
        }
        
        if delay > 0:
            message_entry["available_at"] = (datetime.now() + timedelta(seconds=delay)).isoformat()
            message_entry["status"] = "delayed"
        
        queue = self.queues[queue_name]
        
        if priority > 0:
            queue["messages"].insert(0, message_entry)
        else:
            queue["messages"].append(message_entry)
        
        return True
    
    def dequeue(self, queue_name: str, visibility_timeout: Optional[int] = None) -> Optional[Dict]:
        """Get message from queue with visibility timeout"""
        if queue_name not in self.queues:
            return None
        
        queue = self.queues[queue_name]
        now = datetime.now()
        
        for i, msg in enumerate(queue["messages"]):
            if msg["status"] == "pending":
                available_at = msg.get("available_at")
                if available_at and datetime.fromisoformat(available_at) > now:
                    continue
                
                msg["status"] = "processing"
                msg["visibility_timeout"] = (now + timedelta(
                    seconds=visibility_timeout or queue["visibility_timeout"]
                )).isoformat()
                return msg
        
        return None
    
    def acknowledge(self, queue_name: str, message_id: str) -> bool:
        """Acknowledge message processing"""
        if queue_name not in self.queues:
            return False
        
        queue = self.queues[queue_name]
        queue["messages"] = [m for m in queue["messages"] if m.get("id") != message_id]
        queue["processed"] += 1
        return True
    
    def reject(self, queue_name: str, message_id: str, requeue: bool = False):
        """Reject message"""
        if queue_name not in self.queues:
            return
        
        queue = self.queues[queue_name]
        message = next((m for m in queue["messages"] if m.get("id") == message_id), None)
        
        if message:
            if requeue and message["retry_count"] < queue["max_retries"]:
                message["retry_count"] += 1
                message["status"] = "pending"
                message.pop("visibility_timeout", None)
            else:
                queue["messages"] = [m for m in queue["messages"] if m.get("id") != message_id]
                queue["failed"] += 1
                self.dead_letter_queues[queue_name].append(message)
    
    def get_stats(self, queue_name: str) -> Dict:
        """Get queue statistics"""
        if queue_name not in self.queues:
            return {}
        
        queue = self.queues[queue_name]
        pending = len([m for m in queue["messages"] if m["status"] == "pending"])
        processing = len([m for m in queue["messages"] if m["status"] == "processing"])
        delayed = len([m for m in queue["messages"] if m["status"] == "delayed"])
        
        return {
            "pending": pending,
            "processing": processing,
            "delayed": delayed,
            "processed": queue["processed"],
            "failed": queue["failed"],
            "workers": queue["worker_count"],
            "dead_letter": len(self.dead_letter_queues.get(queue_name, []))
        }
    
    def purge(self, queue_name: str) -> int:
        """Purge all messages from queue"""
        if queue_name not in self.queues:
            return 0
        
        count = len(self.queues[queue_name]["messages"])
        self.queues[queue_name]["messages"] = []
        return count


class GraphQLGenerator:
    """Advanced GraphQL schema generator"""
    
    def __init__(self):
        self.types: Dict[str, Dict] = {}
        self.queries: List[Dict] = []
        self.mutations: List[Dict] = []
        self.subscriptions: List[Dict] = []
        self.directives: List[Dict] = []
        self.interfaces: Dict[str, Dict] = {}
        self.unions: Dict[str, List[str]] = {}
        self.enums: Dict[str, List[str]] = {}
        self.inputs: Dict[str, Dict] = {}
    
    def add_type(self, name: str, fields: Dict, description: str = ""):
        """Add GraphQL type"""
        self.types[name] = {
            "fields": fields,
            "description": description,
            "interfaces": []
        }
    
    def add_interface(self, name: str, fields: Dict, description: str = ""):
        """Add GraphQL interface"""
        self.interfaces[name] = {
            "fields": fields,
            "description": description
        }
    
    def add_union(self, name: str, types: List[str], description: str = ""):
        """Add GraphQL union"""
        self.unions[name] = {
            "types": types,
            "description": description
        }
    
    def add_enum(self, name: str, values: List[str], description: str = ""):
        """Add GraphQL enum"""
        self.enums[name] = {
            "values": values,
            "description": description
        }
    
    def add_input(self, name: str, fields: Dict, description: str = ""):
        """Add GraphQL input type"""
        self.inputs[name] = {
            "fields": fields,
            "description": description
        }
    
    def add_query(self, name: str, return_type: str, resolver: str,
                 args: Dict = None, description: str = "", deprecation_reason: str = ""):
        """Add query"""
        self.queries.append({
            "name": name,
            "return_type": return_type,
            "resolver": resolver,
            "args": args or {},
            "description": description,
            "deprecation_reason": deprecation_reason
        })
    
    def add_mutation(self, name: str, input_type: str, return_type: str,
                    resolver: str, args: Dict = None, description: str = ""):
        """Add mutation"""
        self.mutations.append({
            "name": name,
            "input_type": input_type,
            "return_type": return_type,
            "resolver": resolver,
            "args": args or {},
            "description": description
        })
    
    def add_subscription(self, name: str, return_type: str, trigger: str,
                        description: str = ""):
        """Add subscription"""
        self.subscriptions.append({
            "name": name,
            "return_type": return_type,
            "trigger": trigger,
            "description": description
        })
    
    def add_directive(self, name: str, locations: List[str], args: Dict = None,
                     description: str = ""):
        """Add directive"""
        self.directives.append({
            "name": name,
            "locations": locations,
            "args": args or {},
            "description": description
        })
    
    def generate_schema(self) -> str:
        """Generate comprehensive GraphQL schema"""
        lines = []
        
        # Schema definition
        lines.append("""
# GraphQL Schema
# Generated: {datetime.now().isoformat()}

""")
        
        # Directives
        if self.directives:
            for directive in self.directives:
                lines.append(f"directive @{directive['name']}(")
                for arg_name, arg_type in directive.get("args", {}).items():
                    lines.append(f"  {arg_name}: {arg_type}")
                lines.append(f") on {', '.join(directive['locations'])}")
                lines.append("")
        
        # Enums
        for enum_name, enum_data in self.enums.items():
            lines.append(f"enum {enum_name} {{")
            for value in enum_data["values"]:
                lines.append(f"  {value}")
            lines.append("}")
            lines.append("")
        
        # Interfaces
        for interface_name, interface_data in self.interfaces.items():
            lines.append(f"interface {interface_name} {{")
            for field_name, field_type in interface_data["fields"].items():
                lines.append(f"  {field_name}: {field_type}")
            lines.append("}")
            lines.append("")
        
        # Types
        for type_name, type_data in self.types.items():
            lines.append(f"type {type_name} {{")
            for field_name, field_type in type_data["fields"].items():
                lines.append(f"  {field_name}: {field_type}")
            lines.append("}")
            lines.append("")
        
        # Inputs
        for input_name, input_data in self.inputs.items():
            lines.append(f"input {input_name} {{")
            for field_name, field_type in input_data["fields"].items():
                lines.append(f"  {field_name}: {field_type}")
            lines.append("}")
            lines.append("")
        
        # Unions
        for union_name, union_data in self.unions.items():
            lines.append(f"union {union_name} = {' | '.join(union_data['types'])}")
            lines.append("")
        
        # Query
        lines.append("type Query {")
        for q in self.queries:
            args_str = ", ".join([f"{k}: {v}" for k, v in q.get("args", {}).items()])
            args_line = f"({args_str})" if args_str else ""
            lines.append(f"  {q['name']}{args_line}: {q['return_type']}")
        lines.append("}")
        lines.append("")
        
        # Mutation
        lines.append("type Mutation {")
        for m in self.mutations:
            args_str = ", ".join([f"{k}: {v}" for k, v in m.get("args", {}).items()])
            input_line = f"(input: {m['input_type']})" if m['input_type'] else ""
            lines.append(f"  {m['name']}{input_line}: {m['return_type']}")
        lines.append("}")
        lines.append("")
        
        # Subscription
        if self.subscriptions:
            lines.append("type Subscription {")
            for s in self.subscriptions:
                lines.append(f"  {s['name']}: {s['return_type']}")
            lines.append("}")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_resolvers(self, framework: str = "python") -> str:
        """Generate resolver code"""
        if framework == "python":
            return self._generate_python_resolvers()
        elif framework == "javascript":
            return self._generate_javascript_resolvers()
        return ""
    
    def _generate_python_resolvers(self) -> str:
        """Generate Python resolvers"""
        lines = [
            "from typing import Optional, List, Dict, Any",
            "from dataclasses import dataclass",
            ""
        ]
        
        for q in self.queries:
            func_name = q["name"]
            lines.append(f"async def resolve_{func_name}(root, info, **kwargs) -> {q['return_type']}:")
            lines.append(f"    # {q.get('description', '')}")
            lines.append(f"    # TODO: Implement resolver")
            lines.append(f"    pass")
            lines.append("")
        
        for m in self.mutations:
            func_name = m["name"]
            lines.append(f"async def resolve_{func_name}(root, info, input: Dict[str, Any]) -> {m['return_type']}:")
            lines.append(f"    # {m.get('description', '')}")
            lines.append(f"    # TODO: Implement resolver")
            lines.append(f"    pass")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_javascript_resolvers(self) -> str:
        """Generate JavaScript resolvers"""
        lines = [
            "const resolvers = {",
            "  Query: {",
        ]
        
        for q in self.queries:
            func_name = q["name"]
            lines.append(f"    {func_name}: async (parent, args, context, info) => {{")
            lines.append(f"      // {q.get('description', '')}")
            lines.append(f"      // TODO: Implement resolver")
            lines.append(f"      return {{}};")
            lines.append(f"    }},")
        
        lines.append("  },")
        lines.append("  Mutation: {")
        
        for m in self.mutations:
            func_name = m["name"]
            lines.append(f"    {func_name}: async (parent, args, context, info) => {{")
            lines.append(f"      // {m.get('description', '')}")
            lines.append(f"      // TODO: Implement resolver")
            lines.append(f"      return {{}};")
            lines.append(f"    }},")
        
        lines.append("  },")
        lines.append("};")
        
        return "\n".join(lines)


class Logger:
    """Logging configuration and management"""
    
    def __init__(self, name: str, level: str = "INFO",
                 format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(format)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def get_logger(self) -> logging.Logger:
        """Get configured logger"""
        return self.logger


class ConfigManager:
    """Configuration management"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.validators: Dict[str, Callable] = {}
    
    def load_from_file(self, file_path: str):
        """Load configuration from file"""
        with open(file_path, 'r') as f:
            if file_path.endswith('.json'):
                self.config = json.load(f)
            elif file_path.endswith(('.yaml', '.yml')):
                import yaml
                self.config = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def validate(self) -> List[Dict]:
        """Validate configuration"""
        errors = []
        for key, validator in self.validators.items():
            value = self.get(key)
            try:
                validator(value)
            except Exception as e:
                errors.append({"key": key, "error": str(e)})
        return errors
    
    def add_validator(self, key: str, validator: Callable):
        """Add configuration validator"""
        self.validators[key] = validator
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return self.config.copy()
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.config, indent=2)


class HealthCheck:
    """Health check management"""
    
    def __init__(self):
        self.checks: Dict[str, Callable] = {}
        self.results: Dict[str, Dict] = {}
    
    def add_check(self, name: str, check_func: Callable, critical: bool = True):
        """Add health check"""
        self.checks[name] = {
            "func": check_func,
            "critical": critical,
            "last_check": None,
            "status": "unknown"
        }
    
    def run_checks(self) -> Dict:
        """Run all health checks"""
        results = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        for name, check in self.checks.items():
            try:
                start_time = time.time()
                result = check["func"]()
                duration = time.time() - start_time
                
                status = "healthy" if result else "unhealthy"
                check["status"] = status
                check["last_check"] = datetime.now().isoformat()
                
                results["checks"][name] = {
                    "status": status,
                    "duration_ms": round(duration * 1000, 2),
                    "critical": check["critical"],
                    "result": result
                }
                
                if not result and check["critical"]:
                    results["status"] = "unhealthy"
                    
            except Exception as e:
                check["status"] = "error"
                check["last_check"] = datetime.now().isoformat()
                results["checks"][name] = {
                    "status": "error",
                    "error": str(e),
                    "critical": check["critical"]
                }
                if check["critical"]:
                    results["status"] = "unhealthy"
        
        self.results = results
        return results
    
    def get_status(self) -> str:
        """Get overall health status"""
        if not self.results:
            self.run_checks()
        return self.results.get("status", "unknown")


class MetricsCollector:
    """Metrics collection and reporting"""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.counters: Dict[str, int] = defaultdict(int)
        self.logger = logging.getLogger(__name__)
    
    def record(self, name: str, value: float, tags: Dict = None):
        """Record metric value"""
        self.metrics[name].append({
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or {}
        })
    
    def increment(self, name: str, amount: int = 1, tags: Dict = None):
        """Increment counter"""
        self.counters[name] += amount
        self.metrics[name].append({
            "type": "counter",
            "value": self.counters[name],
            "timestamp": datetime.now().isoformat(),
            "tags": tags or {}
        })
    
    def histogram(self, name: str, value: float, tags: Dict = None):
        """Record histogram value"""
        self.metrics[name].append({
            "type": "histogram",
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or {}
        })
    
    def get_stats(self, name: str) -> Dict:
        """Get statistics for metric"""
        if name not in self.metrics:
            return {}
        
        values = [m["value"] for m in self.metrics[name] if "value" in m]
        if not values:
            return {}
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "p50": self._percentile(values, 50),
            "p95": self._percentile(values, 95),
            "p99": self._percentile(values, 99)
        }
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile"""
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format"""
        lines = []
        
        for name, values in self.metrics.items():
            for entry in values[-100:]:
                if "value" in entry:
                    tags_str = ",".join([f'{k}="{v}"' for k, v in entry.get("tags", {}).items()])
                    tags_str = f"{{{tags_str}}}" if tags_str else ""
                    lines.append(f"{name}{tags_str} {entry['value']}")
        
        for name, count in self.counters.items():
            lines.append(f"{name}_total {count}")
        
        return "\n".join(lines)


class CircuitBreaker:
    """Circuit breaker pattern implementation"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60,
                 half_open_requests: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_requests = half_open_requests
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.logger = logging.getLogger(__name__)
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker"""
        if self.state == "OPEN":
            if self.last_failure_time and \
               time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                self.logger.info("Circuit breaker transitioning to HALF_OPEN")
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call"""
        if self.state == "HALF_OPEN":
            self.success_count += 1
            if self.success_count >= self.half_open_requests:
                self.state = "CLOSED"
                self.failure_count = 0
                self.success_count = 0
                self.logger.info("Circuit breaker CLOSED")
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == "HALF_OPEN" or self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.logger.warning(f"Circuit breaker OPEN after {self.failure_count} failures")
    
    def get_state(self) -> Dict:
        """Get circuit breaker state"""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time
        }


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass


class RateLimitError(Exception):
    """Raised when rate limit is exceeded"""
    pass


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


class APIGateway:
    """API Gateway for routing and load balancing"""
    
    def __init__(self):
        self.routes: Dict[str, Dict] = {}
        self.middleware: List[Callable] = []
        self.rate_limiter = RateLimiter()
        self.load_balancers: Dict[str, List[str]] = {}
    
    def add_route(self, path: str, target: str, methods: List[str] = None,
                  auth_required: bool = False, rate_limit: Optional[int] = None):
        """Add route to gateway"""
        self.routes[path] = {
            "target": target,
            "methods": methods or ["GET"],
            "auth_required": auth_required,
            "rate_limit": rate_limit
        }
    
    def add_load_balancer(self, name: str, targets: List[str],
                         strategy: str = "round_robin"):
        """Add load balancer"""
        self.load_balancers[name] = {
            "targets": targets,
            "strategy": strategy,
            "current_index": 0
        }
    
    def route(self, path: str, method: str) -> Optional[str]:
        """Route request to target"""
        if path not in self.routes:
            return None
        
        route = self.routes[path]
        if method not in route["methods"]:
            return None
        
        return route["target"]
    
    def get_load_balanced_target(self, name: str) -> Optional[str]:
        """Get next target from load balancer"""
        if name not in self.load_balancers:
            return None
        
        lb = self.load_balancers[name]
        targets = lb["targets"]
        
        if not targets:
            return None
        
        if lb["strategy"] == "round_robin":
            target = targets[lb["current_index"]]
            lb["current_index"] = (lb["current_index"] + 1) % len(targets)
            return target
        elif lb["strategy"] == "random":
            import random
            return random.choice(targets)
        
        return targets[0]


class ServiceRegistry:
    """Service discovery and registry"""
    
    def __init__(self):
        self.services: Dict[str, Dict] = {}
        self.health_checks: Dict[str, Callable] = {}
    
    def register(self, name: str, host: str, port: int,
                health_check: Optional[Callable] = None, metadata: Dict = None):
        """Register service"""
        self.services[name] = {
            "host": host,
            "port": port,
            "url": f"http://{host}:{port}",
            "metadata": metadata or {},
            "registered_at": datetime.now().isoformat(),
            "last_health_check": None,
            "status": "unknown"
        }
        
        if health_check:
            self.health_checks[name] = health_check
    
    def deregister(self, name: str):
        """Deregister service"""
        self.services.pop(name, None)
        self.health_checks.pop(name, None)
    
    def get_service(self, name: str) -> Optional[Dict]:
        """Get service info"""
        return self.services.get(name)
    
    def discover(self, name: str) -> Optional[str]:
        """Discover service URL"""
        service = self.services.get(name)
        return service["url"] if service else None
    
    def check_health(self, name: str) -> Dict:
        """Check service health"""
        if name not in self.services:
            return {"status": "not_found"}
        
        service = self.services[name]
        
        if name in self.health_checks:
            try:
                healthy = self.health_checks[name]()
                service["status"] = "healthy" if healthy else "unhealthy"
            except Exception as e:
                service["status"] = "error"
                return {"status": "error", "error": str(e)}
        else:
            service["status"] = "unknown"
        
        service["last_health_check"] = datetime.now().isoformat()
        return {"status": service["status"]}
    
    def get_all_services(self) -> List[Dict]:
        """Get all registered services"""
        return [
            {"name": name, **service}
            for name, service in self.services.items()
        ]


class BackendAgent:
    """Main backend agent orchestrator"""
    
    def __init__(self, config: Dict = None):
        self.config = ConfigManager(config)
        self.logger = Logger("BackendAgent").get_logger()
        self.api_builder = APIBuilder()
        self.db_manager = DatabaseManager()
        self.cache_manager = CacheManager()
        self.queue_manager = QueueManager()
        self.graphql_generator = GraphQLGenerator()
        self.auth_manager: Optional[AuthenticationManager] = None
        self.health_check = HealthCheck()
        self.metrics = MetricsCollector()
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.api_gateway = APIGateway()
        self.service_registry = ServiceRegistry()
        
        self._setup_defaults()
    
    def _setup_defaults(self):
        """Setup default configuration"""
        self.add_endpoint = self.api_builder.add_endpoint
        self.generate_openapi = self.api_builder.generate_openapi
        self.generate_routes = self.api_builder.generate_routes
    
    def setup_auth(self, secret_key: str, algorithm: str = "HS256") -> AuthenticationManager:
        """Setup authentication"""
        self.auth_manager = AuthenticationManager(secret_key, algorithm)
        return self.auth_manager
    
    def add_circuit_breaker(self, name: str, **kwargs) -> CircuitBreaker:
        """Add circuit breaker"""
        cb = CircuitBreaker(**kwargs)
        self.circuit_breakers[name] = cb
        return cb
    
    def add_health_check(self, name: str, check_func: Callable, critical: bool = True):
        """Add health check"""
        self.health_check.add_check(name, check_func, critical)
    
    def run_health_checks(self) -> Dict:
        """Run health checks"""
        return self.health_check.run_checks()
    
    def record_metric(self, name: str, value: float, tags: Dict = None):
        """Record metric"""
        self.metrics.record(name, value, tags)
    
    def export_metrics(self) -> str:
        """Export metrics"""
        return self.metrics.export_prometheus()
    
    def validate_api(self) -> List[Dict]:
        """Validate API configuration"""
        return self.api_builder.validate_endpoints()
    
    def generate_full_stack(self, framework: APIFramework = APIFramework.FASTAPI) -> Dict:
        """Generate full stack code"""
        return {
            "routes": self.api_builder.generate_routes(framework),
            "openapi": self.api_builder.generate_openapi(),
            "models": self.db_manager.generate_models(framework=framework.value),
            "graphql_schema": self.graphql_generator.generate_schema(),
            "migrations": self._generate_all_migrations(),
            "dockerfile": self._generate_dockerfile(framework),
            "docker_compose": self._generate_docker_compose(),
            "requirements": self._generate_requirements(framework)
        }
    
    def _generate_all_migrations(self) -> str:
        """Generate all migrations"""
        migrations = []
        for model_name in self.db_manager.models:
            migrations.append(self.db_manager.generate_migrations(model_name))
        return "\n\n".join(migrations)
    
    def _generate_dockerfile(self, framework: APIFramework) -> str:
        """Generate Dockerfile"""
        base_images = {
            APIFramework.FASTAPI: "python:3.11-slim",
            APIFramework.EXPRESS: "node:20-alpine",
            APIFramework.SPRING: "openjdk:17-slim",
            APIFramework.DJANGO: "python:3.11-slim",
            APIFramework.FLASK: "python:3.11-slim"
        }
        
        return f"""
FROM {base_images.get(framework, 'python:3.11-slim')}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
"""
    
    def _generate_docker_compose(self) -> str:
        """Generate docker-compose.yml"""
        return """
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
"""
    
    def _generate_requirements(self, framework: APIFramework) -> str:
        """Generate requirements.txt"""
        base_requirements = [
            "fastapi==0.104.0",
            "uvicorn[standard]==0.24.0",
            "pydantic==2.5.0",
            "sqlalchemy==2.0.23",
            "alembic==1.12.1",
            "redis==5.0.1",
            "python-jose[cryptography]==3.3.0",
            "passlib[bcrypt]==1.7.4",
            "python-multipart==0.0.6",
            "python-dotenv==1.0.0",
            "pytest==7.4.3",
            "pytest-asyncio==0.21.1",
            "httpx==0.25.2"
        ]
        
        framework_specific = {
            APIFramework.EXPRESS: [],
            APIFramework.SPRING: [],
            APIFramework.DJANGO: [
                "django==4.2.7",
                "djangorestframework==3.14.0"
            ],
            APIFramework.FLASK: [
                "flask==2.3.3",
                "flask-sqlalchemy==3.1.1"
            ]
        }
        
        return "\n".join(base_requirements + framework_specific.get(framework, []))
    
    def generate_api_client(self, language: str = "python") -> str:
        """Generate API client code"""
        if language == "python":
            return self._generate_python_client()
        elif language == "javascript":
            return self._generate_javascript_client()
        elif language == "typescript":
            return self._generate_typescript_client()
        return ""
    
    def _generate_python_client(self) -> str:
        """Generate Python API client"""
        openapi = self.api_builder.generate_openapi()
        
        lines = [
            "import requests",
            "from typing import Optional, Dict, Any",
            "",
            f"class {self.api_builder.title.replace(' ', '')}Client:",
            f"    def __init__(self, base_url: str, api_key: Optional[str] = None):",
            f"        self.base_url = base_url.rstrip('/')",
            f"        self.api_key = api_key",
            f"        self.session = requests.Session()",
            f"        if api_key:",
            f"            self.session.headers.update({{'Authorization': f'Bearer {{api_key}}'}})",
            ""
        ]
        
        for e in self.api_builder.endpoints:
            func_name = e.path.replace('/', '_').strip('_').replace('{', '').replace('}', '')
            func_name = f"{e.method.lower()}_{func_name}"
            
            params = []
            for param_name in e.params:
                params.append(f"{param_name}: str = None")
            
            params_str = ", ".join(params)
            if params_str:
                params_str = f", {params_str}"
            
            lines.append(f"    def {func_name}(self{params_str}) -> Dict[str, Any]:")
            lines.append(f"        url = f'{{self.base_url}}{e.path}'")
            lines.append(f"        params = {{k: v for k, v in {{")
            for param_name in e.params:
                lines.append(f"            '{param_name}': {param_name},")
            lines.append(f"        }}.items() if v is not None}}")
            lines.append(f"        response = self.session.{e.method.lower()}(url, params=params)")
            lines.append(f"        response.raise_for_status()")
            lines.append(f"        return response.json()")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_javascript_client(self) -> str:
        """Generate JavaScript API client"""
        lines = [
            "class ApiClient {",
            f"  constructor(baseUrl, apiKey = null) {{",
            f"    this.baseUrl = baseUrl.replace(/\\/$/, '');",
            f"    this.headers = {{ 'Content-Type': 'application/json' }};",
            f"    if (apiKey) {{",
            f"      this.headers['Authorization'] = `Bearer ${{apiKey}}`;",
            f"    }}",
            f"  }}",
            ""
        ]
        
        for e in self.api_builder.endpoints:
            func_name = e.path.replace('/', '_').strip('_').replace('{', '').replace('}', '')
            func_name = f"{e.method.lower()}{func_name.capitalize()}"
            
            lines.append(f"  async {func_name}(params = {{}}) {{")
            lines.append(f"    const url = `${{this.baseUrl}}{e.path}`;")
            lines.append(f"    const response = await fetch(url, {{")
            lines.append(f"      method: '{e.method.upper()}',")
            lines.append(f"      headers: this.headers,")
            if e.method.upper() in ["POST", "PUT", "PATCH"]:
                lines.append(f"      body: JSON.stringify(params),")
            else:
                lines.append(f"      params,")
            lines.append(f"    }});")
            lines.append(f"    if (!response.ok) {{")
            lines.append(f"      throw new Error(`HTTP error! status: ${{response.status}}`);")
            lines.append(f"    }}")
            lines.append(f"    return await response.json();")
            lines.append(f"  }}")
            lines.append("")
        
        lines.append("}")
        lines.append("module.exports = ApiClient;")
        return "\n".join(lines)
    
    def _generate_typescript_client(self) -> str:
        """Generate TypeScript API client"""
        lines = [
            "export interface ApiClientConfig {",
            "  baseUrl: string;",
            "  apiKey?: string;",
            "}",
            "",
            "export interface ApiResponse<T> {",
            "  data: T;",
            "  status: number;",
            "  message?: string;",
            "}",
            "",
            f"export class {self.api_builder.title.replace(' ', '')}Client {{",
            f"  private baseUrl: string;",
            f"  private headers: Record<string, string>;",
            "",
            f"  constructor(config: ApiClientConfig) {{",
            f"    this.baseUrl = config.baseUrl.replace(/\\/$/, '');",
            f"    this.headers = { 'Content-Type': 'application/json' };",
            f"    if (config.apiKey) {{",
            f"      this.headers['Authorization'] = `Bearer ${{config.apiKey}}`;",
            f"    }}",
            f"  }}",
            ""
        ]
        
        for e in self.api_builder.endpoints:
            func_name = e.path.replace('/', '_').strip('_').replace('{', '').replace('}', '')
            func_name = f"{e.method.lower()}{func_name.capitalize()}"
            
            return_type = e.response_schema.get("type", "any")
            
            lines.append(f"  async {func_name}(params?: any): Promise<ApiResponse<{return_type}>> {{")
            lines.append(f"    const url = `${{this.baseUrl}}{e.path}`;")
            lines.append(f"    const options: RequestInit = {{")
            lines.append(f"      method: '{e.method.upper()}',")
            lines.append(f"      headers: this.headers,")
            if e.method.upper() in ["POST", "PUT", "PATCH"]:
                lines.append(f"      body: JSON.stringify(params),")
            lines.append(f"    }};")
            lines.append(f"    const response = await fetch(url, options);")
            lines.append(f"    if (!response.ok) {{")
            lines.append(f"      throw new Error(`HTTP error! status: ${{response.status}}`);")
            lines.append(f"    }}")
            lines.append(f"    const data = await response.json();")
            lines.append(f"    return {{ data, status: response.status }};")
            lines.append(f"  }}")
            lines.append("")
        
        lines.append("}")
        return "\n".join(lines)


class BackendAgent:
    """Main backend agent orchestrator - Advanced version"""
    
    def __init__(self, config: Dict = None):
        self.config = ConfigManager(config)
        self.logger = Logger("BackendAgent").get_logger()
        self.api_builder = APIBuilder()
        self.db_manager = DatabaseManager()
        self.cache_manager = CacheManager()
        self.queue_manager = QueueManager()
        self.graphql_generator = GraphQLGenerator()
        self.auth_manager: Optional[AuthenticationManager] = None
        self.health_check = HealthCheck()
        self.metrics = MetricsCollector()
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.api_gateway = APIGateway()
        self.service_registry = ServiceRegistry()
        
        self._setup_defaults()
        self._setup_default_checks()
    
    def _setup_defaults(self):
        """Setup default configuration"""
        self.add_endpoint = self.api_builder.add_endpoint
        self.generate_openapi = self.api_builder.generate_openapi
        self.generate_routes = self.api_builder.generate_routes
    
    def _setup_default_checks(self):
        """Setup default health checks"""
        self.add_health_check("api", lambda: True, critical=True)
        self.add_health_check("database", lambda: True, critical=True)
        self.add_health_check("cache", lambda: True, critical=False)
        self.add_health_check("queue", lambda: True, critical=False)
    
    def setup_auth(self, secret_key: str, algorithm: str = "HS256") -> AuthenticationManager:
        """Setup authentication"""
        self.auth_manager = AuthenticationManager(secret_key, algorithm)
        return self.auth_manager
    
    def add_circuit_breaker(self, name: str, **kwargs) -> CircuitBreaker:
        """Add circuit breaker"""
        cb = CircuitBreaker(**kwargs)
        self.circuit_breakers[name] = cb
        return cb
    
    def add_health_check(self, name: str, check_func: Callable, critical: bool = True):
        """Add health check"""
        self.health_check.add_check(name, check_func, critical)
    
    def run_health_checks(self) -> Dict:
        """Run health checks"""
        return self.health_check.run_checks()
    
    def record_metric(self, name: str, value: float, tags: Dict = None):
        """Record metric"""
        self.metrics.record(name, value, tags)
    
    def export_metrics(self) -> str:
        """Export metrics"""
        return self.metrics.export_prometheus()
    
    def validate_api(self) -> List[Dict]:
        """Validate API configuration"""
        return self.api_builder.validate_endpoints()
    
    def generate_full_stack(self, framework: APIFramework = APIFramework.FASTAPI) -> Dict:
        """Generate full stack code"""
        return {
            "routes": self.api_builder.generate_routes(framework),
            "openapi": self.api_builder.generate_openapi(),
            "models": self.db_manager.generate_models(framework=framework.value),
            "graphql_schema": self.graphql_generator.generate_schema(),
            "migrations": self._generate_all_migrations(),
            "dockerfile": self._generate_dockerfile(framework),
            "docker_compose": self._generate_docker_compose(),
            "requirements": self._generate_requirements(framework),
            "api_client_python": self.generate_api_client("python"),
            "api_client_javascript": self.generate_api_client("javascript"),
            "api_client_typescript": self.generate_api_client("typescript")
        }
    
    def _generate_all_migrations(self) -> str:
        """Generate all migrations"""
        migrations = []
        for model_name in self.db_manager.models:
            migrations.append(self.db_manager.generate_migrations(model_name))
        return "\n\n".join(migrations)
    
    def _generate_dockerfile(self, framework: APIFramework) -> str:
        """Generate Dockerfile"""
        base_images = {
            APIFramework.FASTAPI: "python:3.11-slim",
            APIFramework.EXPRESS: "node:20-alpine",
            APIFramework.SPRING: "openjdk:17-slim",
            APIFramework.DJANGO: "python:3.11-slim",
            APIFramework.FLASK: "python:3.11-slim"
        }
        
        return f"""
FROM {base_images.get(framework, 'python:3.11-slim')}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
"""
    
    def _generate_docker_compose(self) -> str:
        """Generate docker-compose.yml"""
        return """
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
"""
    
    def _generate_requirements(self, framework: APIFramework) -> str:
        """Generate requirements.txt"""
        base_requirements = [
            "fastapi==0.104.0",
            "uvicorn[standard]==0.24.0",
            "pydantic==2.5.0",
            "sqlalchemy==2.0.23",
            "alembic==1.12.1",
            "redis==5.0.1",
            "python-jose[cryptography]==3.3.0",
            "passlib[bcrypt]==1.7.4",
            "python-multipart==0.0.6",
            "python-dotenv==1.0.0",
            "pytest==7.4.3",
            "pytest-asyncio==0.21.1",
            "httpx==0.25.2"
        ]
        
        framework_specific = {
            APIFramework.EXPRESS: [],
            APIFramework.SPRING: [],
            APIFramework.DJANGO: [
                "django==4.2.7",
                "djangorestframework==3.14.0"
            ],
            APIFramework.FLASK: [
                "flask==2.3.3",
                "flask-sqlalchemy==3.1.1"
            ]
        }
        
        return "\n".join(base_requirements + framework_specific.get(framework, []))
    
    def generate_api_client(self, language: str = "python") -> str:
        """Generate API client code"""
        if language == "python":
            return self._generate_python_client()
        elif language == "javascript":
            return self._generate_javascript_client()
        elif language == "typescript":
            return self._generate_typescript_client()
        return ""
    
    def _generate_python_client(self) -> str:
        """Generate Python API client"""
        lines = [
            "import requests",
            "from typing import Optional, Dict, Any",
            "",
            f"class {self.api_builder.title.replace(' ', '')}Client:",
            f"    def __init__(self, base_url: str, api_key: Optional[str] = None):",
            f"        self.base_url = base_url.rstrip('/')",
            f"        self.api_key = api_key",
            f"        self.session = requests.Session()",
            f"        if api_key:",
            f"            self.session.headers.update({{'Authorization': f'Bearer {{api_key}}'}})",
            ""
        ]
        
        for e in self.api_builder.endpoints:
            func_name = e.path.replace('/', '_').strip('_').replace('{', '').replace('}', '')
            func_name = f"{e.method.lower()}_{func_name}"
            
            params = []
            for param_name in e.params:
                params.append(f"{param_name}: str = None")
            
            params_str = ", ".join(params)
            if params_str:
                params_str = f", {params_str}"
            
            lines.append(f"    def {func_name}(self{params_str}) -> Dict[str, Any]:")
            lines.append(f"        url = f'{{self.base_url}}{e.path}'")
            lines.append(f"        params = {{k: v for k, v in {{")
            for param_name in e.params:
                lines.append(f"            '{param_name}': {param_name},")
            lines.append(f"        }}.items() if v is not None}}")
            lines.append(f"        response = self.session.{e.method.lower()}(url, params=params)")
            lines.append(f"        response.raise_for_status()")
            lines.append(f"        return response.json()")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_javascript_client(self) -> str:
        """Generate JavaScript API client"""
        lines = [
            "class ApiClient {",
            f"  constructor(baseUrl, apiKey = null) {{",
            f"    this.baseUrl = baseUrl.replace(/\\/$/, '');",
            f"    this.headers = {{ 'Content-Type': 'application/json' }};",
            f"    if (apiKey) {{",
            f"      this.headers['Authorization'] = `Bearer ${{apiKey}}`;",
            f"    }}",
            f"  }}",
            ""
        ]
        
        for e in self.api_builder.endpoints:
            func_name = e.path.replace('/', '_').strip('_').replace('{', '').replace('}', '')
            func_name = f"{e.method.lower()}{func_name.capitalize()}"
            
            lines.append(f"  async {func_name}(params = {{}}) {{")
            lines.append(f"    const url = `${{this.baseUrl}}{e.path}`;")
            lines.append(f"    const response = await fetch(url, {{")
            lines.append(f"      method: '{e.method.upper()}',")
            lines.append(f"      headers: this.headers,")
            if e.method.upper() in ["POST", "PUT", "PATCH"]:
                lines.append(f"      body: JSON.stringify(params),")
            else:
                lines.append(f"      params,")
            lines.append(f"    }});")
            lines.append(f"    if (!response.ok) {{")
            lines.append(f"      throw new Error(`HTTP error! status: ${{response.status}}`);")
            lines.append(f"    }}")
            lines.append(f"    return await response.json();")
            lines.append(f"  }}")
            lines.append("")
        
        lines.append("}")
        lines.append("module.exports = ApiClient;")
        return "\n".join(lines)
    
    def _generate_typescript_client(self) -> str:
        """Generate TypeScript API client"""
        lines = [
            "export interface ApiClientConfig {",
            "  baseUrl: string;",
            "  apiKey?: string;",
            "}",
            "",
            "export interface ApiResponse<T> {",
            "  data: T;",
            "  status: number;",
            "  message?: string;",
            "}",
            "",
            f"export class {self.api_builder.title.replace(' ', '')}Client {{",
            f"  private baseUrl: string;",
            f"  private headers: Record<string, string>;",
            "",
            f"  constructor(config: ApiClientConfig) {{",
            f"    this.baseUrl = config.baseUrl.replace(/\\/$/, '');",
            f"    this.headers = {{ 'Content-Type': 'application/json' }};",
            f"    if (config.apiKey) {{",
            f"      this.headers['Authorization'] = `Bearer ${{config.apiKey}}`;",
            f"    }}",
            f"  }}",
            ""
        ]
        
        for e in self.api_builder.endpoints:
            func_name = e.path.replace('/', '_').strip('_').replace('{', '').replace('}', '')
            func_name = f"{e.method.lower()}{func_name.capitalize()}"
            
            return_type = e.response_schema.get("type", "any")
            
            lines.append(f"  async {func_name}(params?: any): Promise<ApiResponse<{return_type}>> {{")
            lines.append(f"    const url = `${{this.baseUrl}}{e.path}`;")
            lines.append(f"    const options: RequestInit = {{")
            lines.append(f"      method: '{e.method.upper()}',")
            lines.append(f"      headers: this.headers,")
            if e.method.upper() in ["POST", "PUT", "PATCH"]:
                lines.append(f"      body: JSON.stringify(params),")
            lines.append(f"    }};")
            lines.append(f"    const response = await fetch(url, options);")
            lines.append(f"    if (!response.ok) {{")
            lines.append(f"      throw new Error(`HTTP error! status: ${{response.status}}`);")
            lines.append(f"    }}")
            lines.append(f"    const data = await response.json();")
            lines.append(f"    return {{ data, status: response.status }};")
            lines.append(f"  }}")
            lines.append("")
        
        lines.append("}")
        return "\n".join(lines)
    
    def run(self) -> Dict:
        """Run backend agent and generate comprehensive output"""
        self.logger.info("Running Backend Agent...")
        
        results = {
            "openapi_spec": self.api_builder.generate_openapi(),
            "routes": {},
            "models": list(self.db_manager.models.keys()),
            "cache_stats": self.cache_manager.get_stats(),
            "queue_stats": {},
            "health_status": self.run_health_checks(),
            "metrics_summary": {
                name: self.metrics.get_stats(name)
                for name in self.metrics.metrics.keys()
            },
            "validation": self.validate_api(),
            "circuit_breakers": {
                name: cb.get_state()
                for name, cb in self.circuit_breakers.items()
            }
        }
        
        for framework in APIFramework:
            results[f"routes_{framework.value}"] = self.api_builder.generate_routes(framework)
        
        for queue_name in self.queue_manager.queues:
            results["queue_stats"][queue_name] = self.queue_manager.get_stats(queue_name)
        
        self.logger.info("Backend Agent completed successfully")
        return results


if __name__ == "__main__":
    agent = BackendAgent()
    
    agent.add_endpoint(
        "/users",
        "GET",
        "Get all users",
        params={"page": {"type": "integer", "required": False}, "limit": {"type": "integer", "required": False}},
        response_schema={"type": "array", "items": {"type": "object"}},
        auth_required=True,
        rate_limit=100,
        cache_ttl=300,
        tags=["users"],
        version="v1"
    )
    
    agent.add_endpoint(
        "/users/{id}",
        "GET",
        "Get user by ID",
        params={"id": {"type": "string", "required": True}},
        response_schema={"type": "object"},
        auth_required=True,
        tags=["users"],
        version="v1"
    )
    
    agent.add_endpoint(
        "/users",
        "POST",
        "Create user",
        request_body={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "password": {"type": "string", "format": "password"}
            },
            "required": ["name", "email", "password"]
        },
        response_schema={"type": "object"},
        auth_required=False,
        error_responses={
            "400": {"description": "Validation error"},
            "409": {"description": "User already exists"}
        },
        tags=["users"],
        version="v1"
    )
    
    agent.db_manager.create_model(
        "User",
        [
            ModelField("id", "uuid", primary_key=True),
            ModelField("name", "str", max_length=100, required=True),
            ModelField("email", "str", max_length=255, unique=True, required=True),
            ModelField("password_hash", "str", max_length=255, required=True),
            ModelField("created_at", "datetime", default="NOW()"),
            ModelField("updated_at", "datetime", default="NOW()")
        ],
        indexes=[
            {"name": "idx_users_email", "columns": ["email"], "unique": True},
            {"name": "idx_users_created", "columns": ["created_at"]}
        ]
    )
    
    agent.db_manager.add_relationship("User", "one_to_many", "Order", "user_id")
    
    agent.setup_auth("your-secret-key-here")
    
    agent.add_circuit_breaker("database", failure_threshold=5, recovery_timeout=60)
    agent.add_circuit_breaker("external_api", failure_threshold=3, recovery_timeout=30)
    
    agent.add_health_check("database", lambda: True, critical=True)
    agent.add_health_check("redis", lambda: True, critical=False)
    
    agent.cache_manager.set("config:app", {"version": "1.0.0"}, ttl=3600)
    
    agent.queue_manager.add_queue("notifications", worker_count=3, max_retries=5)
    agent.queue_manager.enqueue("notifications", {
        "type": "email",
        "to": "user@example.com",
        "subject": "Welcome!",
        "body": "Welcome to our platform"
    }, priority=1)
    
    agent.graphql_generator.add_type("User", {
        "id": "ID!",
        "name": "String!",
        "email": "String!",
        "orders": "[Order!]!"
    })
    agent.graphql_generator.add_query("getUser", "User", "resolve_user")
    agent.graphql_generator.add_mutation("createUser", "CreateUserInput!", "User!")
    
    agent.service_registry.register(
        "user-service",
        "localhost",
        8001,
        metadata={"version": "1.0.0", "env": "development"}
    )
    
    result = agent.run()
    
    print(f"API endpoints: {len(agent.api_builder.endpoints)}")
    print(f"Database models: {result['models']}")
    print(f"Cache stats: {result['cache_stats']}")
    print(f"Queue stats: {result['queue_stats']}")
    print(f"Health status: {result['health_status']['status']}")
    print(f"Validation issues: {len(result['validation'])}")
    print(f"Circuit breakers: {list(result['circuit_breakers'].keys())}")
