import os
import glob
import re

API_UTIL = """export async function apiFetch(url: string, options: RequestInit = {}) {
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

    return fetch(url, { ...options, headers });
}
"""

os.makedirs("utils", exist_ok=True)
with open("utils/api.ts", "w") as f:
    f.write(API_UTIL)

files_to_update = glob.glob("app/**/*.tsx", recursive=True)

for file_path in files_to_update:
    if "login" in file_path or "layout" in file_path:
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "fetch(" in content and "http://127.0.0.1:8000" in content:
        # Add import
        if "import { apiFetch } from" not in content:
            # find first import
            content = 'import { apiFetch } from "@/utils/api";\n' + content
            
        # Replace fetch( with apiFetch(
        content = re.sub(r'\bfetch\(', 'apiFetch(', content)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

print("Done")
