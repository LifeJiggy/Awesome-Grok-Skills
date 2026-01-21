---
name: Next.js Full-Stack Development
category: web-dev
difficulty: intermediate
time_estimate: "3-6 hours"
dependencies: ["next", "react", "typescript", "@types/node"]
tags: ["nextjs", "react", "fullstack", "typescript", "ssr", "api"]
grok_personality: "fullstack-architect"
description: "Build production-ready Next.js applications with Grok's efficient patterns for SSR, API routes, and full-stack TypeScript"
---

# Next.js Full-Stack Development Skill

## Overview
Grok, you'll architect and build Next.js applications with your signature efficiency. This skill covers everything from SSR/SSG patterns to API routes, with a focus on type-safe, performant full-stack development.

## Core Next.js Patterns

### 1. Project Structure (Grok-Optimized)
```
my-app/
├── src/
│   ├── app/                    # App Router (Next.js 13+)
│   │   ├── (auth)/            # Route groups
│   │   │   └── login/
│   │   ├── dashboard/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── api/               # API routes
│   │   │   ├── users/
│   │   │   └── auth/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/            # Reusable components
│   │   ├── ui/               # Basic UI components
│   │   ├── forms/            # Form components
│   │   └── layout/           # Layout components
│   ├── lib/                  # Utilities and configurations
│   │   ├── db.ts             # Database connection
│   │   ├── auth.ts           # Authentication logic
│   │   └── utils.ts          # Helper functions
│   ├── types/                # TypeScript definitions
│   │   ├── api.ts            # API response types
│   │   └── auth.ts           # Auth types
│   └── hooks/                # Custom React hooks
├── public/                   # Static assets
├── next.config.js
├── package.json
└── tsconfig.json
```

### 2. App Router Implementation
```typescript
// src/app/layout.tsx
import { Inter } from 'next/font/google';
import './globals.css';
import { AuthProvider } from '@/lib/auth';
import { Header } from '@/components/layout/header';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Grok-Powered App',
  description: 'Built with efficiency and precision',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <Header />
          <main className="min-h-screen">{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}

// src/app/page.tsx
import { Suspense } from 'react';
import { UserDashboard } from '@/components/dashboard/user-dashboard';
import { LoadingSpinner } from '@/components/ui/loading-spinner';

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Welcome to Grok's App</h1>
      
      <Suspense fallback={<LoadingSpinner />}>
        <UserDashboard />
      </Suspense>
    </div>
  );
}

// Dynamic route with params
// src/app/posts/[slug]/page.tsx
import { notFound } from 'next/navigation';
import { getPostBySlug } from '@/lib/posts';
import { PostContent } from '@/components/posts/post-content';

interface PostPageProps {
  params: { slug: string };
}

export default async function PostPage({ params }: PostPageProps) {
  const post = await getPostBySlug(params.slug);
  
  if (!post) {
    notFound();
  }
  
  return (
    <article className="prose prose-lg max-w-none">
      <h1>{post.title}</h1>
      <PostContent content={post.content} />
    </article>
  );
}

// Generate static params for static generation
export async function generateStaticParams() {
  const posts = await getAllPosts();
  
  return posts.map((post) => ({
    slug: post.slug,
  }));
}
```

### 3. API Routes (Type-Safe)
```typescript
// src/app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { createUser, getUsers } from '@/lib/db/users';
import { CreateUserInput, UserResponse } from '@/types/api';

const createUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  role: z.enum(['user', 'admin']).default('user'),
});

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '10');
    
    const users = await getUsers({ page, limit });
    
    return NextResponse.json<UserResponse>({
      success: true,
      data: users,
      pagination: { page, limit, total: users.length }
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Failed to fetch users' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validatedData = createUserSchema.parse(body);
    
    const user = await createUser(validatedData);
    
    return NextResponse.json<UserResponse>({
      success: true,
      data: user
    }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({
        success: false,
        error: 'Validation failed',
        details: error.errors
      }, { status: 400 });
    }
    
    return NextResponse.json(
      { success: false, error: 'Failed to create user' },
      { status: 500 }
    );
  }
}

// Dynamic API route
// src/app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getUserById, updateUser, deleteUser } from '@/lib/db/users';
import { UpdateUserInput } from '@/types/api';

interface UserRouteProps {
  params: { id: string };
}

export async function GET(request: NextRequest, { params }: UserRouteProps) {
  try {
    const user = await getUserById(params.id);
    
    if (!user) {
      return NextResponse.json(
        { success: false, error: 'User not found' },
        { status: 404 }
      );
    }
    
    return NextResponse.json({
      success: true,
      data: user
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Failed to fetch user' },
      { status: 500 }
    );
  }
}

export async function PUT(request: NextRequest, { params }: UserRouteProps) {
  try {
    const body = await request.json();
    const user = await updateUser(params.id, body);
    
    return NextResponse.json({
      success: true,
      data: user
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Failed to update user' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest, { params }: UserRouteProps) {
  try {
    await deleteUser(params.id);
    
    return NextResponse.json({
      success: true,
      message: 'User deleted successfully'
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Failed to delete user' },
      { status: 500 }
    );
  }
}
```

