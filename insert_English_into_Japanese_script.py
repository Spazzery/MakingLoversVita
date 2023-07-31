import os
import re
from extract_english_text_making_lovers import extract_english_text
from extract_english_text_making_lovers import get_english_data_PC


def write_to_file(filename, data_list):
    dir = os.path.join("Translated")
    if not os.path.exists(dir):
        os.mkdir(dir)

    save_path = "Translated/"
    complete_name = os.path.join(save_path, filename)
    create_file = open(complete_name, "w", encoding="shift-jis")

    for i in data_list:
        # print(i)
        create_file.write(i)
        if data_list.index(i) != len(data_list) - 1:
            create_file.write("\n")
    create_file.close()


def get_data_from_file(vita_input):
    open_file = open("Vita/" + vita_input, "r+", encoding="shift-jis")
    data = open_file.read()
    open_file.close()
    return data


def get_english_data(filename):
    return extract_english_text(filename)

# DEPRACATED
def add_linebreaks_and_modify_text_size(line: str) -> list:
    """Based on the information in file 'font size text lengths.txt'."""
    result = []
    text_string = line[6:-1]  # removes "<text " part
    text_string_replaced_characters = re.sub("\"(.*?)\"", "“\\1”", text_string)  # quick hackfix. Replace all instances of in game quotation marks. cant do it later.
    text_string_splitted = text_string_replaced_characters.split(" ")
    resulting_lines = []
    current_line = ""
    resulting_font_size = 0

    value_pairs = [(35, 26), (37, 25), (38, 24), (42, 23), (43, 22), (44, 21), (47, 20), (50, 19), (53, 18),
                   (56, 17), (60, 16), (64, 15), (69, 14), (73, 13),
                   (79, 12)]  # Based on the information in file 'font size text lengths.txt'.

    for value_pair in value_pairs:

        text_line_limit = value_pair[0]
        # Splits the sentence into 36 (or other number) characters and puts it in resulting_lines
        for i in range(0, len(text_string_splitted)):
            if i == len(text_string_splitted) - 1:  # if i is last element's index
                if len(current_line) + len(text_string_splitted[i]) <= text_line_limit:
                    current_line += text_string_splitted[i]
                    resulting_lines.append(current_line)
                else:
                    resulting_lines.append(current_line)
                    current_line = text_string_splitted[i]
                    resulting_lines.append(current_line)
            elif len(current_line) + len(text_string_splitted[i]) == text_line_limit:
                current_line += text_string_splitted[i]
            elif len(current_line) + len(text_string_splitted[i]) + 1 <= text_line_limit:
                current_line += text_string_splitted[i] + " "
            else:
                current_line = current_line.rstrip()
                resulting_lines.append(current_line)
                current_line = ""
                current_line += text_string_splitted[i] + " "

        # Check the lines we made. If there are 4 or more resulting lines, we need to make text smaller. If 3 lines or less, we good.
        # if len(resulting_lines) > 3 and text_line_limit == value_pairs[-1][0]:
        #     # print(resulting_lines)
        #     raise Exception(f"we need to go smaller than text size {value_pairs[-1][1]}")
        if len(resulting_lines) > 3 and text_line_limit >= 47:
            resulting_font_size = value_pair[1]
            break
        elif len(resulting_lines) > 3:
            resulting_lines = []
            current_line = ""
            continue
        else:
            resulting_font_size = value_pair[1]
            break

    resulting_lines = list(map(lambda x: x.rstrip(), resulting_lines))  # just removes spaces from sentence ends?
    resulting_text_line = "<text " + "\\n".join(resulting_lines) + ">"

    result.append(resulting_text_line)

    # if resulting_font_size != 26:
    result.insert(0, f"<font size:{resulting_font_size}>")
    result.append("<font>")


        # PROBABLY OLD STUFF FOR OLD ALGORITHM. GONNA COMMENT IT OUT.
        # # Remove all spaces from the right for each line and split them into chunks of 3
        # resulting_lines = list(map(lambda x: x.rstrip(), resulting_lines))
        # resulting_lines = [resulting_lines[i:i + 3] for i in range(0, len(resulting_lines), 3)]  # some code I stole. generates size 3 chunks
        #
        # # if len(resulting_lines) == 3:
        # #     print(f"3 textboxes in this file")
        #
        # # Utilize 3-sized chunks to create result
        # for index, chunk in enumerate(resulting_lines):
        #     result.append("<text " + "\\n".join(chunk) + ">")
        #     if index < len(resulting_lines) - 1:
        #         result.append(keywait)
        #         if name is not None:
        #             result.append(name)

    return result

