import os

def get_english_data_PC(filename: str) -> str:
    open_file = open("PC scripts/" + filename, "r+", encoding="utf-8")
    data = open_file.read()
    open_file.close()
    return data

def ends_with_allowed_ends(data: str) -> bool:
    if data.endswith("　") or data.endswith("<") or data.endswith(".") or data.endswith("!") or data.endswith("?") or data.endswith(",") or data.endswith("\"") or data.endswith("*") or data.endswith("-") or data.endswith("_") or data.endswith("") or data.endswith("O") or data.endswith("↑") or data.endswith("s") or data.endswith("y") or data.endswith("t"):
        return True
    return False


def remove_unnecessary_ends(text: str) -> str:
    if text.endswith("　"):
        return text[0:-1]
    elif text.endswith("<"):
        return text[0:-1]
    else:
        return text

def extract_english_text(filename: str) -> tuple:
    data = get_english_data_PC(filename)
    data_split = list(filter(lambda x: not x.startswith("//"), data.split("\n")))  # filters out all lines that start with // (like things commented out)

    names = []
    texts = []

    for i in range(0, len(data_split) - 1):
        # For times when there's an empty thing and nothing else
        if data_split[i].split(">")[1] == "　" and len(data_split[i].split(">")[1]) == 1:
            continue

        # For times when there's a name that's followed by a sentence
        if data_split[i].split(">")[1].startswith("　"):
            # Checks if data ends with allowed signs. If it hits neither of those things, throw an exception
            if not ends_with_allowed_ends(data_split[i + 1].split(">")[1]):
                raise Exception(f"English data might not have a sentence after name in {filename} line {i}")
            name = data_split[i].split(">")[1]
            text = remove_unnecessary_ends(data_split[i + 1].split(">")[1])
            names.append(name)
            texts.append(text)

        # For times when there is no name and is followed by a sentence
        if data_split[i].endswith(",0>"):
            if not ends_with_allowed_ends(data_split[i + 1].split(">")[1]):
                raise Exception(f"English data might not have a sentence after name in {filename} line {i}\nAt line '{data_split[i + 1]}'")
            text = remove_unnecessary_ends(data_split[i + 1].split(">")[1])
            texts.append(text)

    # print(f"Names list length: {len(names)}")
    # print(f"Texts list length: {len(texts)}")
    # print(names)
    # print(texts)

    # Clear out unnecessary symbols
    for i in range(0, len(texts)):
        if "" in texts[i]:
            texts[i] = texts[i].replace("", "♪")
        if "_" in texts[i]:
            texts[i] = texts[i].replace("_", "...")
        if "↑" in texts[i]:
            texts[i] = texts[i].replace("↑", "")

    return names, texts


if __name__ == '__main__':
    for filename in os.listdir("PC scripts"):
        # if filename == "prologue01.txt":
           extract_english_text(filename)