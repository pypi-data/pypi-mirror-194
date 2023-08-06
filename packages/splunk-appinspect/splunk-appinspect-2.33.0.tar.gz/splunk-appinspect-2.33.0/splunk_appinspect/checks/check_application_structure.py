# Copyright 2019 Splunk Inc. All rights reserved.

"""
### Directory structure standards

Ensure that the directories and files in the app adhere to hierarchy standards.
"""

import logging
import os
import re
import string

import splunk_appinspect
from splunk_appinspect.common.file_hash import md5
from splunk_appinspect.splunk import normalizeBoolean

report_display_order = 2
logger = logging.getLogger(__name__)


@splunk_appinspect.tags(
    "splunk_appinspect", "appapproval", "cloud", "self-service", "private_app", "private_victoria", "private_classic"
)
@splunk_appinspect.cert_version(min="1.0.0")
@splunk_appinspect.display(report_display_order=1)
def check_that_local_does_not_exist(app, reporter):
    """Check that the 'local' directory does not exist.  All configuration
    should be in the 'default' directory.
    """
    if app.directory_exists("local"):
        reporter_output = "A 'local' directory exists in the app."
        reporter.fail(reporter_output)


@splunk_appinspect.tags(
    "splunk_appinspect",
    "cloud",
    "self-service",
    "private_app",
    "private_victoria",
    "private_classic"
)
@splunk_appinspect.cert_version(min="1.1.9")
def check_for_local_meta(app, reporter):
    """Check that the file 'local.meta' does not exist.  All metadata
    permissions should be set in 'default.meta'.
    """
    if app.file_exists("metadata", "local.meta"):
        file_path = os.path.join("metadata", "local.meta")
        reporter_output = (
            "Do not supply a local.meta file- put all settings"
            f" in default.meta. File: {file_path}"
        )
        reporter.fail(reporter_output, file_path)


@splunk_appinspect.tags("cloud", "private_app", "private_victoria", "private_classic")
@splunk_appinspect.cert_version(min="1.1.16")
def check_that_local_passwords_conf_does_not_exist(app, reporter):
    """Check that `local/passwords.conf` does not exist.  Password files are not
    transferable between instances.
    """
    if app.directory_exists("local"):
        if app.file_exists("local", "passwords.conf"):
            file_path = os.path.join("local", "passwords.conf")
            reporter_output = (
                "A 'passwords.conf' file exists in the 'local'"
                f" directory of the app. File: {file_path}"
            )
            reporter.fail(reporter_output, file_path)
        else:
            pass  # No passwords.conf so it passes
    else:
        reporter_output = "The local directory does not exist."
        reporter.not_applicable(reporter_output)


@splunk_appinspect.tags("splunk_appinspect", "cloud", "private_app", "private_victoria", "private_classic")
@splunk_appinspect.cert_version(min="1.5.0")
def check_filenames_for_spaces(app, reporter):
    """Check that app has no .conf or dashboard filenames that contain spaces.
    Splunk software does not support such files.
    """
    # <app_dir>/default contains configuration required by your app and dashboard files,
    # so set it as the base directory.
    for directory, file, _ in list(
        app.iterate_files(basedir="default", types=[".conf"])
    ) + list(app.iterate_files(basedir="default/data", types=[".xml"])):
        if re.search(r"\s", file):
            filename = os.path.join(directory, file)
            # The regex that extracts the filename would extract wrong file name due to the space,
            # so here I use `Filename: {}`.
            reporter_output = f"A conf or dashboard file contains a space in the filename. Filename: {filename}"
            reporter.fail(reporter_output)


@splunk_appinspect.tags("splunk_appinspect", "cloud", "private_app", "private_victoria", "private_classic")
@splunk_appinspect.cert_version(min="1.6.0")
def check_that_app_name_config_is_valid(app, reporter):
    """Check that the app name does not start with digits"""
    if app.package.app_cloud_name.startswith(tuple(string.digits)):
        reporter_output = "The app name (%s) cannot start with digits!" % app.name
        reporter.fail(reporter_output)
    else:
        pass