def add_linebreaks(line: str, keywait: str, name: str) -> list:
    TEXT_LINE_LIMIT = 35
    result = []
    text_string = line[6:-1]  # removes "<text " and ">" part

    # Do replacements that cant be done later
    text_string_replaced_characters = re.sub("\"(.*?)\"", "“\\1”", text_string)  # quick hackfix. Replace all instances of in game quotation marks. cant do it later.
    if "Protag(firstname)" in text_string_replaced_characters:
        text_string_replaced_characters = text_string_replaced_characters.replace("Protag(firstname)", "Kazuma")
    if "Protag(lastname)" in text_string_replaced_characters:
        text_string_replaced_characters = text_string_replaced_characters.replace("Protag(lastname)", "Takanashi")

    text_string_splitted = text_string_replaced_characters.split(" ")
    resulting_lines = []
    current_line = ""

    # Splits the sentence into 36 (or other number) characters and puts it in resulting_lines
    for i in range(0, len(text_string_splitted)):
        if i == len(text_string_splitted) - 1:  # if i is last element's index
            if len(current_line) + len(text_string_splitted[i]) <= TEXT_LINE_LIMIT:
                current_line += text_string_splitted[i]
                resulting_lines.append(current_line)
            else:
                resulting_lines.append(current_line)
                current_line = text_string_splitted[i]
                resulting_lines.append(current_line)
        elif len(current_line) + len(text_string_splitted[i]) == TEXT_LINE_LIMIT:
            current_line += text_string_splitted[i]
        elif len(current_line) + len(text_string_splitted[i]) + 1 <= TEXT_LINE_LIMIT:
            current_line += text_string_splitted[i] + " "
        else:
            current_line = current_line.rstrip()
            resulting_lines.append(current_line)
            current_line = ""
            current_line += text_string_splitted[i] + " "

    resulting_lines = list(map(lambda x: x.rstrip(), resulting_lines)) # Remove all spaces from the right for each line

    # Create chunks of 3 (lists inside a list)
    resulting_lines = [resulting_lines[i:i + 3] for i in range(0, len(resulting_lines), 3)]  # some code I stole. generates size 3 chunks

    # Utilize 3-sized chunks to create result
    for index, chunk in enumerate(resulting_lines):
        result.append("<text " + "\\n".join(chunk) + ">")
        if index < len(resulting_lines) - 1:  # if there's more than 1 chunk, add name and keywait
            result.append(keywait)
            if name is not None:
                result.append(name)

    return result

def get_keywait(remaining_list: list):
    for i in range(0, len(remaining_list)):
        if remaining_list[i].startswith("<keywait"):
            return remaining_list[i]


