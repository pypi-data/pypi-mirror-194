#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   main.py
@Author  :   Raighne.Weng
@Version :   0.7.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   CLI main entrance
'''

import sys
import datature
from datature import messages
from datature.cli.commands import Commands
from datature.cli import functions
from datature.cli.config import Config
from datature.error import ForbiddenError, ErrorWithCode


# pylint: disable=R0912
def main() -> None:
    """
    Executes the main function of cli.

    """
    args = Commands().parse_args()
    try:
        # project secret management
        if args.command == "project":
            if args.action == "auth":
                functions.authenticate()
            elif args.action == "select":
                functions.select_project()
            elif args.action == "list":
                functions.list_projects()

        else:
            # Get default project
            config = Config()
            project = config.get_default_project()
            if not project:
                print(messages.NO_PROJECT_MESSAGE)
                sys.exit(1)

            # Set project secret
            datature.project_secret = project.get("project_secret")

            if args.command == "asset":
                if args.action == "upload":
                    functions.upload_assets(args.path, args.cohorts)
                if args.action == "group":
                    functions.assets_group(args.cohort)

            elif args.command == "annotation":
                if args.action == "upload":
                    functions.upload_annotations(args.path, args.format)
                if args.action == "download":
                    functions.download_annotations(args.path, args.format)

            elif args.command == "artifact":
                if args.action == "download":
                    functions.download_artifact(args.artifact_id, args.format)
    except KeyboardInterrupt:
        sys.exit(0)
    except ForbiddenError:
        print(messages.AUTHENTICATION_FAILED_MESSAGE)
        sys.exit(1)
    except ErrorWithCode:
        print(messages.UNKNOWN_ERROR_SUPPORT_MESSAGE)
        sys.exit(1)
