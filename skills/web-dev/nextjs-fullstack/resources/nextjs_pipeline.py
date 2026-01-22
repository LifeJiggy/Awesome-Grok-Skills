"""
Next.js Full-Stack Pipeline
Production-ready Next.js patterns and utilities
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class RenderMode(Enum):
    SSR = "ssr"
    SSG = "ssg"
    ISR = "isr"
    CSR = "csr"


@dataclass
class PageConfig:
    path: str
    render_mode: RenderMode
    revalidate: int = 60
    cache_control: str = "public, max-age=60"
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class NextJSRouter:
    """Next.js App Router utilities"""
    
    @staticmethod
    def generate_route(params: Dict) -> str:
        """Generate dynamic route from params"""
        segments = []
        for key, value in params.items():
            if isinstance(value, list):
                segments.extend([f"[{key}]={v}" for v in value])
            else:
                segments.append(f"[{key}]={value}")
        return "/".join(segments)
    
    @staticmethod
    def parse_route(path: str) -> Dict:
        """Parse dynamic route parameters"""
        params = {}
        segments = path.split("/")
        
        for i, segment in enumerate(segments):
            if segment.startswith("[") and segment.endswith("]"):
                key = segment[1:-1]
                if key.endswith("..."):
                    key = key[:-3]
                    params[key] = segments[i+1:]
                else:
                    params[key] = segments[i+1]
        
        return params
    
    @staticmethod
    def generate_metadata(title: str,
                         description: str,
                         image: str = None,
                         theme_color: str = "#000000") -> Dict:
        """Generate Next.js metadata object"""
        return {
            "metadataBase": "https://example.com",
            "title": {
                "default": title,
                "template": "%s | Example"
            },
            "description": description,
            "openGraph": {
                "title": title,
                "description": description,
                "type": "website",
                "images": [image] if image else []
            },
            "twitter": {
                "card": "summary_large_image",
                "title": title,
                "description": description,
                "images": [image] if image else []
            },
            "themeColor": theme_color
        }


class APIRouteBuilder:
    """API route handler builder"""
    
    def __init__(self, base_path: str = "/api"):
        self.base_path = base_path
        self.handlers = {}
    
    def add_endpoint(self, 
                    path: str,
                    methods: List[str] = ["GET"]) -> str:
        """Generate API route file content"""
        handler_name = path.replace("[", "").replace("]", "").replace("-", "_")
        
        imports = """
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  
  try {
    const data = await getData(id);
    return NextResponse.json({ data });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch data' },
      { status: 500 }
    );
  }
}
"""
        
        return imports
    
    def add_validation(self, 
                      schema: Dict,
                      body_param: str = "body") -> str:
        """Add Zod validation"""
        return f"""
const {body_param}Schema = z.object({self._dict_to_zod(schema)});

function validate(body: any) {{
  try {{
    {body_param}Schema.parse(body);
    return {{ valid: true, errors: [] }};
  }} catch (error) {{
    return {{
      valid: false,
      errors: error.errors.map((e: any) => ({{
        path: e.path.join('.'),
        message: e.message
      }}))
    }};
  }}
}}
"""
    
    def _dict_to_zod(self, schema: Dict, indent: int = 2) -> str:
        """Convert dict to Zod schema string"""
        lines = []
        for key, value in schema.items():
            if isinstance(value, str):
                lines.append(f"{key}: z.string()")
            elif isinstance(value, int):
                lines.append(f"{key}: z.number()")
            elif isinstance(value, bool):
                lines.append(f"{key}: z.boolean()")
            elif isinstance(value, list):
                lines.append(f"{key}: z.array(z.string())")
            elif isinstance(value, dict):
                lines.append(f"{key}: z.object({{")
                lines.append(self._dict_to_zod(value, indent + 2))
                lines.append("})")
        return "\n".join(lines)


class ServerComponentBuilder:
    """React Server Component utilities"""
    
    @staticmethod
    def async_data_fetch(fetch_url: str, 
                        cache_strategy: str = "force-cache") -> str:
        """Generate async data fetch pattern"""
        return f"""
async function getData() {{
  const res = await fetch('{fetch_url}', {{
    next: {{ revalidate: 60 }}
  }});
  
  if (!res.ok) {{
    throw new Error('Failed to fetch data');
  }}
  
  return res.json();
}}
"""
    
    @staticmethod
    def streaming_component(suspense_key: str) -> str:
        """Generate streaming component pattern"""
        return f"""
import {{ Suspense }} from 'react';

export function {suspense_key.title().replace('_', '')}() {{
  return (
    <Suspense fallback={<Skeleton />}>
      <DataContent />
    </Suspense>
  );
}}

async function DataContent() {{
  const data = await getData();
  return <div>{{data}}</div>;
}}
"""


class NextAuthConfig:
    """NextAuth.js configuration builder"""
    
    @staticmethod
    def generate_config(provider: str = "credentials") -> str:
        """Generate NextAuth configuration"""
        return f"""