def insert_english_text(filename):
    data = get_data_from_file(filename)
    data_split = list(filter(lambda x: not x.startswith("//"), data.split("\n"))) # filters out all lines that start with // (like things commented out)
    english_names = get_english_data(filename)[0]
    # print(english_names)
    print(len(english_names))
    english_texts = get_english_data(filename)[1]
    print("PC: " + str(len(english_texts)))

    translated_data_split = data_split

    # Firstly, replace names
    for i in range(0, len(data_split)):
        if data_split[i].startswith("<name"):
            # print(data_split[i] + " " + str(i))
            # print(english_names[0])
            # print("---------")
            name = english_names.pop(0)[1:] # removes English version's big space
            name = name.replace(" ", "_")
            if data_split[i] == "<name 主人公（名）>":
                name = "Kazuma"
                # name = "主人公（名）"
            if "Protag(firstname)" in name:
                name = name.replace("Protag(firstname)", "Kazuma")
            translated_data_split[i] = "<name " + name + ">"

    vita_texts_test = []
    count = 0
    # Then, replace text sentences
    for i in range(0, len(data_split)):
        if data_split[i].startswith("<text"):
            vita_texts_test.append(data_split[i]) # used only for testing
            count += 1
            english_text = english_texts.pop(0)

            # Add Japanese quotation marks to sentence BEGINNINGS AND ENDS, but not in the middle of sentence, this is done later
            if data_split[i].startswith("<text 「") and data_split[i].endswith("」>"):
                translated_data_split[i] = "<text " + "「" + english_text + "」" + ">"
            elif data_split[i].startswith("<text 『") and data_split[i].endswith("』>") and english_text.startswith("\"") and english_text.endswith("\""):
                translated_data_split[i] = "<text " + "『" + english_text[1:-1] + "』" + ">"
            elif data_split[i].startswith("<text 『") and data_split[i].endswith("』>"):
                translated_data_split[i] = "<text " + "『" + english_text + "』" + ">"
            else:
                translated_data_split[i] = "<text " + english_text + ">"

    # print("PC: " + str(len(english_texts)))
    print("vita: " + str(count))
    print(len(english_names))
    # print(english_texts)

    # Put linebreaks after every 36 characters
    translated_data_split_with_linebreaks = []
    for i in range(0, len(translated_data_split)):

        if translated_data_split[i].startswith("<text"):
            if translated_data_split[i - 1].startswith("<name"):
                name = translated_data_split[i - 1]
            else:
                name = None
            keywait = get_keywait(translated_data_split[i:])
            text_with_linebreaks = add_linebreaks(translated_data_split[i], keywait, name)
            for new_line in text_with_linebreaks:
                translated_data_split_with_linebreaks.append(new_line)

        else:
            translated_data_split_with_linebreaks.append(translated_data_split[i])

    # Substitute all quotation marks for Japanese quotation marks and other stuff
    for i in range(0, len(translated_data_split_with_linebreaks)):
        if translated_data_split_with_linebreaks[i].startswith("<text"):
            translated_data_split_with_linebreaks[i] = translated_data_split_with_linebreaks[i].replace(", ", "，")
            # translated_data_split_with_linebreaks[i] = translated_data_split_with_linebreaks[i].replace("-", "―")
            translated_data_split_with_linebreaks[i] = re.sub("\"(.*?)\"", "『\\1』", translated_data_split_with_linebreaks[i])
        if translated_data_split_with_linebreaks[i] == "<font size:22>" \
                or translated_data_split_with_linebreaks[i] == "<font size:24>" \
                or translated_data_split_with_linebreaks[i] == "<font size:28>" \
                or translated_data_split_with_linebreaks[i] == "<font size:30>" \
                or translated_data_split_with_linebreaks[i] == "<font size:32>" \
                or translated_data_split_with_linebreaks[i] == "<font size:34>" \
                or translated_data_split_with_linebreaks[i] == "<font size:35>" \
                or translated_data_split_with_linebreaks[i] == "<font size:36>" \
                or translated_data_split_with_linebreaks[i] == "<font size:40>" \
                or translated_data_split_with_linebreaks[i] == "<font size:45>" \
                or translated_data_split_with_linebreaks[i] == "<font size:50>":
            translated_data_split_with_linebreaks[i] = "<font>"

    # print(translated_data_split_with_linebreaks)
    # write_to_file(filename[:-4] + "_lines_PC" + ".txt", english_texts)
    # write_to_file(filename[:-4] + "_lines_Vita" + ".txt", vita_texts_test)
    # print(len(english_texts) - count)
    write_to_file(filename, translated_data_split_with_linebreaks)
    print(f"{filename} translated successfully!\n")


