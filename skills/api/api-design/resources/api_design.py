class APIDesign:
    def __init__(self):
        self.api_spec = None

    def create_openapi_spec(self, title, version, description=None):
        self.api_spec = {
            "openapi": "3.1.0",
            "info": {
                "title": title,
                "version": version,
                "description": description,
                "contact": {"name": "API Support", "email": "support@example.com"},
                "license": {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
            },
            "servers": [],
            "paths": {},
            "components": {
                "schemas": {},
                "securitySchemes": {}
            }
        }
        return self

    def add_server(self, url, description=None, variables=None):
        if self.api_spec:
            self.api_spec["servers"].append({
                "url": url,
                "description": description,
                "variables": variables or {}
            })
        return self

    def create_path(self, path, operations=None):
        if self.api_spec:
            self.api_spec["paths"][path] = operations or {}
        return self

    def add_operation(self, path, method, operation_id, summary, description=None, tags=None, parameters=None, request_body=None, responses=None, security=None):
        if path in self.api_spec["paths"]:
            self.api_spec["paths"][path][method] = {
                "operationId": operation_id,
                "summary": summary,
                "description": description,
                "tags": tags or [],
                "parameters": parameters or [],
                "requestBody": request_body,
                "responses": responses or {"200": {"description": "Success"}},
                "security": security or []
            }
        return self

    def create_parameter(self, name, param_in, description=None, required=False, deprecated=False, schema=None):
        return {
            "name": name,
            "in": param_in,
            "description": description,
            "required": required,
            "deprecated": deprecated,
            "schema": schema or {"type": "string"}
        }

    def create_request_body(self, description=None, required=False, content_type="application/json", schema=None):
        return {
            "description": description,
            "required": required,
            "content": {
                content_type: {
                    "schema": schema
                }
            }
        }

    def create_response(self, status_code, description, schema=None, headers=None):
        response = {"description": description}
        if schema:
            response["content"] = {
                "application/json": {
                    "schema": schema
                }
            }
        if headers:
            response["headers"] = headers
        return {str(status_code): response}

    def create_schema(self, schema_name, schema_type="object", properties=None, required=None, description=None):
        schema = {
            "type": schema_type,
            "description": description
        }
        if properties:
            schema["properties"] = properties
        if required:
            schema["required"] = required
        if self.api_spec:
            self.api_spec["components"]["schemas"][schema_name] = schema
        return schema

    def create_object_property(self, property_name, property_type, description=None, nullable=True, example=None):
        prop = {"type": property_type, "nullable": nullable}
        if description:
            prop["description"] = description
        if example:
            prop["example"] = example
        return {property_name: prop}

    def create_array_property(self, property_name, item_schema, description=None):
        return {property_name: {"type": "array", "items": item_schema, "description": description}}

    def create_reference(self, schema_name):
        return {"$ref": f"#/components/schemas/{schema_name}"}

    def create_security_scheme(self, scheme_name, scheme_type, description=None, bearer_format=None, flows=None):
        security_scheme = {"type": scheme_type, "description": description}
        if scheme_type == "http" and bearer_format:
            security_scheme["bearerFormat"] = bearer_format
        if scheme_type == "oauth2" and flows:
            security_scheme["flows"] = flows
        if scheme_type == "apiKey":
            security_scheme["name"] = "api_key"
            security_scheme["in"] = "header"
        if self.api_spec:
            self.api_spec["components"]["securitySchemes"][scheme_name] = security_scheme
        return security_scheme

    def create_oauth_flow(self, authorization_url, token_url, scopes=None):
        return {
            "implicit": {
                "authorizationUrl": authorization_url,
                "scopes": scopes or {}
            },
            "authorizationCode": {
                "authorizationUrl": authorization_url,
                "tokenUrl": token_url,
                "scopes": scopes or {}
            }
        }

    def add_tag(self, name, description=None):
        if self.api_spec:
            if "tags" not in self.api_spec:
                self.api_spec["tags"] = []
            self.api_spec["tags"].append({"name": name, "description": description})
        return self

    def create_webhook(self, webhook_name, url, description=None):
        if self.api_spec:
            if "webhooks" not in self.api_spec:
                self.api_spec["webhooks"] = {}
            self.api_spec["webhooks"][webhook_name] = {
                "url": url,
                "description": description
            }
        return self

    def create_link(self, operation_id, description=None, parameters=None):
        return {
            "operationId": operation_id,
            "description": description,
            "parameters": parameters or {}
        }

    def add_example(self, example_name, value, summary=None, description=None):
        if "examples" not in self.api_spec.get("components", {}):
            self.api_spec["components"]["examples"] = {}
        self.api_spec["components"]["examples"][example_name] = {
            "value": value,
            "summary": summary,
            "description": description
        }
        return self

    def configure_rate_limiting(self, requests_per_minute=60, burst=100):
        if self.api_spec:
            self.api_spec["x-rate-limiting"] = {
                "requests_per_minute": requests_per_minute,
                "burst": burst
            }
        return self

    def add_deprecation_notice(self, deprecation_date, sunset_date, alternative=None):
        if self.api_spec:
            self.api_spec["x-deprecation"] = {
                "deprecation_date": deprecation_date,
                "sunset_date": sunset_date,
                "alternative": alternative
            }
        return self

    def create_versioning_strategy(self, strategy="header", header_name="API-Version", url_pattern="/v{version}"):
        if self.api_spec:
            self.api_spec["x-api-versioning"] = {
                "strategy": strategy,
                "header_name": header_name,
                "url_pattern": url_pattern
            }
        return self

    def create_error_schema(self, error_code, error_message, error_type="object"):
        return {
            "type": error_type,
            "properties": {
                "error": self.create_object_property("error", "object", "Error details"),
                "code": self.create_object_property("code", "integer", "Error code"),
                "message": self.create_object_property("message", "string", "Error message"),
                "timestamp": self.create_object_property("timestamp", "string", "Timestamp of the error")
            }
        }

    def create_pagination_params(self, limit_param="limit", offset_param="offset", max_limit=100):
        return [
            self.create_parameter(limit_param, "query", "Maximum items to return", required=False, schema={"type": "integer", "default": 20, "maximum": max_limit}),
            self.create_parameter(offset_param, "query", "Offset for pagination", required=False, schema={"type": "integer", "default": 0})
        ]

    def create_sorting_params(self, default_field="created_at", default_order="desc", available_fields=None):
        return [
            self.create_parameter("sort_by", "query", "Field to sort by", required=False, schema={"type": "string", "default": default_field}),
            self.create_parameter("sort_order", "query", "Sort order (asc or desc)", required=False, schema={"type": "string", "enum": ["asc", "desc"], "default": default_order})
        ]
