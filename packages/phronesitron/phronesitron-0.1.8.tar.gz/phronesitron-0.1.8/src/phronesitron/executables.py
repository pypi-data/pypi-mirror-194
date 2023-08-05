import argparse
import os
import sys
import openai
import os
import sys
import time
import textwrap as tr
import argparse
from termcolor import colored
import pyperclip as pc  # type: ignore
import re

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except KeyError:
    print("Please set the OPENAI_API_KEY environment variable.")
    print("You can get a key with some credits here:")
    print("\nhttps://platform.openai.com/account/api-keys")
    exit(-1)

def generate_response(prompt, args):
    model_engine = "text-" + args.engine
    context = args.context
    if args.context != "":
        prompt = "in the context of " + context + ": " + prompt
        print(colored("Context: " + context, "green"))

    if args.wordcount > 0:
        prompt = "{}. in {} words.".format(prompt, args.wordcount)

    prompt = f"{prompt}"

    success = False
    n = 0
    prompt_length = len(re.compile("[ \n\t]+").split(prompt))
    
    while not success:
        try:
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=args.money,
                n=1,
                stop=None,
                temperature=args.temp,
            )
            success = True
        except Exception as e:
            print("{}: {}\r".format(n, str(e)))
            time.sleep(n)
        n += 1
        if n > 10:
            exit(-1)
    sys.stdout.write("\r")
    sys.stdout.flush()

    actual_prompt = prompt

    info = colored(
        "tokens: {}, finish: {}, id: {}".format(
            completions.usage.total_tokens,
            completions.choices[0].finish_reason,
            completions.id,
        ),
        "blue",
    )
    davinciCost = 20 # in µ$
    print("Cost {}µ$".format(completions.usage.total_tokens*davinciCost)) 
    message = completions.choices[0].text

    return message.strip(), info, actual_prompt


def ph_args():
    parser = argparse.ArgumentParser(description="Chatbot.")
    parser.add_argument(
        "-e",
        "--engine",
        choices=["davinci-003", "curie-001", "babbage-001", "ada-001"],
        help="Engine to use",
        default="davinci-003",
    )
    parser.add_argument(
        "-c",
        "--context",
        type=str,
        help="Provide a context prefix. env:bot_context",
        default=os.getenv("bot_context", ""),
    )
    parser.add_argument(
        "-m", "--money", type=int, help="how many tokens for the request and the answer", default=100000
    )
    parser.add_argument(
        "-f",
        "--file",
        type=argparse.FileType("r"),
        help="file to append to string",
        default=None,
    )
    parser.add_argument(
        "-t",
        "--temp",
        type=float,
        help="0: deterministic, 2: I am very random",
        default=0.8,
    )
    parser.add_argument(
        "-i", "--iterations", type=int, help="Number of iterations to run", default=3
    )
    parser.add_argument(
        "-w", "--wordcount", type=int, help="Number of words in answer", default=0
    )
    parser.add_argument(
        "-u", "--unedited", action="store_true", help="Don't reformat text"
    )
    parser.add_argument(
        "-p",
        "--paste",
        action="store_true",
        help="Append what's in the paste buffer to the question provided",
    )
    parser.add_argument("question", nargs="+", default="")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


# https://github.com/daveshap/RecursiveSummarizer/blob/main/recursively_summarize.py


def ph_main():
    user_input = " ".join(args.question)

    if args.paste:  # Paste the copy buffer
        pb = pc.paste().split("\n")
        bracketCount = 0
        for char in pb[-1]:  # strip kindle refs
            if char in "()":
                bracketCount += 1
        if bracketCount > 3:
            pb[-1] = ""
            print("(Removed suspected kindle citation from pasted text)")
        user_input += " ".join(pb)

    if args.file:
        with args.file as f:
            user_input += " ".join(f.readlines())

    response, info, actual_prompt = generate_response(user_input)

    if not args.unedited:
        nice_response = ""
        for paragraph in response.split("\n"):
            nice_response += "\n".join(tr.wrap(paragraph, replace_whitespace=False))
            nice_response += "\n"
        nice_response = nice_response[:-1]
    else:
        nice_response = response

    with open(os.path.expanduser("~") + "/.botlog.txt", "a") as file:
        file.write("\n¡BOT! " + actual_prompt + "\n\n")
        file.write(nice_response)
        file.write("\n")
        file.write("[" + info + "]\n")
        file.write("\n" + "=" * 80 + "\n\n")

    print(colored(nice_response, "green"))



def ph_args():
    parser = argparse.ArgumentParser(description="Chatbot.")
    parser.add_argument(
        "-e",
        "--engine",
        choices=["davinci-003", "curie-001", "babbage-001", "ada-001"],
        help="Engine to use",
        default="davinci-003",
    )
    parser.add_argument(
        "-c",
        "--context",
        type=str,
        help="Provide a context prefix. env:bot_context",
        default=os.getenv("bot_context", ""),
    )
    parser.add_argument(
        "-m", "--money", type=int, help="how many tokens maximum for the answer", default=512
    )
    parser.add_argument(
        "-f",
        "--file",
        type=argparse.FileType("r"),
        help="file to append to string",
        default=None,
    )
    parser.add_argument(
        "-t",
        "--temp",
        type=float,
        help="0: deterministic, 2: I am very random",
        default=0.8,
    )
    parser.add_argument(
        "-i", "--iterations", type=int, help="Number of iterations to run", default=3
    )
    parser.add_argument(
        "-w", "--wordcount", type=int, help="Number of words in answer", default=0
    )
    parser.add_argument(
        "-u", "--unedited", action="store_true", help="Don't reformat text"
    )
    parser.add_argument(
        "-p",
        "--paste",
        action="store_true",
        help="Append what's in the paste buffer to the question provided",
    )
    parser.add_argument("question", nargs="+", default="")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


# https://github.com/daveshap/RecursiveSummarizer/blob/main/recursively_summarize.py


def ph_main():

    args = ph_args()

    user_input = " ".join(args.question)
    
    if args.paste:  # Paste the copy buffer
        pb = pc.paste().split("\n")
        bracketCount = 0
        for char in pb[-1]:  # strip kindle refs
            if char in "()":
                bracketCount += 1
        if bracketCount > 3:
            pb[-1] = ""
            print("(Removed suspected kindle citation from pasted text)")
        user_input += "\n".join(pb)

    if args.file:
        with args.file as f:
            user_input += "\n".join(f.readlines())

    response, info, actual_prompt = generate_response(user_input, args)

    if not args.unedited:
        nice_response = ""
        for paragraph in response.split("\n"):
            nice_response += "\n".join(tr.wrap(paragraph, replace_whitespace=False))
            nice_response += "\n"
        nice_response = nice_response[:-1]
    else:
        nice_response = response

    with open(os.path.expanduser("~") + "/.botlog.txt", "a") as file:
        file.write("\n¡BOT! " + actual_prompt + "\n\n")
        file.write(nice_response)
        file.write("\n")
        file.write("[" + info + "]\n")
        file.write("\n" + "=" * 80 + "\n\n")

    print(colored(nice_response, "green"))
