import glob
import re

files_to_update = glob.glob("app/**/*.tsx", recursive=True)

for file_path in files_to_update:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if 'import { apiFetch } from "@/utils/api";\n"use client";\n' in content:
        content = content.replace(
            'import { apiFetch } from "@/utils/api";\n"use client";\n',
            '"use client";\nimport { apiFetch } from "@/utils/api";\n'
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
    # Also check if it's there but maybe with carriage returns
    elif 'import { apiFetch } from "@/utils/api";' in content and '"use client";' in content:
        # We can just remove the import, and re-add it under use client
        lines = content.split('\n')
        if lines[0].startswith('import { apiFetch }') and '"use client"' in lines[1]:
            lines[0], lines[1] = lines[1], lines[0]
            with open(file_path, "w", encoding="utf-8") as f:
                f.write('\n'.join(lines))

print("Fixed use client positions")
