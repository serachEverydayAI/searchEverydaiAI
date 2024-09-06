def read_words(file_path: str) -> list:
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
    return words
