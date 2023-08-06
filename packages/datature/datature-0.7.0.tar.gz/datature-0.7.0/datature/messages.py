#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   messages.py
@Author  :   Raighne.Weng
@Version :   0.7.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   collect all string messages variables
'''

REQUEST_SERVER_MESSAGE = 'Communication with server.\n'
SERVER_PROCESSING_MESSAGE = 'Server processing in progress.\n'
SERVER_COMPLETED_MESSAGE = 'Server processing completed.\n'
ASSETS_FOLDER_MESSAGE = 'Enter the assets folder to be uploaded'
ASSETS_COHORTS_MESSAGE = "Enter assets cohorts to be upload, split by ','"
COHORT_MUST_BE_STRING_MESSAGE = "cohort must be string"
COHORTS_INVALID_MESSAGE = "Invalid cohorts type, cohorts must be a string array:"
ANNOTATION_FOLDER_MESSAGE = "Enter the file path to be upload"
ANNOTATION_FORMAT_MESSAGE = "Which format is the file to be uploaded?"
NO_ARTIFACTS_MESSAGE = "No artifact can be download, please start a training first."
ARTIFACT_DOWNLOAD_MESSAGE = "Which artifact do you want to download?"
ARTIFACT_MODEL_FORMAT_DOWNLOAD_MESSAGE = "Which format do you want to download?"
EXPORT_ARTIFACT_WAITING_MESSAGE = "Server processing in progress, it may take 5-10 minutes.\n"
ARTIFACT_MODEL_FOLDER_MESSAGE = 'Enter the folder path to download model'
EXPORT_ANNOTATION_FOLDER_MESSAGE = "Enter the path to be download"
CHOOSE_COHORT_MESSAGE = "Which cohort do you want to list?"
NO_PROJECT_MESSAGE = "No saved projects, please use 'datature project auth' first."
INVALID_PROJECT_MESSAGE = "Invalid project name."
PATH_NOT_EXISTS_MESSAGE = "Path not exists."
NO_COHORTS_MESSAGE = "No cohorts in this project, please create cohorts first."
INVALID_PROJECT_SECRET_MESSAGE = "Invalid project secret."
AUTHENTICATION_MESSAGE = "Authentication succeeded."
AUTHENTICATION_REMINDER_MESSAGE = (
    "Project Secret needed, "
    "generate one for your project on nexus: Advanced/API Management")
DOWNLOAD_ANNOTATIONS_NORMALIZED_MESSAGE = "Whether the download should be normalized? [Y/n]"
DOWNLOAD_ANNOTATIONS_SHUFFLE_MESSAGE = "Whether the download should be shuffled? [Y/n]"
DOWNLOAD_ANNOTATIONS_SPLIT_RATIO_MESSAGE = "Enter the split ratio for this download. [0-1]"
INVALID_SPLIT_RATIO_MESSAGE = "Invalid split ratio."
AUTHENTICATION_FAILED_MESSAGE = "\nAuthentication failed, please use 'datature project auth' again."
UNKNOWN_ERROR_SUPPORT_MESSAGE = "\nRequest Failed, please contact our support."
