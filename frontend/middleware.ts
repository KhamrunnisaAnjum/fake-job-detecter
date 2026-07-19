import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const token = request.cookies.get('jobx_token')?.value;

    // Allow dummy token for now if present, but since we are replacing it, real tokens will be strings
    if (!token && !request.nextUrl.pathname.startsWith('/login')) {
        return NextResponse.redirect(new URL('/login', request.url));
    }
    
    // Redirect logged in users away from login
    if (token && request.nextUrl.pathname.startsWith('/login')) {
        return NextResponse.redirect(new URL('/dashboard', request.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: [
        '/dashboard/:path*',
        '/scan/:path*',
        '/history/:path*',
        '/reports/:path*',
        '/settings/:path*',
        '/messages/:path*',
        '/login'
    ]
};
