#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from app.application import Application
from app.logz import create_logger
from app.internal.login import login
from app.internal.assessments_editor import new_assessment, all_assessments, upload_data


class Test_Assessment:
    logger = create_logger()

    def test_init(self):
        """Init"""
        with open("init.yaml", "r", encoding="utf-8") as file:
            data = file.read()
            self.logger.debug("init file: %s", data)
            assert len(data) > 5

    def test_assessments_editor_build(self):
        """Simple login test"""

        app = Application()
        self.logger.debug(os.getenv("REGSCALE_USER"))
        self.logger.debug(os.getenv("REGSCALE_PASSWORD"))

        jwt = login(os.getenv("REGSCALE_USER"), os.getenv("REGSCALE_PASSWORD"), app=app)
        self.logger.info(jwt)
        assert jwt is not None

    def test_assessments_editor_new_assessment(self):
        path = os.path.join(os.getcwd() + r"\artifacts")

        # load workbook for creation of new assessment

        new_assessment(path)

    def test_assessments_editor_all_assessments(self):
        regscale_parent_id = 64
        regscale_module = "securityplans"
        path = os.path.join(os.getcwd() + r"\artifacts")

        # Load workboook and upload data from RegScale database for editing

        all_assessments(regscale_parent_id, regscale_module, path)

    def test_assessments_editor_upload_data(self):
        path = os.path.join(os.getcwd() + r"\artifacts")

        # # Check file for changes and upload changes to RegScale database and delete files

        upload_data(path)
