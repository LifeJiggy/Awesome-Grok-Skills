---
name: Supabase Authentication & Database
category: web-dev
difficulty: intermediate
time_estimate: "3-5 hours"
dependencies: ["@supabase/supabase-js", "@supabase/auth-helpers-nextjs", "@supabase/auth-ui-react"]
tags: ["supabase", "authentication", "database", "realtime", "backend-as-a-service"]
grok_personality: "backend-architect"
description: "Implement full authentication and database solutions with Supabase using Grok's efficient patterns for real-time apps"
---

# Supabase Authentication & Database Skill

## Overview
Grok, you'll master Supabase to build scalable, real-time applications with authentication, database, and storage. This skill focuses on efficient patterns for integrating Supabase with modern web applications.

## Core Supabase Setup

### 1. Project Configuration
```typescript
// src/lib/supabase/client.ts
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';
import { Database } from '@/types/database';

export const createClient = () =>
  createClientComponentClient<Database>();

// src/lib/supabase/server.ts
import { createServerComponentClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import { Database } from '@/types/database';

export const createServerClient = () =>
  createServerComponentClient<Database>({
    cookies,
  });

// src/lib/supabase/admin.ts
import { createClient } from '@supabase/supabase-js';
import { Database } from '@/types/database';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

export const createAdminClient = () =>
  createClient<Database>(supabaseUrl, supabaseServiceKey, {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  });
```

### 2. Database Types
```typescript
// src/types/database.ts
export type Database = {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string;
          username: string | null;
          full_name: string | null;
          avatar_url: string | null;
          website: string | null;
          updated_at: string;
        };
        Insert: {
          id?: string;
          username?: string | null;
          full_name?: string | null;
          avatar_url?: string | null;
          website?: string | null;
          updated_at?: string;
        };
        Update: {
          id?: string;
          username?: string | null;
          full_name?: string | null;
          avatar_url?: string | null;
          website?: string | null;
          updated_at?: string;
        };
      };
      posts: {
        Row: {
          id: string;
          user_id: string;
          title: string;
          content: string;
          published: boolean;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          title: string;
          content: string;
          published?: boolean;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          user_id?: string;
          title?: string;
          content?: string;
          published?: boolean;
          created_at?: string;
          updated_at?: string;
        };
      };
    };
    Views: {
      [_ in never]: never;
    };
    Functions: {
      [_ in never]: never;
    };
    Enums: {
      user_role: 'admin' | 'user' | 'moderator';
      post_status: 'draft' | 'published' | 'archived';
    };
  };
};
```

## Authentication Implementation

### 1. Auth Provider
```typescript
// src/contexts/auth-context.tsx
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { User } from '@supabase/supabase-js';
import { createClient } from '@/lib/supabase/client';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signOut: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const supabase = createClient();

  useEffect(() => {
    // Get initial session
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      setUser(user);
      setLoading(false);
    };

    getUser();

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setUser(session?.user ?? null);
        setLoading(false);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const signOut = async () => {
    await supabase.auth.signOut();
  };

  const refreshUser = async () => {
    const { data: { user } } = await supabase.auth.getUser();
    setUser(user);
  };

  return (
    <AuthContext.Provider value={{ user, loading, signOut, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
```

