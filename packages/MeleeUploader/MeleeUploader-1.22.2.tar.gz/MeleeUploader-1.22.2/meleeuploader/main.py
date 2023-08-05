#!/usr/bin/env python3

import os
import sys

from . import forms
from . import consts
from . import youtube as yt

import pyforms_lite


def main():
    try:
        if os.path.isfile(consts.youtube_oauth_file) or not len(
            os.listdir(consts.yt_accounts_folder)
        ):
            consts.youtube = yt.get_youtube_service()
        elif len(os.listdir(consts.yt_accounts_folder)):
            pyforms_lite.start_app(forms.YouTubeSelector, geometry=(200, 200, 330, 100))
            consts.youtube = yt.get_youtube_service()
    except Exception as e:
        print(e)
        print("There was an issue with getting Google Credentials")
        sys.exit(1)
    try:
        pyforms_lite.start_app(forms.MeleeUploader, geometry=(200, 200, 1, 1))
    except Exception as e:
        print("Error:", e)
        sys.exit(1)


def s64():
    consts.game = "64"
    main()


def melee():
    main()


def ult():
    consts.game = "ult"
    main()


def rivals():
    consts.game = "rivals"
    main()


def splatoon():
    consts.game = "splatoon"
    main()


if __name__ == "__main__":
    main()
