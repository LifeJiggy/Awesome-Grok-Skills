"""
Supabase Authentication Pipeline
Supabase auth and database patterns
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import hashlib


class AuthProvider(Enum):
    EMAIL = "email"
    PHONE = "phone"
    GOOGLE = "google"
    GITHUB = "github"
    TWITTER = "twitter"
    DISCORD = "discord"


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"
    GUEST = "guest"


@dataclass
class User:
    id: str
    email: str
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime
    email_confirmed: bool
    phone_confirmed: bool
    role: UserRole
    metadata: Dict


@dataclass
class Session:
    access_token: str
    refresh_token: str
    user_id: str
    expires_at: datetime
    token_type: str = "bearer"


class SupabaseAuth:
    """Supabase authentication utilities"""
    
    def __init__(self, url: str, anon_key: str):
        self.url = url
        self.anon_key = anon_key
    
    def sign_up(self, 
               email: str,
               password: str,
               metadata: Dict = None) -> Dict:
        """Sign up new user"""
        return {
            "url": f"{self.url}/auth/v1/signup",
            "method": "POST",
            "body": {
                "email": email,
                "password": password,
                "data": metadata or {}
            },
            "headers": {
                "apikey": self.anon_key,
                "Content-Type": "application/json"
            }
        }
    
    def sign_in(self, 
               email: str,
               password: str) -> Dict:
        """Sign in with email/password"""
        return {
            "url": f"{self.url}/auth/v1/token?grant_type=password",
            "method": "POST",
            "body": {
                "email": email,
                "password": password
            },
            "headers": {
                "apikey": self.anon_key,
                "Content-Type": "application/json"
            }
        }
    
    def sign_in_oauth(self, 
                     provider: AuthProvider,
                     redirect_to: str = None) -> str:
        """Generate OAuth sign-in URL"""
        base_url = f"{self.url}/auth/v1/authorize"
        
        params = {
            "provider": provider.value,
            "redirect_to": redirect_to or f"{self.url}/auth/callback"
        }
        
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{param_str}"
    
    def verify_token(self, token: str) -> Dict:
        """Verify and decode JWT token"""
        return {
            "url": f"{self.url}/auth/v1/user",
            "method": "GET",
            "headers": {
                "Authorization": f"Bearer {token}",
                "apikey": self.anon_key
            }
        }
    
    def refresh_session(self, refresh_token: str) -> Dict:
        """Refresh access token"""
        return {
            "url": f"{self.url}/auth/v1/token?grant_type=refresh_token",
            "method": "POST",
            "body": {
                "refresh_token": refresh_token
            },
            "headers": {
                "apikey": self.anon_key,
                "Content-Type": "application/json"
            }
        }
    
    def sign_out(self, access_token: str) -> Dict:
        """Sign out user"""
        return {
            "url": f"{self.url}/auth/v1/logout",
            "method": "POST",
            "headers": {
                "Authorization": f"Bearer {access_token}",
                "apikey": self.anon_key
            }
        }
    
    def reset_password(self, email: str) -> Dict:
        """Send password reset email"""
        return {
            "url": f"{self.url}/auth/v1/recover",
            "method": "POST",
            "body": {
                "email": email
            },
            "headers": {
                "apikey": self.anon_key,
                "Content-Type": "application/json"
            }
        }


class RLSManager:
    """Row Level Security policy manager"""
    
    def __init__(self):
        self.policies = {}
    
    def create_policy(self, 
                     table: str,
                     policy_name: str,
                     operation: str,
                     using_expression: str,
                     check_expression: str = None) -> str:
        """Generate RLS policy SQL"""
        policy = f"""
CREATE POLICY "{policy_name}" ON "{table}"
FOR {operation.upper()}
TO authenticated
USING ({using_expression});
"""
        if check_expression:
            policy += f"""
WITH CHECK ({check_expression});
"""
        return policy
    
    def generate_user_is_owner_policy(self, 
                                     table: str,
                                     user_id_column: str = "user_id") -> str:
        """Generate user ownership policy"""
        return self.create_policy(
            table,
            f"users_can_only_own_data_{table}",
            "ALL",
            f"auth.uid() = {user_id_column}",
            f"auth.uid() = {user_id_column}"
        )
    
    def generate_role_based_policy(self, 
                                  table: str,
                                  role: UserRole,
                                  operations: List[str] = ["SELECT"]) -> str:
        """Generate role-based access policy"""
        policies = []
        
        for op in operations:
            policies.append(self.create_policy(
                table,
                f"{role.value}_can_{op}_{table}",
                op,
                f"auth.role() = '{role.value}'"
            ))
        
        return "\n".join(policies)
    
    def generate_time_based_policy(self, 
                                  table: str,
                                  timestamp_column: str = "created_at",
                                  days_old: int = 30) -> str:
        """Generate time-based access policy"""
        return self.create_policy(
            table,
            f"access_recent_{table}",
            "SELECT",
            f"{timestamp_column} > now() - interval '{days_old} days'"
        )


class SupabaseClient:
    """Supabase database client utilities"""
    
    def __init__(self, url: str, anon_key: str):
        self.url = url
        self.anon_key = anon_key
    
    def create_client(self, access_token: str = None) -> str:
        """Generate Supabase client initialization"""
        token_param = f'"session": {{ "accessToken": "{access_token}" }}' if access_token else ""
        
        return f"""