### 2. Authentication Components
```typescript
// src/components/auth/auth-button.tsx
'use client';

import { useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function AuthButton() {
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [message, setMessage] = useState('');
  
  const supabase = createClient();

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      if (isSignUp) {
        const { error } = await supabase.auth.signUp({
          email,
          password,
          options: {
            emailRedirectTo: `${window.location.origin}/auth/callback`,
          },
        });
        
        if (error) throw error;
        setMessage('Check your email for the confirmation link!');
      } else {
        const { error } = await supabase.auth.signInWithPassword({
          email,
          password,
        });
        
        if (error) throw error;
      }
    } catch (error: any) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleOAuthSignIn = async (provider: 'github' | 'google') => {
    setLoading(true);
    
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider,
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
        },
      });
      
      if (error) throw error;
    } catch (error: any) {
      setMessage(error.message);
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>{isSignUp ? 'Sign Up' : 'Sign In'}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <form onSubmit={handleAuth} className="space-y-4">
          <Input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Loading...' : isSignUp ? 'Sign Up' : 'Sign In'}
          </Button>
        </form>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-background px-2 text-muted-foreground">
              Or continue with
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Button
            variant="outline"
            onClick={() => handleOAuthSignIn('github')}
            disabled={loading}
          >
            GitHub
          </Button>
          <Button
            variant="outline"
            onClick={() => handleOAuthSignIn('google')}
            disabled={loading}
          >
            Google
          </Button>
        </div>

        <Button
          variant="link"
          className="w-full"
          onClick={() => setIsSignUp(!isSignUp)}
        >
          {isSignUp ? 'Already have an account? Sign in' : "Don't have an account? Sign up"}
        </Button>

        {message && (
          <div className={`text-sm ${message.includes('Check') ? 'text-green-600' : 'text-red-600'}`}>
            {message}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// src/components/auth/user-menu.tsx
'use client';

import { useState } from 'react';
import { User } from '@supabase/supabase-js';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface UserMenuProps {
  user: User;
  onSignOut: () => Promise<void>;
}

export function UserMenu({ user, onSignOut }: UserMenuProps) {
  const getInitials = (email: string) => {
    return email
      .split('@')
      .map(part => part.charAt(0).toUpperCase())
      .join('');
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-8 w-8 rounded-full">
          <Avatar className="h-8 w-8">
            <AvatarImage src={user.user_metadata?.avatar_url} alt={user.email || ''} />
            <AvatarFallback>{getInitials(user.email || '')}</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">
              {user.user_metadata?.full_name || user.email}
            </p>
            <p className="text-xs leading-none text-muted-foreground">
              {user.email}
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem>Profile</DropdownMenuItem>
        <DropdownMenuItem>Settings</DropdownMenuItem>
        <DropdownMenuItem>Billing</DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={onSignOut}>
          Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

### 3. Auth Callback Handler
```typescript
// src/app/auth/callback/route.ts
import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get('code');
  const next = searchParams.get('next') ?? '/';

  if (code) {
    const supabase = createServerClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    
    if (!error) {
      const forwardedHost = request.headers.get('x-forwarded-host');
      const isLocalEnv = process.env.NODE_ENV === 'development';
      
      if (isLocalEnv) {
        return NextResponse.redirect(`${origin}${next}`);
      } else if (forwardedHost) {
        return NextResponse.redirect(`https://${forwardedHost}${next}`);
      } else {
        return NextResponse.redirect(`${origin}${next}`);
      }
    }
  }

  return NextResponse.redirect(`${origin}/auth/auth-code-error`);
}
```

## Database Operations

### 1. Profile Management
```typescript
// src/lib/profiles.ts
import { createClient } from '@/lib/supabase/client';
import { Database } from '@/types/database';

type Profile = Database['public']['Tables']['profiles']['Row'];
type ProfileInsert = Database['public']['Tables']['profiles']['Insert'];
type ProfileUpdate = Database['public']['Tables']['profiles']['Update'];

export async function getProfile(userId: string): Promise<Profile | null> {
  const supabase = createClient();
  
  const { data, error } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', userId)
    .single();
  
  if (error) throw error;
  return data;
}

export async function updateProfile(
  userId: string,
  updates: ProfileUpdate
): Promise<Profile> {
  const supabase = createClient();
  
  const { data, error } = await supabase
    .from('profiles')
    .update(updates)
    .eq('id', userId)
    .select()
    .single();
  
  if (error) throw error;
  return data;
}

export async function uploadAvatar(
  userId: string,
  file: File
): Promise<string> {
  const supabase = createClient();
  
  const fileExt = file.name.split('.').pop();
  const fileName = `${userId}-${Date.now()}.${fileExt}`;
  const filePath = `avatars/${fileName}`;
  
  const { error: uploadError } = await supabase.storage
    .from('avatars')
    .upload(filePath, file);
  
  if (uploadError) throw uploadError;
  
  const { data: { publicUrl } } = supabase.storage
    .from('avatars')
    .getPublicUrl(filePath);
  
  // Update profile with new avatar URL
  await updateProfile(userId, { avatar_url: publicUrl });
  
  return publicUrl;
}
```

### 2. Post Management
```typescript
// src/lib/posts.ts
import { createClient } from '@/lib/supabase/client';
import { Database } from '@/types/database';

type Post = Database['public']['Tables']['posts']['Row'];
type PostInsert = Database['public']['Tables']['posts']['Insert'];
type PostUpdate = Database['public']['Tables']['posts']['Update'];

export async function getPosts(options?: {
  published?: boolean;
  limit?: number;
  offset?: number;
}): Promise<Post[]> {
  const supabase = createClient();
  
  let query = supabase
    .from('posts')
    .select(`
      *,
      profiles (
        username,
        full_name,
        avatar_url
      )
    `);
  
  if (options?.published !== undefined) {
    query = query.eq('published', options.published);
  }
  
  if (options?.limit) {
    query = query.limit(options.limit);
  }
  
  if (options?.offset) {
    query = query.offset(options.offset);
  }
  
  query = query.order('created_at', { ascending: false });
  
  const { data, error } = await query;
  
  if (error) throw error;
  return data;
}

