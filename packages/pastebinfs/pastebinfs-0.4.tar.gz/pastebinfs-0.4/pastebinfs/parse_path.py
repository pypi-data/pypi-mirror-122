def parse_path(path: str) -> str:
    # strip the leading slash
    while path[0] == '/':
        path = path[1:]

    return path.strip()