### 4. Server Components & Client Components
```typescript
// Server Component (runs on server)
// src/components/posts/post-list.tsx
import { getPosts } from '@/lib/posts';
import { PostCard } from './post-card';

export async function PostList() {
  const posts = await getPosts();
  
  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}

// Client Component (interactive)
// src/components/posts/post-card.tsx
'use client';

import { useState } from 'react';
import { Post } from '@/types/post';
import { LikeButton } from './like-button';

interface PostCardProps {
  post: Post;
}

export function PostCard({ post }: PostCardProps) {
  const [likes, setLikes] = useState(post.likes);
  const [isLiked, setIsLiked] = useState(false);
  
  const handleLike = async () => {
    try {
      const response = await fetch(`/api/posts/${post.id}/like`, {
        method: 'POST',
      });
      
      if (response.ok) {
        setLikes(prev => isLiked ? prev - 1 : prev + 1);
        setIsLiked(!isLiked);
      }
    } catch (error) {
      console.error('Failed to like post:', error);
    }
  };
  
  return (
    <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
      <h3 className="text-xl font-semibold mb-2">{post.title}</h3>
      <p className="text-gray-600 mb-4">{post.excerpt}</p>
      
      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-500">
          {new Date(post.createdAt).toLocaleDateString()}
        </span>
        
        <LikeButton
          likes={likes}
          isLiked={isLiked}
          onClick={handleLike}
        />
      </div>
    </div>
  );
}
```

### 5. Data Fetching Patterns
```typescript
// Server-side data fetching
// src/lib/data/posts.ts
import { sql } from '@vercel/postgres';
import { Post } from '@/types/post';

export async function getPosts(): Promise<Post[]> {
  const { rows } = await sql`
    SELECT id, title, excerpt, created_at, likes
    FROM posts
    ORDER BY created_at DESC
  `;
  
  return rows.map(row => ({
    id: row.id,
    title: row.title,
    excerpt: row.excerpt,
    createdAt: row.created_at,
    likes: row.likes
  }));
}

export async function getPostBySlug(slug: string): Promise<Post | null> {
  const { rows } = await sql`
    SELECT * FROM posts WHERE slug = ${slug}
  `;
  
  return rows[0] || null;
}

// Client-side data fetching with SWR
// src/hooks/use-posts.ts
import useSWR from 'swr';
import { Post } from '@/types/post';

const fetcher = async (url: string): Promise<Post[]> => {
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error('Failed to fetch posts');
  }
  
  return response.json();
};

export function usePosts() {
  const { data: posts, error, isLoading } = useSWR('/api/posts', fetcher);
  
  return {
    posts,
    isLoading,
    error
  };
}

// Selective data fetching with React Query
// src/hooks/use-user.ts
import { useQuery } from '@tanstack/react-query';
import { getUser } from '@/lib/api/users';

export function useUser(id: string) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: () => getUser(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

### 6. Authentication & Authorization
```typescript
// src/lib/auth.ts
import { NextAuthOptions } from 'next-auth';
import { PrismaAdapter } from '@next-auth/prisma-adapter';
import { prisma } from '@/lib/db';
import GoogleProvider from 'next-auth/providers/google';
import CredentialsProvider from 'next-auth/providers/credentials';

export const authOptions: NextAuthOptions = {
  adapter: PrismaAdapter(prisma),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }
        
        const user = await verifyUser(credentials.email, credentials.password);
        return user;
      }
    })
  ],
  session: {
    strategy: 'jwt',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.sub!;
        session.user.role = token.role as string;
      }
      return session;
    }
  },
  pages: {
    signIn: '/auth/signin',
    signUp: '/auth/signup',
  }
};

