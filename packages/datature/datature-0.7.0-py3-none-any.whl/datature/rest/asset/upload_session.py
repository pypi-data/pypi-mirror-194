#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   upload_session.py
@Author  :   Raighne.Weng
@Version :   0.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Asset Upload Session
'''

import os
import struct
from os.path import exists
from requests import request
import google_crc32c
import filetype
import cv2
from tqdm import tqdm
import datature
from datature import error, logger
from datature.http.resource import RESTResource
from datature.rest.operation import Operation


class UploadSession(RESTResource):
    """Datature Asset Upload Session Class."""

    def __init__(self):
        self.assets = []
        self.file_name_map = {}

    def add(self, file_path: str):
        """Add asset to upload."""
        if len(self.assets) >= datature.ASSET_UPLOAD_BATCH_SIZE:
            raise error.Error("One upload session allow max 5000 assets.")

        if not exists(file_path):
            raise error.Error("Cannot find the Asset file")

        with open(file_path, 'rb') as file:
            contents = file.read()

            # calculate file crc32
            file_hash = google_crc32c.Checksum()
            file_hash.update(contents)

            # To fix the wrong crc32 caused by mac M1 clip
            crc32 = struct.unpack(">l", file_hash.digest())[0]

            # Prepare filename size and mime type
            filename = os.path.basename(file_path)
            size = os.path.getsize(file_path)

            mime_kind = filetype.guess(file_path)

            file.close()

            if self.file_name_map.get(filename) is not None:
                raise error.Error(
                    f"Cannot add multiple files with the same name, {filename}"
                )

            if (filename and size and crc32 and mime_kind):
                if mime_kind.mime in ["image/jpeg", "image/png"]:
                    metadata = {
                        "filename": filename,
                        "size": size,
                        "crc32c": crc32,
                        "mime": mime_kind.mime
                    }
                elif mime_kind.mime == "video/mp4":
                    cap = cv2.VideoCapture(file_path)
                    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    four_c_c = int(cap.get(cv2.CAP_PROP_FOURCC))
                    codec = chr(four_c_c
                                & 0xff) + chr((four_c_c >> 8) & 0xff) + chr(
                                    (four_c_c >> 16)
                                    & 0xff) + chr((four_c_c >> 24) & 0xff)
                    print(codec)
                    if not codec.startswith('avc1'):
                        raise error.Error("UnSupported asset file")

                    metadata = {
                        "filename": filename,
                        "size": size,
                        "crc32c": crc32,
                        "mime": mime_kind.mime,
                        "frames": frames,
                        "encoder": {
                            "profile": "h264Saver",
                            "everyNthFrame": 1
                        },
                    }
                else:
                    raise error.Error("UnSupported asset file")

                self.assets.append(metadata)
                self.file_name_map[filename] = {"path": file_path}

                logger.log_info("Add asset:", metadata=metadata)
            else:
                raise error.Error("UnSupported asset file")

    def start(self, cohorts: [str] = None, early_return=True) -> dict:
        """Request server to get signed ur and upload file to gcp."""

        # Set default cohorts
        if cohorts is None:
            cohorts = ["main"]

        # check asset length
        if not self.assets:
            raise error.Error("Assets to upload is empty")

        # call API to get signed url
        response = self.request("POST",
                                "/asset/uploadSession",
                                request_body={
                                    "cohorts": cohorts,
                                    "assets": self.assets
                                })

        op_link = response["op_link"]

        assets_upload_progress = None
        if datature.SHOW_PROGRESS:
            assets_upload_progress = tqdm(total=len(response["assets"]))

        for asset_upload in response["assets"]:
            file_name = asset_upload["metadata"]["filename"]
            file_path = self.file_name_map.get(file_name)["path"]

            with open(file_path, 'rb') as file:
                contents = file.read()

                logger.log_info("Start Uploading" + file_path)

                # upload asset to GCP one by one
                request("PUT",
                        asset_upload["upload"]["url"],
                        headers=asset_upload["upload"]["headers"],
                        data=contents,
                        timeout=10)
                logger.log_info("Done Uploading" + file_path)

                if assets_upload_progress is not None:
                    assets_upload_progress.update(1)
                    assets_upload_progress.set_description(
                        f"{'Uploading file':<20}{file_name:>25}")

        if assets_upload_progress is not None:
            assets_upload_progress.close()

        if early_return:
            return {"op_link": op_link}

        return Operation.loop_retrieve(op_link)
