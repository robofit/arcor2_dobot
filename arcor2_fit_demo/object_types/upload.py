#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from arcor2.object_types.upload import upload_def

from arcor2_fit_demo.object_types.dobot_magician import DobotMagician


def main() -> None:

    upload_def(DobotMagician)


if __name__ == "__main__":
    main()
