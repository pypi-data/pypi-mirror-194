#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   commands.py
@Author  :   Raighne.Weng
@Version :   0.7.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   CLI supported commands
'''

from argparse import ArgumentParser


# pylint: disable = R0903
class Commands:
    """ALl cli commands."""

    def __init__(self) -> None:

        self.parser = ArgumentParser(
            prog='datature',
            description=
            "Command line tool to create/upload/download datasets on datature nexus.",
        )

        subparsers = self.parser.add_subparsers(dest="command")

        # Project authenticate
        project = subparsers.add_parser("project", help="Project management.")
        project_action = project.add_subparsers(dest="action")

        project_action.add_parser('auth', help='Authenticate the project.')
        project_action.add_parser('select', help='Select the project.')
        project_action.add_parser('list', help='List the projects.')

        # Asset
        asset = subparsers.add_parser("asset", help="Asset management.")
        asset_action = asset.add_subparsers(dest="action")

        asset_upload = asset_action.add_parser('upload',
                                               help='Bulk update assets.')
        asset_upload.add_argument("path",
                                  nargs='*',
                                  help='The asset path to upload.')
        asset_upload.add_argument("cohorts",
                                  nargs='*',
                                  help='The asset groups to upload.')

        asset_group = asset_action.add_parser(
            'group', help='List assets group details.')
        asset_group.add_argument("cohort", nargs='*', help='The asset cohort.')

        # Annotation
        annotation = subparsers.add_parser("annotation",
                                           help="Annotation management.")
        annotation_action = annotation.add_subparsers(dest="action")

        annotation_upload = annotation_action.add_parser(
            'upload', help='Bulk upload annotations from file.')
        annotation_upload.add_argument("path",
                                       nargs='*',
                                       help='The annotations file path.')
        annotation_upload.add_argument(
            "format", nargs='*', help='The annotations format to upload.')

        annotation_download = annotation_action.add_parser(
            'download', help='Bulk download annotations to file.')

        annotation_download.add_argument("path",
                                         nargs='*',
                                         help='The annotations file path.')
        annotation_download.add_argument(
            "format", nargs='*', help='The annotations format to download.')

        # Artifact
        artifact = subparsers.add_parser("artifact",
                                         help="Artifact management.")

        artifact_action = artifact.add_subparsers(dest="action")
        artifact_download = artifact_action.add_parser(
            'download', help='Download artifact model.')
        artifact_download.add_argument("artifact_id",
                                       nargs='*',
                                       help='The id of the artifact.')
        artifact_download.add_argument("format",
                                       nargs='*',
                                       help='The artifact model formate.')

    def parse_args(self) -> ArgumentParser:
        """
        Parses and validates the CLI commands.

        :return: The parser to use.
        """
        return self.parser.parse_args()