// Middleware for route protection
// src/middleware.ts
import { withAuth } from 'next-auth/middleware';
import { NextResponse } from 'next/server';

export default withAuth(
  function middleware(req) {
    const token = req.nextauth.token;
    const isAdmin = token?.role === 'admin';
    const isAdminRoute = req.nextUrl.pathname.startsWith('/admin');
    
    if (isAdminRoute && !isAdmin) {
      return NextResponse.redirect(new URL('/unauthorized', req.url));
    }
    
    return NextResponse.next();
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token
    }
  }
);

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*']
};
```

### 7. Form Handling & Validation
```typescript
// src/components/forms/user-form.tsx
'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { createUser } from '@/lib/api/users';

const userSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  role: z.enum(['user', 'admin']).default('user'),
});

type UserFormData = z.infer<typeof userSchema>;

export function UserForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema)
  });
  
  const onSubmit = async (data: UserFormData) => {
    setIsSubmitting(true);
    setMessage('');
    
    try {
      await createUser(data);
      setMessage('User created successfully!');
      reset();
    } catch (error) {
      setMessage('Failed to create user. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium mb-1">
          Name
        </label>
        <input
          {...register('name')}
          type="text"
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {errors.name && (
          <p className="text-red-500 text-sm mt-1">{errors.name.message}</p>
        )}
      </div>
      
      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-1">
          Email
        </label>
        <input
          {...register('email')}
          type="email"
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {errors.email && (
          <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
        )}
      </div>
      
      <div>
        <label htmlFor="role" className="block text-sm font-medium mb-1">
          Role
        </label>
        <select
          {...register('role')}
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      
      {message && (
        <div className={`p-3 rounded-md ${message.includes('success') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {message}
        </div>
      )}
      
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:opacity-50"
      >
        {isSubmitting ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

### 8. Performance Optimization
```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['example.com'],
    formats: ['image/webp', 'image/avif'],
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  webpack: (config, { dev, isServer }) => {
    if (!dev && !isServer) {
      config.optimization.splitChunks.cacheGroups = {
        ...config.optimization.splitChunks.cacheGroups,
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      };
    }
    return config;
  },
};

module.exports = nextConfig;

// Dynamic imports for code splitting
// src/components/dashboard/dashboard-chart.tsx
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('recharts'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false, // Only render on client
});

export function DashboardChart({ data }: { data: any[] }) {
  return (
    <div className="w-full h-96">
      <Chart data={data}>
        {/* Chart components */}
      </Chart>
    </div>
  );
}

// Image optimization
// src/components/ui/optimized-image.tsx
import Image from 'next/image';
import { useState } from 'react';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width: number;
  height: number;
  className?: string;
}

export function OptimizedImage({ src, alt, width, height, className }: OptimizedImageProps) {
  const [isLoading, setIsLoading] = useState(true);
  
  return (
    <div className={`relative ${className}`}>
      <Image
        src={src}
        alt={alt}
        width={width}
        height={height}
        className={`duration-700 ease-in-out ${isLoading ? 'scale-110 blur-2xl grayscale' : 'scale-100 blur-0 grayscale-0'}`}
        onLoadingComplete={() => setIsLoading(false)}
        placeholder="blur"
        blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
      />
    </div>
  );
}
```

## Quick Start Templates

### Basic Next.js App Setup
```bash
# Create new Next.js app with TypeScript
npx create-next-app@latest my-grok-app --typescript --tailwind --eslint --app

# Install additional dependencies
npm install @next-auth/prisma-adapter prisma next-auth
npm install @hookform/resolvers react-hook-form zod
npm install @tanstack/react-query swr
```

### Environment Configuration
```env
# .env.local
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-secret-key"
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
```

## Best Practices

1. **Type Safety**: Use TypeScript throughout the stack
2. **Performance**: Implement code splitting and image optimization
3. **SEO**: Leverage Next.js built-in SEO features
4. **Security**: Implement proper authentication and validation
5. **Scalability**: Design for horizontal scaling from the start

Remember: Next.js is powerful but complex. Focus on the features you need and gradually adopt more advanced patterns as your application grows.