import {{ createClient }} from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {{
  auth: {{
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }},
  global: {{
    headers: {{ 'x-application-name': 'my-app' }}
  }}
}});

{self._generate_helper_functions()}
"""
    
    def _generate_helper_functions(self) -> str:
        """Generate helper functions"""
        return """
export const getUser = async () => {
  const { data: { user } } = await supabase.auth.getUser();
  return user;
};

export const getSession = async () => {
  const { data: { session } } = await supabase.auth.getSession();
  return session;
};

export const onAuthStateChange = (callback) => {
  return supabase.auth.onAuthStateChange(callback);
};

export const signUp = async (email, password, metadata) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: { data: metadata }
  });
  return { data, error };
};

export const signIn = async (email, password) => {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  });
  return { data, error };
};

export const signOut = async () => {
  const { error } = await supabase.auth.signOut();
  return { error };
};
"""
    
    def generate_insert(self, 
                       table: str,
                       data: Dict,
                       returning: str = "minimal") -> str:
        """Generate insert query"""
        columns = ", ".join(data.keys())
        values = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in data.values()])
        
        return f"""
const {{ data, error }} = await supabase
  .from('{table}')
  .insert([{{ {', '.join([f"{k}: {repr(v)}" for k, v in data.items()])} }}])
  .select('{returning}');
"""
    
    def generate_select(self, 
                       table: str,
                       filters: Dict = None,
                       select_columns: str = "*",
                       order_by: str = None,
                       limit: int = None) -> str:
        """Generate select query"""
        query = f"supabase.from('{table}').select('{select_columns}')"
        
        if filters:
            for key, value in filters.items():
                query += f".eq('{key}', {repr(value)})"
        
        if order_by:
            query += f".order('{order_by}', {{ ascending: true }})"
        
        if limit:
            query += f".limit({limit})"
        
        query += "; const { data, error } = await "
        return f"const {{ data, error }} = {query}"
    
    def generate_update(self,
                       table: str,
                       data: Dict,
                       filters: Dict) -> str:
        """Generate update query"""
        set_clause = ", ".join([f"{k}: {repr(v)}" for k, v in data.items()])
        
        query = f"supabase.from('{table}').update({{ {set_clause} }})"
        
        for key, value in filters.items():
            query += f".eq('{key}', {repr(value)})"
        
        query += "; const { data, error } = await "
        return f"const {{ data, error }} = {query}"
    
    def generate_delete(self, 
                       table: str,
                       filters: Dict) -> str:
        """Generate delete query"""
        query = f"supabase.from('{table}').delete()"
        
        for key, value in filters.items():
            query += f".eq('{key}', {repr(value)})"
        
        query += "; const { data, error } = await "
        return f"const {{ data, error }} = {query}"


class DatabaseSchema:
    """Supabase database schema utilities"""
    
    @staticmethod
    def generate_table_definition(table_name: str,
                                  columns: Dict,
                                  primary_key: str = "id",
                                  timestamps: bool = True) -> str:
        """Generate table creation SQL"""
        col_defs = []
        
        for col, col_type in columns.items():
            col_defs.append(f'  {col} {col_type}')
        
        if timestamps:
            col_defs.extend([
                "  created_at timestamptz default now()",
                "  updated_at timestamptz default now()"
            ])
        
        col_defs.append(f"  PRIMARY KEY ({primary_key})")
        
        return f"""
CREATE TABLE {table_name} (
{chr(10).join(col_defs)}
);

ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;
"""
    
    @staticmethod
    def generate_foreign_key(column: str, 
                           ref_table: str,
                           ref_column: str = "id") -> str:
        """Generate foreign key constraint"""
        return f"""
ALTER TABLE ADD CONSTRAINT fk_{column}
FOREIGN KEY ({column}) REFERENCES {ref_table}({ref_column});
"""
    
    @staticmethod
    def generate_index(table: str,
                      columns: List[str],
                      index_name: str = None,
                      unique: bool = False) -> str:
        """Generate index creation SQL"""
        index_name = index_name or f"idx_{table}_{'_'.join(columns)}"
        unique_key = "UNIQUE" if unique else ""
        
        return f"CREATE {unique_key} INDEX {index_name} ON {table}({', '.join(columns)});"


if __name__ == "__main__":
    auth = SupabaseAuth("https://example.supabase.co", "anon-key")
    rls = RLSManager()
    client = SupabaseClient("https://example.supabase.co", "anon-key")
    schema = DatabaseSchema()
    
    signup = auth.sign_up("user@example.com", "password123")
    signin_url = auth.sign_in_oauth(AuthProvider.GOOGLE)
    
    policy = rls.generate_user_is_owner_policy("posts")
    
    client_code = client.create_client()
    insert_code = client.generate_insert("users", {"email": "test@example.com", "name": "Test"})
    select_code = client.generate_select("users", {"role": "admin"}, "email,name", "created_at", 10)
    
    table_sql = schema.generate_table_definition(
        "posts",
        {
            "id": "uuid default gen_random_uuid()",
            "title": "text not null",
            "content": "text",
            "user_id": "uuid references auth.users"
        }
    )
    
    index_sql = schema.generate_index("posts", ["user_id", "created_at"])
    
    print(f"Sign up URL: {signup['url']}")
    print(f"OAuth URL: {signin_url}")
    print(f"RLS Policy: {len(policy)} chars")
    print(f"Client code: {len(client_code)} chars")
    print(f"Table SQL: {len(table_sql)} chars")
