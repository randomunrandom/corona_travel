#!/usr/bin/env python3
"""
# Task:
```
The KWIC index system accepts an ordered set of lines,
each line is an ordered set of words,
and each word is an ordered set of characters.
Any line may be "circularly shifted" by repeatedly removing the first word and
appending it at the end of the line.
The KWIC index system outputs a listing of all circular shifts of all lines
in alphabetical order.
```

Team: Everything is awesome
Members: Danil Kireev, Sofya Donskaya, Elena Karelina, Artem Filimonov
"""

import sys


def handle_input() -> list[list[str]]:
    raw_list_of_lines: list[str] = sys.stdin.readlines()
    list_of_words = [line.strip().split(" ") for line in raw_list_of_lines]
    return list_of_words


def shift(inp: list[list[str]]) -> list[list[str]]:
    res: list[list[str]] = []
    for splited_sentence in inp:
        res2: list[str] = []
        for _ in splited_sentence:
            res2.append(" ".join(splited_sentence))
            first_word = splited_sentence.pop(0)
            splited_sentence.append(first_word)
        res.append(res2)
    return res


def alphabetize(inp: list[list[str]]) -> list[str]:
    # big_list = [l2 for l1 in inp for l2 in l1]

    big_list: list[str] = []
    for sentence_group in inp:
        for sentence in sentence_group:
            big_list.append(sentence)

    sorted(big_list, key=str.lower)

    return big_list


def output(out: list[str]):
    print("\n".join(out))


if __name__ == "__main__":
    output(
        alphabetize(
            shift(
                handle_input()
            )
        )
    )

