from modules.wb_parse import get_wb_info


def main():
    article = input("Enter WB product article: ")
    print(get_wb_info(article))


if __name__ == "__main__":
    main()
