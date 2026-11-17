import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="director cu table-joc/ si table-scor/")
    parser.add_argument("--output", required=True, help="director unde se scriu fisierele .txt")
    args = parser.parse_args()
    pass


if __name__ == "__main__":
    main()
