def replace_in_file(file_path: str, original: str, dist: str):
    content = ''
    
    with open(file_path, 'r') as f:
        content = f.read()

    content = content.replace(original, dist)

    with open(file_path, 'w') as f:
        f.write(content)
