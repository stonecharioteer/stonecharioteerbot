from stonecharioteerbot import serve
import argparse

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="StoneCharioteerBot CLI")
    arg_parser.add_argument("env", help="Path to the env file.")
    args = arg_parser.parse_args()
    env = args.env
    serve(env)
