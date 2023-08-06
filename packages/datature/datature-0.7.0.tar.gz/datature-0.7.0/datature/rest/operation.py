#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   operation.py
@Author  :   Raighne.Weng
@Version :   0.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Operation API
'''

import time
from halo import Halo
from datature.http.resource import RESTResource
from datature.messages import SERVER_PROCESSING_MESSAGE, SERVER_COMPLETED_MESSAGE
from datature import error, logger
import datature


class Operation(RESTResource):
    """Datature Operation API Resource."""

    @classmethod
    def retrieve(cls, op_link: str) -> dict:
        """Get a operation.

        :param op_link: the operation link
        :return: response json data
        """
        return cls.request("GET", "/operation", query={"opLink": op_link})

    @classmethod
    def loop_retrieve(
            cls,
            op_link: str,
            loop_times: int = datature.OPERATION_LOOPING_TIMES) -> dict:
        """Loop query a operation.

        :param op_link: the operation link
        :param loop_times: the operation link
        :return: response json data
        """
        request_spinner = None

        if datature.SHOW_PROGRESS:
            request_spinner = Halo(text=SERVER_PROCESSING_MESSAGE,
                                   spinner='dots')

        for _ in range(loop_times):
            response = cls.request("GET",
                                   "/operation",
                                   query={"opLink": op_link})

            if request_spinner is not None:
                request_spinner.start()

            logger.log_info("Operation status:", status=response["status"])

            if response["status"]["overview"] == "Finished":
                if request_spinner is not None:
                    request_spinner.succeed(SERVER_COMPLETED_MESSAGE)
                    request_spinner.stop()
                return response

            if response["status"]["overview"] == "Errored":
                logger.log_info("Operation error: please contacts our support")

                if request_spinner is not None:
                    request_spinner.stop()

                raise error.BadRequestError(
                    "Operation error: please contacts our support")

            time.sleep(datature.OPERATION_LOOPING_DELAY_SECONDS)

        if request_spinner is not None:
            request_spinner.stop()
        return None
