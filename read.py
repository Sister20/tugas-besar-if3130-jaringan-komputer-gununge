
file_path = "input.txt"

with open(file_path, "r") as file:
    content = file.read()
    word_count = len(content.split())
    print("Number of words:", word_count)
