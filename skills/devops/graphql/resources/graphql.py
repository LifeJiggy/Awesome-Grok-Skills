class GraphQL:
    def __init__(self):
        self.schema = None

    def create_schema(self, query_type_name="Query", mutation_type_name="Mutation", subscription_type_name="Subscription"):
        self.schema = {
            "query": query_type_name,
            "mutation": mutation_type_name,
            "subscription": subscription_type_name,
            "types": {},
            "directives": [],
            "description": None
        }
        return self

    def create_object_type(self, type_name, fields, description=None, implements=None):
        type_def = {
            "kind": "OBJECT",
            "name": type_name,
            "description": description,
            "fields": fields,
            "interfaces": implements or []
        }
        self.schema["types"][type_name] = type_def
        return type_def

    def create_scalar_type(self, type_name, description=None):
        type_def = {"kind": "SCALAR", "name": type_name, "description": description}
        self.schema["types"][type_name] = type_def
        return type_def

    def create_enum_type(self, type_name, values, description=None):
        type_def = {
            "kind": "ENUM",
            "name": type_name,
            "description": description,
            "values": values
        }
        self.schema["types"][type_name] = type_def
        return type_def

    def create_interface_type(self, type_name, fields, description=None):
        type_def = {
            "kind": "INTERFACE",
            "name": type_name,
            "description": description,
            "fields": fields,
            "possibleTypes": []
        }
        self.schema["types"][type_name] = type_def
        return type_def

    def create_union_type(self, type_name, types, description=None):
        type_def = {
            "kind": "UNION",
            "name": type_name,
            "description": description,
            "types": types
        }
        self.schema["types"][type_name] = type_def
        return type_def

    def create_input_type(self, type_name, fields, description=None):
        type_def = {
            "kind": "INPUT_OBJECT",
            "name": type_name,
            "description": description,
            "inputFields": fields
        }
        self.schema["types"][type_name] = type_def
        return type_def

    def create_field(self, field_name, field_type, args=None, description=None, deprecation_reason=None):
        field = {
            "name": field_name,
            "type": field_type,
            "description": description,
            "args": args or [],
            "deprecationReason": deprecation_reason
        }
        return field

    def create_argument(self, arg_name, arg_type, default_value=None, description=None):
        return {
            "name": arg_name,
            "type": {"kind": "NON_NULL", "ofType": {"kind": "SCALAR", "name": arg_type}} if default_value is None else {"name": arg_name, "type": {"kind": "SCALAR", "name": arg_type}, "defaultValue": default_value, "description": description}
        }

    def create_non_null_type(self, of_type):
        return {"kind": "NON_NULL", "ofType": of_type}

    def create_list_type(self, of_type):
        return {"kind": "LIST", "ofType": of_type}

    def create_query_type(self, fields):
        self.schema["types"]["Query"] = {
            "kind": "OBJECT",
            "name": "Query",
            "fields": fields
        }
        return self

    def create_mutation_type(self, fields):
        self.schema["types"]["Mutation"] = {
            "kind": "OBJECT",
            "name": "Mutation",
            "fields": fields
        }
        return self

    def create_subscription_type(self, fields):
        self.schema["types"]["Subscription"] = {
            "kind": "OBJECT",
            "name": "Subscription",
            "fields": fields
        }
        return self

    def create_directive(self, name, locations, args=None, description=None):
        directive = {
            "name": name,
            "locations": locations,
            "args": args or [],
            "description": description
        }
        self.schema["directives"].append(directive)
        return directive

    def create_query_field(self, field_name, return_type, args=None, description=None, resolver=None):
        return self.create_field(field_name, return_type, args, description)

    def create_mutation_field(self, field_name, input_type, return_type, description=None):
        arg = {"name": "input", "type": {"kind": "NON_NULL", "ofType": {"kind": "INPUT_OBJECT", "name": input_type}}}
        return self.create_field(field_name, return_type, [arg], description)

    def create_subscription_field(self, field_name, return_type, description=None):
        return self.create_field(field_name, return_type, [], description)

    def add_query_field(self, type_name, field_name, field_type, args=None):
        if "Query" in self.schema["types"]:
            self.schema["types"]["Query"]["fields"].append(self.create_field(field_name, field_type, args or []))
        return self

    def create_pagination_info(self):
        return self.create_object_type(
            "PageInfo",
            {
                "hasNextPage": {"type": {"kind": "SCALAR", "name": "Boolean"}},
                "hasPreviousPage": {"type": {"kind": "SCALAR", "name": "Boolean"}},
                "startCursor": {"type": {"kind": "SCALAR", "name": "String"}},
                "endCursor": {"type": {"kind": "SCALAR", "name": "String"}}
            },
            description="Information about pagination"
        )

    def create_edge_type(self, node_type_name):
        return self.create_object_type(
            f"{node_type_name}Edge",
            {
                "node": {"type": {"kind": "OBJECT", "name": node_type_name}},
                "cursor": {"type": {"kind": "SCALAR", "name": "String"}}
            },
            description=f"An edge in a connection to a {node_type_name}"
        )

    def create_connection_type(self, node_type_name):
        edge_type_name = f"{node_type_name}Edge"
        self.create_edge_type(node_type_name)
        return self.create_object_type(
            f"{node_type_name}Connection",
            {
                "edges": {"type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": edge_type_name}}},
                "pageInfo": {"type": {"kind": "OBJECT", "name": "PageInfo"}},
                "totalCount": {"type": {"kind": "SCALAR", "name": "Int"}}
            },
            description=f"A connection to a list of {node_type_name}"
        )

    def create_order_enum(self, direction_values=["ASC", "DESC"]):
        return self.create_enum_type("OrderDirection", direction_values)

    def create_order_input(self, field_name, order_enum_name="OrderDirection"):
        return self.create_input_type(
            f"OrderBy{field_name}",
            {
                "field": {"type": {"kind": "SCALAR", "name": "String"}},
                "direction": {"type": {"kind": "ENUM", "name": order_enum_name}}
            }
        )

    def create_filter_input(self, filter_fields):
        return self.create_input_type(
            f"{filter_fields[0].capitalize()}Filter",
            {field: {"type": {"kind": "SCALAR", "name": "String"}} for field in filter_fields}
        )

    def configure_auth_directive(self, requires_auth=False, roles=None):
        return self.create_directive(
            name="auth",
            locations=["FIELD_DEFINITION", "OBJECT"],
            args=[{"name": "requiresAuth", "type": {"kind": "SCALAR", "name": "Boolean"}, "defaultValue": str(requires_auth).lower()}],
            description="Directive for authentication"
        )

    def configure_cache_directive(self, max_age=3600, scope="PUBLIC"):
        return self.create_directive(
            name="cache",
            locations=["FIELD_DEFINITION"],
            args=[
                {"name": "maxAge", "type": {"kind": "SCALAR", "name": "Int"}, "defaultValue": str(max_age)},
                {"name": "scope", "type": {"kind": "SCALAR", "name": "String"}, "defaultValue": scope}
            ],
            description="Directive for caching"
        )

    def create_schema_directive(self, name, implementation):
        return self.create_directive(
            name=name,
            locations=["SCHEMA"],
            description="Schema directive"
        )
