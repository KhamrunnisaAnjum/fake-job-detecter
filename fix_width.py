with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()
n = c.count('use_container_width=True')
c = c.replace('use_container_width=True', 'width="stretch"')
c = c.replace('use_container_width=False', 'width="content"')
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(c)
print(f'Fixed {n} occurrences in app.py')

with open('auth.py', 'r', encoding='utf-8') as f:
    c = f.read()
n2 = c.count('use_container_width=True')
c = c.replace('use_container_width=True', 'width="stretch"')
c = c.replace('use_container_width=False', 'width="content"')
with open('auth.py', 'w', encoding='utf-8') as f:
    f.write(c)
print(f'Fixed {n2} occurrences in auth.py')