import NextAuth from 'next-auth';
import {{ {provider} }} from 'next-auth/providers';

export const authOptions = {{
  providers: [
    {provider}({{
      credentials: {{
        email: {{ label: 'Email', type: 'email' }},
        password: {{ label: 'Password', type: 'password' }}
      }},
      async authorize(credentials) {{
        const user = await authenticateUser(credentials);
        if (user) {{
          return user;
        }}
        return null;
      }}
    }})
  ],
  pages: {{
    signIn: '/auth/signin',
    error: '/auth/error'
  }},
  callbacks: {{
    async jwt({{ token, user }}) {{
      if (user) {{
        token.id = user.id;
      }}
      return token;
    }},
    async session({{ session, token }}) {{
      session.user.id = token.id;
      return session;
    }}
  }},
  session: {{
    strategy: 'jwt'
  }}
}};

const handler = NextAuth(authOptions);
export {{ handler as GET, handler as POST }};
"""
    
    @staticmethod
    def generate_middleware() -> str:
        """Generate middleware for route protection"""
        return """
import { withAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";

export default withAuth(
  function middleware(req) {
    const token = req.nextauth.token;
    const path = req.nextUrl.pathname;
    
    if (path.startsWith("/admin") && token?.role !== "admin") {
      return NextResponse.redirect(new URL("/unauthorized", req.url));
    }
    
    return NextResponse.next();
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token,
    },
  }
);

export const config = {
  matcher: ["/dashboard/:path*", "/admin/:path*"],
};
"""


class SWRConfig:
    """SWR configuration for client-side data fetching"""
    
    @staticmethod
    def generate_hooks(key: str, 
                      fetcher_url: str,
                      options: Dict = None) -> str:
        """Generate SWR hook configuration"""
        opts = options or {}
        
        return f"""
import useSWR from 'swr';

const fetcher = (url: string) => 
  fetch(url).then(res => res.json());

export function useData() {{
  const {{ data, error, isLoading, mutate }} = useSWR(
    '{key}',
    fetcher,
    {{
      revalidateOnFocus: {str(opts.get('revalidateOnFocus', True))},
      dedupingInterval: {opts.get('dedupingInterval', 2000)},
      refreshInterval: {opts.get('refreshInterval', 0)},
      fallbackData: null,
      onSuccess: (data) => console.log('Data fetched:', data),
      onError: (err) => console.error('Fetch error:', err)
    }}
  );

  return {{
    data,
    error,
    isLoading,
    mutate
  }};
}}
"""


class TailwindConfig:
    """Tailwind CSS configuration"""
    
    @staticmethod
    def generate_tailwind_config(colors: Dict = None) -> str:
        """Generate tailwind.config.js"""
        custom_colors = colors or {
            "primary": "#3B82F6",
            "secondary": "#10B981",
            "accent": "#F59E0B"
        }
        
        colors_str = ",\n    ".join([f"{name}: '{value}'" for name, value in custom_colors.items()])
        
        return f"""
/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: [
    './pages/**/*.{{js,ts,jsx,tsx,mdx}}',
    './components/**/*.{{js,ts,jsx,tsx,mdx}}',
    './app/**/*.{{js,ts,jsx,tsx,mdx}}',
  ],
  theme: {{
    extend: {{
      colors: {{
        {colors_str}
      }},
      fontFamily: {{
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-mono)', 'monospace'],
      }},
      animation: {{
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      }},
      keyframes: {{
        fadeIn: {{
          '0%': {{ opacity: 0 }},
          '100%': {{ opacity: 1 }},
        }},
        slideUp: {{
          '0%': {{ transform: 'translateY(10px)', opacity: 0 }},
          '100%': {{ transform: 'translateY(0)', opacity: 1 }},
        }},
      }},
    }},
  }},
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')],
}};
"""


if __name__ == "__main__":
    router = NextJSRouter()
    api_builder = APIRouteBuilder()
    nextauth = NextAuthConfig()
    tailwind = TailwindConfig()
    
    route = router.generate_route({"id": "123", "slug": "my-post"})
    parsed = router.parse_route("/posts/[id]/comments/[commentId]")
    metadata = router.generate_metadata("My Page", "Description")
    
    api_code = api_builder.add_endpoint("/users/[id]", ["GET", "PUT"])
    
    auth_config = nextauth.generate_config("credentials")
    middleware = nextauth.generate_middleware()
    
    swr_hook = SWRConfig.generate_hooks("users", "/api/users")
    
    tailwind_config = tailwind.generate_tailwind_config({
        "brand": "#6366F1",
        "success": "#22C55E",
        "warning": "#F59E0B"
    })
    
    print(f"Route: {route}")
    print(f"Parsed params: {parsed}")
    print(f"Metadata keys: {list(metadata.keys())}")
    print(f"API code length: {len(api_code)} chars")
    print(f"Auth config length: {len(auth_config)} chars")
    print(f"Tailwind config generated: {len(tailwind_config)} chars")
