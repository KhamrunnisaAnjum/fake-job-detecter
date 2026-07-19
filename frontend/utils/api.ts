export async function apiFetch(url: string, options: RequestInit = {}) {
    let token = "";
    if (typeof document !== 'undefined') {
        const row = document.cookie.split('; ').find(r => r.startsWith('jobx_token='));
        if (row) token = row.split('=')[1];
    }
    
    const headers: Record<string, string> = {
        ...((options.headers as Record<string, string>) || {})
    };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const res = await fetch(url, { ...options, headers });
    if (res.status === 401 && typeof window !== 'undefined') {
        document.cookie = "jobx_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        window.location.href = "/login";
    }
    return res;
}
