import argparse
from bot import Bot


def main():
    parser = argparse.ArgumentParser(description="Automate TikTok and Instagram tasks using PyAutoGUI.")

    parser.add_argument("--urls", type=str, nargs="+", required=True, help="A list of URLs.")

    args = parser.parse_args()

    bot = Bot()
    bot.run(args.urls)


if __name__ == "__main__":
    main()
