from pathlib import Path


SPECIAL_CHARACTERS = ["'", '"', "(", ",", ")", " ", "="]


def main():
    environment = read_settings(input("Provide your project's settings file from root dir: "))
    write_file(environment)


def write_file(environment):
    path = Path(__file__).resolve().parent.parent
    file = open(f"{path}/.env", "w")
    file.write(environment)


def read_settings(settings_file):
    environment = ""
    path = Path(__file__).resolve().parent.parent
    file = open(f"{path}/{settings_file}", "r")
    content = file.read()
    index = 0

    while index < len(content):
        current_word = get_word(index, content)
        if not current_word:
            break
        index += len(current_word)
        while content[index] in SPECIAL_CHARACTERS:
            index += 1
        if current_word not in ["config", "cast"]:
            continue
        parameter = get_word(index, content)
        if current_word == "config":
            environment += f"\n{parameter}" if len(environment) != 0 else f"{parameter}"
        else:
            if parameter == "Csv":
                parameter = "list"
            environment += f": {parameter}"
        while content[index] in SPECIAL_CHARACTERS:
            index += 1

    return environment


def get_word(current_character: int, content: str) -> str | None:
    word = ""
    if current_character == len(content) - 1:
        return None
    while current_character < len(content) - 1 and \
            content[current_character] not in SPECIAL_CHARACTERS:
        word += content[current_character]
        current_character += 1

    return word


main()