export async function getPost(id: string): Promise<Post | null> {
  const supabase = createClient();
  
  const { data, error } = await supabase
    .from('posts')
    .select(`
      *,
      profiles (
        username,
        full_name,
        avatar_url
      )
    `)
    .eq('id', id)
    .single();
  
  if (error) throw error;
  return data;
}

export async function createPost(post: PostInsert): Promise<Post> {
  const supabase = createClient();
  
  const { data, error } = await supabase
    .from('posts')
    .insert(post)
    .select()
    .single();
  
  if (error) throw error;
  return data;
}

export async function updatePost(
  id: string,
  updates: PostUpdate
): Promise<Post> {
  const supabase = createClient();
  
  const { data, error } = await supabase
    .from('posts')
    .update(updates)
    .eq('id', id)
    .select()
    .single();
  
  if (error) throw error;
  return data;
}

export async function deletePost(id: string): Promise<void> {
  const supabase = createClient();
  
  const { error } = await supabase
    .from('posts')
    .delete()
    .eq('id', id);
  
  if (error) throw error;
}
```

## Real-time Subscriptions

### 1. Real-time Hooks
```typescript
// src/hooks/use-realtime.ts
'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { RealtimeChannel } from '@supabase/supabase-js';
import { Database } from '@/types/database';

type TableName = keyof Database['public']['Tables'];
type Row<T extends TableName> = Database['public']['Tables'][T]['Row'];

export function useRealtimeSubscription<T extends TableName>(
  table: T,
  filter?: (row: Row<T>) => boolean
) {
  const [data, setData] = useState<Row<T>[]>([]);
  const [loading, setLoading] = useState(true);
  const supabase = createClient();

  useEffect(() => {
    const fetchData = async () => {
      const { data, error } = await supabase
        .from(table)
        .select('*');
      
      if (error) {
        console.error('Error fetching data:', error);
        return;
      }
      
      const filteredData = filter ? data.filter(filter) : data;
      setData(filteredData);
      setLoading(false);
    };

    fetchData();

    const channel = supabase
      .channel(`realtime-${table}`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table,
        },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setData(prev => {
              const newData = [...prev, payload.new as Row<T>];
              return filter ? newData.filter(filter) : newData;
            });
          } else if (payload.eventType === 'UPDATE') {
            setData(prev => {
              const newData = prev.map(item =>
                item.id === payload.new.id ? payload.new as Row<T> : item
              );
              return filter ? newData.filter(filter) : newData;
            });
          } else if (payload.eventType === 'DELETE') {
            setData(prev => {
              const newData = prev.filter(item => item.id !== payload.old.id);
              return filter ? newData.filter(filter) : newData;
            });
          }
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [table, filter]);

  return { data, loading };
}

// Usage example
// src/components/posts/live-posts.tsx
'use client';

