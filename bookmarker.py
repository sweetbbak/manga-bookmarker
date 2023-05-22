#!/bin/env python3

import argparse
from rich import print
from urllib.parse import urlparse
import json
import datetime
from natsort import natsorted
import re
import sys
import os
from time import sleep
from browser_history.browsers import Firefox


def get_history():
    f = Firefox()
    outputs = f.fetch_history()
    # his is a list of (datetime.datetime, url) tuples
    history = outputs.histories
    return list(history)


def choose(options: list, limit: bool = True):
    oxot = []
    for option in options:
        oxot.append(f'"{option}"')
    options = " ".join(oxot)
    if not limit:
        # result = os.popen(f"gum choose --no-limit {options}")
        f"printf '%s\n' {options} | fzf --reverse -m --cycle"
    else:
        result = os.popen(
            # f"printf '%s\n' {options} | gum filter --fuzzy --match.italic --selected-indicator.foreground=212 --selected-indicator.bold"
            f"printf '%s\n' {options} | fzf --reverse -m --cycle"
        )
    if not limit:
        return result.read().replace(r"\n", "\n").strip().split("\n")
    else:
        return result.read().replace(r"\n", "\n").strip()


def chooser(options: list, limit: bool = True):
    oxot = []
    for option in options:
        oxot.append(f'"{option}"')
    options = " ".join(oxot)
    if not limit:
        result = os.popen(f"gum choose --no-limit {options}")
    else:
        result = os.popen(f"gum choose {options}")
    if not limit:
        return result.read().replace(r"\n", "\n").strip().split("\n")
    else:
        return result.read().replace(r"\n", "\n").strip()


def add_url():
    pass


def rm_url():
    pass


def _open_link(url):
    os.system(f"firefox {url}")


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--list", help="list all bookmarks", action="store_true")
    ap.add_argument("-b", "--browser", help="dump browser history", action="store_true")
    ap.add_argument(
        "-n", "--nsfw", help="dump browser history nsfw", action="store_true"
    )
    ap.add_argument("-u", "--update", help="parse browser history", action="store_true")
    ap.add_argument("-a", "--add", help="add a bookmark", default=None, nargs="?")
    ap.add_argument("-r", "--remove", help="remove a bookmark", default=None, nargs="?")
    # ap.add_argument(
    #     "command",
    #     help="command to run",
    #     choices=["add", "rm", "update"],
    #     default=None,
    #     nargs="?",
    # )
    args = ap.parse_args()
    return args


def base_url():
    pass


def chapter_urls():
    pass


def list_bookmarks():
    pass


def remove_dupes2(it):
    """remove duplicates in array"""
    # not working I guess
    seen = []
    for x in it:
        if x not in seen:
            # yield x
            seen.append(x)
    return seen


def remove_dupes(x):
    return list(dict.fromkeys(x))


def to_json(body, title) -> None:
    """Write a list or object to json"""

    with open(title, "w") as f:
        json.dump(body, f)


def parse_browser(domains: list) -> list:
    """Dump browser history and retrun list of matching domains"""

    history = get_history()
    output = []
    urls = []
    for u in list(history):
        urls.append(u[-1])

    for x in urls:
        netloc = urlparse(x).netloc
        for net in domains:
            if net in netloc:
                output.append(x)

    return output


# find_number('abce123de34', 'e') >> ['123', '34']
# find_number('abce123de34', 'de') >> ['34']
def get_chapter_num(text, c) -> None:
    return re.findall(r"%s(\d+)" % c, text)


def parse_list(url_list: list) -> list:
    new_list = []
    for item in url_list:
        if item.endswith("jpg") or item.endswith("png") or item.endswith("webp"):
            pass
    return new_list


def rm_bad_links(url_list: list) -> list:
    """Remove links that are associated with non-chapter and non-base urls"""

    url_list = remove_dupes2(url_list)
    url_list = list(set(url_list))

    bad_items = [
        "jpg",
        "webp",
        "png",
        "/?s=",
        "bookmark",
        "#comment",
        "/#/next/",
        "/#comment-",
        "#div-comment-",
        "/wp-content/",
        "/wp-content/uploads",
        "https:ww5.manganelo.tv",
        "https://status.reaperscans.com/",
        "https:www.webtoons.com/en/genre",
        "https://1stkissmanga.me/user-settings/?tab=bookmark",
        "https://user.manganelo.com/login?l=mangakakalot&re_l=login",
        "https://1stkissmanga.me/user-settings/?tab=account-settings",
    ]

    new_list = []
    for item in url_list:
        for bad_item in bad_items:
            # if item.endswith("jpg") or item.endswith("png") or item.endswith("webp"):
            if bad_item in item or bad_item == item:
                print(bad_item + " -> " + item)
                print("MATCHED BAD LINK LOL")
                # sleep(1)
                pass
            elif item not in bad_item and item not in new_list:
                # print(item + " APPENDED TO GOOD LIST :3")
                new_list.append(item)

    print(new_list)
    return new_list


def writeout(res):
    """Write to Stdout"""
    for x in res:
        # sys.stdout.write(x + "\n")
        sys.stdout.write(x)


def sort_json(data):
    # set removes duplicate entries
    res = [*set(data)]
    # natural sort for logical order
    res = natsorted(res)
    return res


def sort_domains(res):
    # just doing this for asura rn
    manga = []
    chapters = []
    for x in res:
        y = urlparse(x)
        if "/manga/" in y.path:
            manga.append(x)
        if "-chapter-" in y.path:
            chapters.append(x)

    return manga, chapters


def list_recent():
    f = open("history.json", "r")
    data = json.load(f)
    sorted_json = sort_json(data)
    # manga, chapters = sort_domains(sorted_json)
    # return manga, chapters
    return sorted_json


def main():
    args = get_arguments()
    # print(args)
    if args.add:
        print(args.add)
        print(urlparse(args.add))
        # xa = urlparse(args.add)
    if args.list:
        print("List this list")
    if args.remove:
        print("List rm this")
    if args.browser:
        # dump browser history for just the listed domains
        # add a config file for accepted websites
        domains = [
            "asurascans",
            "reaperscans",
            "1stkissmanga",
            "webtoons",
            "flamescans",
            "manganelo",
            "manganato",
            "manganato.com",
            "chapmanganato",
            "chapmanganelo",
            "comick",
            "comick.app",
        ]
        urls = parse_browser(domains)
        urls = sort_json(urls)
        to_json(urls, "history.json")
        # choose(urls)
    if args.update:
        # sort recently read manhwa from chapters
        manga = list_recent()
        manga = rm_bad_links(manga)
        # choice = choose(manga)
        # writeout(choice)
        # to_json(manga, "recent.json")
        # _open_link(choice)


main()
