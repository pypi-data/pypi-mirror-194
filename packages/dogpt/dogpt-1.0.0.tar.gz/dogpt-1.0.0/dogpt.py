"""
doGPT - AI for canine conversation.

(c) 2023 Nicholas H.Tollervey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import random, sys, time


#: MAJOR, MINOR, RELEASE, STATUS [alpha, beta, final], VERSION
_VERSION = (1, 0, 0)


#: TODO: i18n required.
_words = [
    "arf",
    "arf",
    "arf",
    "arf",
    "woof",
    "woof",
    "woof",
    "woof",
    "woof",
    "woof",
    "woof",
    "woof",
    "grrr",
    "CAT!",
    "walkies",
    "bone",
    "I'm a good dog",
    "play",
    "need scratch",
    "sniff",
    "dinner",
    "tummy rub",
    "fetch",
]


def get_version():
    """
    Returns a string representation of the version information of this project.
    """
    return ".".join([str(i) for i in _VERSION])


def text(prompt=""):
    """
    Advanced AI for piping dog conversation, subtly based upon user provided
    prompt, to STDOUT.
    """
    if prompt:
        max_response_len = len(prompt.split())
    else:
        max_response_len = 8
    for i in range(random.randint(1, max_response_len)):
        time.sleep(random.random() * 1.3)
        print(random.choice(_words), end=" ")
        sys.stdout.flush()
    print("")


def command():
    """
    Command line usage - grab prompt for argv.
    """
    prompt = " ".join(sys.argv[1:])
    text(prompt)


if __name__ == "__main__":
    command()