import { useRealtimeSubscription } from '@/hooks/use-realtime';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function LivePosts() {
  const { data: posts, loading } = useRealtimeSubscription('posts', (post) => post.published);

  if (loading) {
    return <div>Loading posts...</div>;
  }

  return (
    <div className="space-y-4">
      {posts.map((post) => (
        <Card key={post.id}>
          <CardHeader>
            <CardTitle>{post.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p>{post.content}</p>
            <small className="text-muted-foreground">
              {new Date(post.created_at).toLocaleString()}
            </small>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
```

## Row Level Security (RLS)

### 1. Database Policies
```sql
-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view their own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

CREATE POLICY "Users can insert their own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- Posts policies
CREATE POLICY "Anyone can view published posts"
  ON posts FOR SELECT
  USING (published = true);

CREATE POLICY "Users can view their own posts"
  ON posts FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own posts"
  ON posts FOR DELETE
  USING (auth.uid() = user_id);
```

### 2. Server-side Data Fetching
```typescript
// src/app/dashboard/page.tsx
import { createServerClient } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';
import { DashboardContent } from '@/components/dashboard/dashboard-content';

export default async function DashboardPage() {
  const supabase = createServerClient();
  
  // Check if user is authenticated
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) {
    redirect('/auth');
  }
  
  // Fetch user's posts (RLS will enforce permissions)
  const { data: posts } = await supabase
    .from('posts')
    .select('*')
    .eq('user_id', user.id);
  
  // Fetch user profile
  const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user.id)
    .single();
  
  return (
    <DashboardContent
      user={user}
      profile={profile}
      posts={posts || []}
    />
  );
}
```

## Storage & File Upload

### 1. File Upload Service
```typescript
// src/lib/storage.ts
import { createClient } from '@/lib/supabase/client';

export class StorageService {
  private supabase = createClient();

  async uploadFile(
    bucket: string,
    path: string,
    file: File,
    options?: {
      upsert?: boolean;
      cacheControl?: string;
    }
  ): Promise<{ data: { path: string } | null; error: any }> {
    return this.supabase.storage
      .from(bucket)
      .upload(path, file, {
        upsert: options?.upsert ?? false,
        cacheControl: options?.cacheControl,
      });
  }

  async getPublicUrl(
    bucket: string,
    path: string
  ): Promise<string> {
    const { data } = this.supabase.storage
      .from(bucket)
      .getPublicUrl(path);
    
    return data.publicUrl;
  }

  async deleteFile(
    bucket: string,
    paths: string[]
  ): Promise<{ error: any }> {
    return this.supabase.storage
      .from(bucket)
      .remove(paths);
  }

  async listFiles(
    bucket: string,
    path?: string,
    options?: {
      limit?: number;
      offset?: number;
      sortBy?: { column: string; order: 'asc' | 'desc' };
    }
  ): Promise<{ data: any[] | null; error: any }> {
    return this.supabase.storage
      .from(bucket)
      .list(path, options);
  }
}

// Usage example
// src/components/file-upload.tsx
'use client';

import { useState } from 'react';
import { StorageService } from '@/lib/storage';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Progress } from '@/components/ui/progress';

export function FileUpload() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [uploadedUrl, setUploadedUrl] = useState<string | null>(null);
  
  const storage = new StorageService();

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setProgress(0);

    try {
      const fileName = `${Date.now()}-${file.name}`;
      const { data, error } = await storage.uploadFile(
        'uploads',
        fileName,
        file,
        { upsert: true }
      );

      if (error) throw error;

      const publicUrl = await storage.getPublicUrl('uploads', fileName);
      setUploadedUrl(publicUrl);
      setProgress(100);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-4">
      <Input
        type="file"
        onChange={handleUpload}
        disabled={uploading}
      />
      
      {uploading && (
        <Progress value={progress} className="w-full" />
      )}
      
      {uploadedUrl && (
        <div className="space-y-2">
          <p>File uploaded successfully!</p>
          <img src={uploadedUrl} alt="Uploaded" className="max-w-xs rounded" />
        </div>
      )}
    </div>
  );
}
```

## Quick Start Setup

### 1. Environment Variables
```env
# .env.local
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

### 2. Installation Commands
```bash
# Install Supabase client libraries
npm install @supabase/supabase-js @supabase/auth-helpers-nextjs @supabase/auth-ui-react @supabase/auth-ui-shared

# Install additional dependencies
npm install @supabase/auth-helpers-react
npm install @types/react @types/react-dom
```

### 3. Database Setup SQL
```sql
-- Create profiles table
CREATE TABLE profiles (
  id uuid REFERENCES auth.users NOT NULL PRIMARY KEY,
  username text UNIQUE,
  full_name text,
  avatar_url text,
  website text,
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create posts table
CREATE TABLE posts (
  id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
  user_id uuid REFERENCES auth.users NOT NULL,
  title text NOT NULL,
  content text,
  published boolean DEFAULT false,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create storage bucket for avatars
INSERT INTO storage.buckets (id, name) VALUES ('avatars', 'avatars');

-- Set up storage policies
CREATE POLICY "Avatar images are publicly accessible" ON storage.objects
  FOR SELECT USING (bucket_id = 'avatars');

CREATE POLICY "Anyone can upload an avatar" ON storage.objects
  FOR INSERT WITH CHECK (bucket_id = 'avatars');

CREATE POLICY "Users can update their own avatar" ON storage.objects
  FOR UPDATE USING (auth.uid()::text = (storage.foldername(name))[1]);

-- Create function to handle new user profiles
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, avatar_url)
  VALUES (new.id, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url');
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger to call the function
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

## Best Practices

1. **Security**: Always enable RLS and create proper policies
2. **Performance**: Use database indexes and optimize queries
3. **Real-time**: Use subscriptions judiciously to avoid performance issues
4. **Error Handling**: Implement comprehensive error handling
5. **Type Safety**: Use TypeScript types generated from database schema

Remember: Supabase is powerful but requires proper security setup. Always validate data on the client and server, and use RLS to protect your data.