#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   functions.py
@Author  :   Raighne.Weng
@Version :   0.7.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   CLI functions
'''

from typing import Optional
from pathlib import Path
from os.path import exists, isfile, basename, join
import os
import time
import sys
import getpass
import inquirer
from tqdm import tqdm
from halo import Halo
import requests
import datature
from datature import error
from datature import messages
from datature.cli.config import Config
from datature.rest.types import (AnnotationFormat)

ASSET_UPLOAD_BATCH_SIZE = datature.ASSET_UPLOAD_BATCH_SIZE

datature.SHOW_PROGRESS = True

if 'DATATURE_API_BASE_URL' in os.environ:
    datature.API_BASE_URL = os.environ['DATATURE_API_BASE_URL']


def authenticate():
    """
    Authenticate the Project Secret with the server and creates a configuration file for it.

    :param project_secret: Secret key to use for the client login.
    :return: None
    """
    project_secret = getpass.getpass(prompt="Project Secret: ", stream=None)
    project_secret = project_secret.strip()
    if project_secret == "":
        print(messages.AUTHENTICATION_REMINDER_MESSAGE)
        sys.exit(1)

    try:
        datature.project_secret = project_secret
        project = datature.Project.retrieve()

        project_name = project.get("name")
        project_id = project.get("id")

        questions = [
            inquirer.Text(
                "default",
                message=f"Make [{project_name}] the default project? [Y/n]",
            ),
        ]

        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        default_project = answer.get("default") not in ["n", "N"]

        config = Config()
        config.set_project(project_id, project_name, project_secret,
                           default_project)

    except error.ForbiddenError:
        print(messages.INVALID_PROJECT_SECRET_MESSAGE)
        sys.exit(1)
    print(messages.AUTHENTICATION_MESSAGE)


def select_project():
    """
    Select project from saved configuration file.

    :return: None
    """
    config = Config()
    project_names = config.get_all_project_names()

    questions = [
        inquirer.List(
            "project_name",
            message="Which project do you want to select?",
            choices=project_names,
        ),
    ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    project = config.get_project_by_name(answers.get("project_name"))

    config.set_default_project(project.get("project_id"))


def list_projects():
    """
    List projects from saved configuration file.

    :return: None
    """
    config = Config()
    project_names = config.get_all_project_names()
    default_project = config.get_default_project()

    output = ""
    for project_name in project_names:
        output += str(project_name) + "\n"

    print((f"{output}\n"
           f"Your active project is: [{default_project.get('project_name')}]"))


def upload_assets(path: Optional[Path] = None, cohorts: Optional[str] = None):
    """
    Upload assets from path.

    :param path: The folder to upload assets.
    :return: None
    """
    # check path if exist
    if not path:
        questions = [
            inquirer.Path("path_result",
                          message=messages.ASSETS_FOLDER_MESSAGE,
                          default=os.getcwd()),
        ]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        path = answer.get("path_result")

    if not exists(path):
        print(messages.PATH_NOT_EXISTS_MESSAGE)
        sys.exit(1)

    if not cohorts:
        questions = [
            inquirer.Text("cohorts_res",
                          message=messages.ASSETS_COHORTS_MESSAGE,
                          default="main"),
        ]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        cohorts_res = answer.get("cohorts_res")
        cohorts = [
            cohorts.strip() for cohorts in cohorts_res.split(',')
            if cohorts.strip()
        ]

    files = os.listdir(path)

    num_batches = len(files) // ASSET_UPLOAD_BATCH_SIZE
    batches = [
        files[i * ASSET_UPLOAD_BATCH_SIZE:(i + 1) * ASSET_UPLOAD_BATCH_SIZE]
        for i in range(num_batches)
    ]

    if len(files) % ASSET_UPLOAD_BATCH_SIZE != 0:
        batches.append(files[num_batches * ASSET_UPLOAD_BATCH_SIZE:])

    # Loop Prepare asset metadata
    for _, batch in enumerate(batches):
        upload_session = datature.Asset.upload_session()
        add_progress = tqdm(batch)

        for file_name in add_progress:
            add_progress.set_description(
                f"{'Preparing file':<20}{file_name:>25}")

            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                upload_session.add(f"{path}/{file_name}")

        add_progress.close()
        upload_session.start(cohorts, early_return=False)


def upload_annotations(path: Optional[Path] = None,
                       annotation_format: Optional[str] = None):
    """
    Upload annotations from path.

    :param path: The annotation path to upload.
    :param annotation_format: The annotation format to upload.
    :return: None
    """
    if not path:
        questions = [
            inquirer.Path("path_result",
                          message=messages.ANNOTATION_FOLDER_MESSAGE),
        ]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        path = answer.get("path_result")

    if not isfile(path):
        print(messages.PATH_NOT_EXISTS_MESSAGE)
        sys.exit(1)

    if not annotation_format:
        questions = [
            inquirer.List(
                "annotation_format",
                message=messages.ANNOTATION_FORMAT_MESSAGE,
                choices=[format.value for format in AnnotationFormat],
            ),
        ]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        annotation_format = answer.get("annotation_format")

    datature.Annotation.upload(annotation_format, path, early_return=False)


def download_file_from_link(link: str, download_path: str):
    """
    Download file from link.

    :param link: The url link.
    :param download_path: The path to download file.
    :return: None
    """
    query_string_removed = link.split("?")[0]
    file_name = basename(query_string_removed)

    resp = requests.get(link,
                        stream=True,
                        timeout=datature.HTTP_TIMEOUT_SECONDS)

    total = int(resp.headers.get('content-length', 0))
    with open(join(download_path, file_name), 'wb') as file, tqdm(
            desc=file_name,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as download_bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            download_bar.update(size)


def get_available_artifact_format(model_name: str):
    """
    Get available artifact format from model name.

    :param model_name: The name of the model.
    :return: [str]
    """
    switcher = {
        "yolov4": ["tensorflow", "onnx"],
        "mask": ["tensorflow", "onnx"],
        "yolox": ["onnx"],
        "deeplabv3": ["onnx"],
        "unet": ["onnx"],
    }
    model_type = model_name.split("-")[0]
    return switcher.get(model_type, ["tensorflow", "tflite", "onnx"])


# pylint: disable=R0912,R0914
def download_artifact(artifact_id: Optional[str] = None,
                      model_format: Optional[str] = None,
                      path: Optional[str] = None):
    """
    Download artifact model.

    :param artifact_id: The id of the artifact.
    :param model_format: The artifact model to download.
    :param path: The path to download the model.
    :return: None
    """
    if not path:
        questions = [
            inquirer.Path("path_result",
                          message=messages.ARTIFACT_MODEL_FOLDER_MESSAGE,
                          default=os.getcwd()),
        ]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        path = answer.get("path_result")

    if not exists(path):
        print(messages.PATH_NOT_EXISTS_MESSAGE)
        sys.exit(1)

    if not artifact_id:
        # call server to list all artifacts
        artifacts = datature.Artifact.list()
        if len(artifacts) == 0:
            print(messages.NO_ARTIFACTS_MESSAGE)
            sys.exit(1)

        artifact_lists = []
        artifacts_key_map = {}
        for artifact in artifacts:
            key = (
                f"{artifact.get('run_id')[-6:].upper()}-{artifact.get('flow_title')}"
            )
            artifact_lists.append(key)
            artifacts_key_map[key] = artifact

        questions = [
            inquirer.List(
                "artifact",
                message=messages.ARTIFACT_DOWNLOAD_MESSAGE,
                choices=artifact_lists,
            ),
        ]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        artifact_key = answer.get("artifact")
        artifact = artifacts_key_map.get(artifact_key)

    model_type = get_available_artifact_format(artifact.get("model_name"))

    if not model_format:
        questions = [
            inquirer.List(
                "model_format",
                message=messages.ARTIFACT_MODEL_FORMAT_DOWNLOAD_MESSAGE,
                choices=model_type,
            ),
        ]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        model_format = answer.get("model_format")

    if model_format in artifact.get("exports"):
        # already exported, can download directly
        models = datature.Artifact.list_exported(artifact.get("id"))
        for model in models:
            if model.get("format") == model_format and model.get(
                    "status") == "Finished":

                download_file_from_link(model.get("download").get("url"), path)
    else:
        # already exported, can download directly
        models = datature.Artifact.export_model(artifact.get("id"),
                                                model_format)
        # Loop to query status,
        wait_spinner = Halo(text=messages.EXPORT_ARTIFACT_WAITING_MESSAGE,
                            spinner='dots')
        wait_spinner.start()

        while True:
            models = datature.Artifact.list_exported(artifact.get("id"))
            for model in models:
                if model.get("format") == model_format and model.get(
                        "status") == "Finished":
                    # start download
                    wait_spinner.stop()
                    download_file_from_link(
                        model.get("download").get("url"), path)

                    return

            time.sleep(datature.OPERATION_LOOPING_DELAY_SECONDS)


def download_annotations(path: Optional[Path] = None,
                         annotation_format: Optional[str] = None):
    """
    Export annotations from path.

    :param path: The annotation path to export.
    :param annotation_format: The annotation format to export.
    :return: None
    """
    if not path:
        questions = [
            inquirer.Path("path_result",
                          message=messages.EXPORT_ANNOTATION_FOLDER_MESSAGE,
                          default=os.getcwd()),
        ]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        path = answer.get("path_result")

    if not exists(path):
        print(messages.PATH_NOT_EXISTS_MESSAGE)
        sys.exit(1)

    if not annotation_format:
        questions = [
            inquirer.List(
                "annotation_format",
                message=messages.ANNOTATION_FORMAT_MESSAGE,
                choices=[format.value for format in AnnotationFormat],
            ),
            inquirer.Text(
                "normalized",
                message=messages.DOWNLOAD_ANNOTATIONS_NORMALIZED_MESSAGE),
            inquirer.Text(
                "shuffle",
                message=messages.DOWNLOAD_ANNOTATIONS_SHUFFLE_MESSAGE),
            inquirer.Text(
                "split_ratio",
                message=messages.DOWNLOAD_ANNOTATIONS_SPLIT_RATIO_MESSAGE),
        ]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        annotation_format = answer.get("annotation_format")
        normalized = answer.get("normalized") not in ["n", "N"]
        shuffle = answer.get("shuffle") not in ["n", "N"]
        split_ratio = float(answer.get("split_ratio"))

        if split_ratio < 0 or split_ratio > 1:
            print(messages.INVALID_SPLIT_RATIO_MESSAGE)
            sys.exit(1)

    operation = datature.Annotation.export(annotation_format,
                                           export_options={
                                               "normalized": normalized,
                                               "shuffle": shuffle,
                                               "split_ratio": split_ratio,
                                               "seed": 1337
                                           },
                                           early_return=False)

    annotation = datature.Annotation.retrieve_exported_file(
        operation.get("id"))
    download_file_from_link(annotation.get("download").get("url"), path)


def assets_group(cohort: Optional[str] = None):
    """
    List assets group statistics.

    :param cohort: The name of cohort name.
    :return: None
    """
    if not cohort:
        project = datature.Project.retrieve()

        if project.get("cohorts") is None or len(project.get("cohorts")) == 0:
            print(messages.NO_COHORTS_MESSAGE)
            sys.exit(1)

        questions = [
            inquirer.List(
                "cohort",
                message=messages.CHOOSE_COHORT_MESSAGE,
                choices=project.get("cohorts"),
            ),
        ]

        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        selected_cohort = answer.get("cohort")

        statistics = datature.Asset.statistic(selected_cohort)
        statistic = statistics[0].get("statistic")

        print((f"[{selected_cohort}]\n"
               f"Total {statistic['asset_total']}\n"
               f"Annotated {statistic['asset_annotated']}\n"
               f"Reviewed {statistic['asset_reviewed']}\n"
               f"Tofixed {statistic['asset_tofixed']}\n"
               f"Completed {statistic['asset_completed']}"))
