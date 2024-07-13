import argparse
from indeed_apply_bot import Indeed_Apply_Bot


def main():
    parser = argparse.ArgumentParser(description="Automate TikTok and Instagram tasks using PyAutoGUI.")

    parser.add_argument("--jobs", type=int, required=True, help="number of jobs to apply to")

    args = parser.parse_args()

    bot = Indeed_Apply_Bot(args.jobs)
    bot.run()


if __name__ == "__main__":
    main()
