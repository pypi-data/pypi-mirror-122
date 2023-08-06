import tempfile


def update_binary(filepath, search_word, new_word) -> str:
    """
    Поиск текста и его замена в бинарном файле\n
    :param filepath: Путь к бинарному файлу
    :param search_word: Поиск текста
    :param new_word: Замена на новое значение
    :return: Путь к модифицированному бинарному файлу
    """
    with open(filepath, 'rb') as f:
        bytes_str = f.read()

    data = bytes_str.replace(search_word.encode(), new_word.encode())

    filepath = tempfile.mktemp()
    with open(filepath, 'wb') as f:
        f.write(data)
    return filepath