if __name__ == '__main__':
    for file in os.listdir("Vita"):
        # if file == "prologue03_S.txt":
        if file.endswith(".txt") and file.startswith("ako"):
            insert_english_text(file)
        if file == "prologue01.txt":
            insert_english_text(file)
        if file == "prologue02.txt":
            insert_english_text(file)
        if file == "prologue03.txt":
            insert_english_text(file)
        if file == "prologue03_M.txt":
            insert_english_text(file)
        if file == "prologue03_S.txt":
            insert_english_text(file)
        # if file == "ako_a04.txt":
        #     insert_english_text(file)
        # if file == "ako_a05.txt":
        #     insert_english_text(file)
        # if file == "ako_b01.txt":
        #     insert_english_text(file)
        # if file == "ako_b02.txt":
        #     insert_english_text(file)
        # if file == "ako_b04.txt":
        #     insert_english_text(file)
        # if file == "ako_b05.txt":
        #     insert_english_text(file)
        # if file == "ako_b06.txt":
        #     insert_english_text(file)
        # if file == "ako_b07.txt":
        #     insert_english_text(file)
        # if file == "ako_b08.txt":
        #     insert_english_text(file)
        # if file == "ako_b09.txt":
        #     insert_english_text(file)

    # insert_english_text("prologue01.txt")



















    #######
    # for i
    # eng_data = get_english_data_PC(filename)
    # eng_data_split = eng_data.split("\n")
    #
    # for i in range(0, len(eng_data_split)):
    #     if len(english_texts) == 0:
    #         break
    #     if english_texts[0] in eng_data_split[i]:
    #         english_texts.pop(0)
    #         eng_data_split[i] = "------------------REMOVED SENTENCE--------------------"
    #     if "wait" in eng_data_split[i]:
    #         eng_data_split[i] = "------------------REMOVED COMMAND--------------------"
    #     if "bustshot" in eng_data_split[i]:
    #         eng_data_split[i] = "------------------REMOVED COMMAND--------------------"
    #     if "se0" in eng_data_split[i]:
    #         eng_data_split[i] = "------------------REMOVED COMMAND--------------------"
    #     if "_" in eng_data_split[i]:
    #         eng_data_split[i] = "------------------REMOVED COMMAND--------------------"
    #     if "KK01" in eng_data_split[i]:
    #         eng_data_split[i] = "------------------REMOVED COMMAND--------------------"
    #
    # for i in eng_data_split:
    #     print(i)

    # else:
    #     current_line_long += current_line + "\\n"
    #     current_line = ""
    # if len(current_line_long + i) > 112:
    #     result.append("<text " + current_line_long + ">")
    #     result.append(keywait)
    #     if name is not None:
    #         result.append(name)
    #     current_line_long = ""
    #
    # if len(current_line) < 36:
    #     if len(current_line) + len(i) + 1 < 36:
    #         current_line += i + " "
    #     if len(current_line) + len(i) == 36:
    #         current_line += i
    #     else:

    # else:
    #     current_line_long += current_line + "\\n"
    #     current_line = ""

    # if line_2 == "":
    #     result.append("<text " + line_1 + ">")
    # elif line_3 == "":
    #     result.append("<text " + line_1 + "\\n" + line_2 + ">")
    # else:
    #     result.append("<text " + line_1 + "\\n" + line_2 + "\\n" + line_3 + ">")

    #     if len(current_line) + len(i) >= 109:
    #         result.append("<text " + current_line[:-1] + ">")
    #         current_line = ""
    #         current_line += i + " "
    #         result.append(keywait)
    #         if name is not None:
    #             result.append(name)
    #
    #     elif len(current_line) + len(i) > 72:
    #         if current_line.count("\\n") == 2:
    #             current_line += i + " "
    #         else:
    #             current_line += "\\n" + i + " "
    #     elif len(current_line) + len(i) + 1 > 35:
    #         if current_line.count("\\n") == 1:
    #             current_line += i + " "
    #         else:
    #             current_line += "\\n" + i + " "
    #     else:
    #         current_line += i + " "
    #
    # result.append("<text " + current_line[:-1] + ">")

    # Removing spaces from before \n-s
    # for i in range(0, len(result)):
    #     if result[i].startswith("<text"):
    #         result[i] = re.sub("\s\\\\\n", "\\n", result[i])

    # else:
    #     line_count = 0
    #     result_line = ""
    #     for i in range(0, len(resulting_lines)):
    #         if line_count == 3:
    #             result.append("<text " + result_line + ">")
    #             result.append(keywait)
    #             if name is not None:
    #                 result.append(name)
    #             result_line = ""
    #             line_count = 0
    #         elif i == len(resulting_lines) - 1:
    #             result_line += resulting_lines[i].rstrip()
    #             result.append("<text " + result_line + ">")
    #         else:
    #             result_line += resulting_lines[i].rstrip()
    #             if line_count != 2:
    #                 result_line += "\\n"
    #             line_count += 1