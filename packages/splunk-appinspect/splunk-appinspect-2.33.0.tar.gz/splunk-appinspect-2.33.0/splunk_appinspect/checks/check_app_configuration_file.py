# Copyright 2019 Splunk Inc. All rights reserved.

"""
### App.conf standards

The **app.conf** file located at **default/app.conf** provides key application information and branding. For more, see [app.conf](https://docs.splunk.com/Documentation/Splunk/latest/Admin/Appconf).
"""

import logging
import os
from pathlib import Path
import re
import json

import splunk_appinspect
from splunk_appinspect.app_util import AppVersionNumberMatcher
from splunk_appinspect.check_messages import WarningMessage, FailMessage, NotApplicableMessage
from splunk_appinspect.splunk import normalizeBoolean
from splunk_appinspect.checks import Check, CheckConfig
from splunk_appinspect.splunk_defined_conf_file_list import SPLUNK_DEFINED_CONFS
from splunk_appinspect.app_configuration_file import _is_check_app_config_file

report_display_order = 2
logger = logging.getLogger(__name__)


@splunk_appinspect.tags("splunk_appinspect", "appapproval")
@splunk_appinspect.cert_version(min="1.0.0")
def check_app_version(app, reporter):
    """Check that the `app.conf` contains an application version number in the
    [launcher] stanza.
    """
    if app.file_exists("default", "app.conf"):
        filename = os.path.join("default", "app.conf")
        config = app.get_config("app.conf")
        matcher = AppVersionNumberMatcher()

        try:
            config.has_option("launcher", "version")
            version = config.get("launcher", "version")
            if not matcher.match(version):
                lineno = config.get_section("launcher").get_option("version").lineno
                reporter_output = (
                    "Major, minor, build version numbering "
                    f"is required. File: {filename}, Line: {lineno}."
                )
                reporter.fail(reporter_output, filename, lineno)

        except splunk_appinspect.configuration_file.NoOptionError:
            lineno = config.get_section("launcher").lineno
            reporter_output = (
                "No version specified in launcher section "
                f"of app.conf. File: {filename}, Line: {lineno}."
            )
            reporter.fail(reporter_output, filename, lineno)

        except splunk_appinspect.configuration_file.NoSectionError:
            reporter_output = f"No launcher section found in app.conf. File: {filename}"
            reporter.fail(reporter_output, file_name=filename)
    else:
        reporter_output = "`default/app.conf` does not exist."
        reporter.not_applicable(reporter_output)


@splunk_appinspect.tags("splunk_appinspect")
@splunk_appinspect.cert_version(min="1.1.20")
def check_that_setup_has_not_been_performed(app, reporter):
    """Check that `default/app.conf` setting `is_configured` = False."""
    if app.file_exists("default", "app.conf"):
        filename = os.path.join("default", "app.conf")
        app_conf = app.app_conf()
        if app_conf.has_section("install") and app_conf.has_option(
                "install", "is_configured"
        ):
            # Sets to either 1 or 0
            is_configured = normalizeBoolean(app_conf.get("install", "is_configured"))
            if is_configured:
                lineno = (
                    app_conf.get_section("install").get_option("is_configured").lineno
                )
                reporter_output = (
                    "The app.conf [install] stanza has the"
                    " `is_configured` property set to true."
                    " This property indicates that a setup was already"
                    f" performed. File: {filename}, Line: {lineno}."
                )
                reporter.fail(reporter_output, filename, lineno)
            else:
                pass  # Pass - The property is true
        else:
            pass  # Pass - The stanza or property does not exist.
    else:
        reporter_output = "`default/app.conf` does not exist."
        reporter.not_applicable(reporter_output)


@splunk_appinspect.tags(
    "splunk_appinspect",
    "cloud",
    "private_app",
    "private_victoria",
    "private_classic"
)
@splunk_appinspect.cert_version(min="2.0.1")
def check_for_valid_package_id(app, reporter):
    """
    Check that the [package] stanza in app.conf has a valid `id` value.
    See https://docs.splunk.com/Documentation/Splunk/latest/Admin/Appconf for details.
    """
    app_config_skip_check = _is_check_app_config_file(app, reporter, "skip")
    if not app_config_skip_check:
        filename = os.path.join("default", "app.conf")
        app_conf = app.app_conf()
        uncompressed_directory_name = app.name
        package_id = id_name = None

        try:
            package_configuration_section = app_conf.get_section("package")
            package_id_object = package_configuration_section.get_option("id")
            package_id = package_id_object.value
            if not _is_package_id_valid(package_id_object):
                lineno = package_configuration_section.get_option("id").lineno
                reporter_output = (
                    f"The app.conf [package] stanza's has an invalid 'id' property: {package_id}."
                    " For the `id` property, it must contain only letters, numbers, `.` (dot),"
                    " `_` (underscore) and `-`(hyphen) characters, should not start with numbers, "
                    " and cannot end with a dot character."
                    " Besides, some reserved names are prohibited."
                    " See https://docs.splunk.com/Documentation/Splunk/latest/Admin/Appconf for details."
                    f" File: {filename}, [package]id Line: {lineno}."
                )
                reporter.fail(reporter_output, filename, lineno)

            if package_id != uncompressed_directory_name:
                # Fail, app id is present but id does not match directory name
                lineno = package_configuration_section.get_option("id").lineno
                reporter_output = (
                    "The `app.conf` [package] stanza has an `id` property"
                    " that does not match the uncompressed directory's name."
                    f" `app.conf` [package] id: {package_id}"
                    f" uncompressed directory name: {uncompressed_directory_name}."
                    f" File: {filename}, [package]id Line: {lineno}."
                )
                reporter.fail(reporter_output, filename, lineno)

        except splunk_appinspect.configuration_file.NoOptionError:
            lineno_package = package_configuration_section.lineno
            reporter_output = (
                "No `id` property found in [package] stanza. `id` is required by the Splunk platform to "
                "enable updates of apps published to Splunkbase. If you intend to publish this app to Splunkbase, "
                "please add an `id` to the [package] stanza."
                "If this app will be installed as a Private app on a Splunk Cloud stack, and the target stack is "
                "running a Splunk Cloud platform version earlier than 8.2.2112, the `id` property is *required* for "
                "installation."
                f"File: {filename}, [package] Line: {lineno_package}."
            )
            reporter.warn(reporter_output, filename, lineno_package)

        except splunk_appinspect.configuration_file.NoSectionError:
            reporter_output = (
                "No `[package]` section found in app.conf file."
            )
            reporter.warn(reporter_output, filename)

        try:
            app_conf.has_option("id", "name")
            id_configuration_section = app_conf.get_section("id")
            id_name = id_configuration_section.get_option("name").value

            if package_id != id_name:
                name_lineno = id_configuration_section.get_option("name").lineno
                reporter_output = (
                    "The `app.conf` [package] stanza has an `id` property"
                    " that does not match the `name` property of the [id] stanza."
                    f" `app.conf` [package] id: {package_id}"
                    f" [id] name: {id_name}."
                    f" File: {filename}, [id]name Line: {name_lineno}."
                )
                reporter.fail(reporter_output, filename, name_lineno)

        except splunk_appinspect.configuration_file.NoOptionError:
            lineno_id = id_configuration_section.lineno
            reporter_output = (
                "No `name` attribute specified in the [id] stanza in app.conf."
                f" This attribute is required for app installation. File: {filename}, [id] line: {lineno_id}."
            )
            reporter.warn(reporter_output, filename, lineno_id)

        except splunk_appinspect.configuration_file.NoSectionError:
            reporter_output = (
                "No [id] stanza specified in app.conf. An id` attribute in the [id] "
                "stanza is required for app installation."
            )
            reporter.warn(reporter_output, filename)

    if not app.package.does_working_artifact_contain_app_manifest():
        reporter_output = (
            "Splunk App packages doesn't contain"
            " `app.manifest file`."
            " No `app.manifest` was found."
        )
        reporter.skip(reporter_output)
        return

    manifest_filename = os.path.join("app.manifest")
    try:
        filepath = open(os.path.join(app.app_dir, "app.manifest"), "r")
        manifest_json = json.loads(filepath.read())
        manifest_name = manifest_json.get("info").get("id").get("name")

        if package_id is not None and package_id != manifest_name:
            id_lineno = package_configuration_section.get_option("id").lineno
            reporter_output = (
                "An `app.manifest` file isn't required, but if present it must contain an info.id.name attribute,"
                " which must match the value of the [package] stanza's `id` attribute in `app.conf`."
                f" `app.conf` [package] id: {package_id}"
                f" [info][id] name: {manifest_name}."
                f" `File`: {filename} or {manifest_filename}, `[package]id Line`: {id_lineno}."
            )
            reporter.fail(reporter_output, manifest_filename)

        if id_name is not None and id_name != manifest_name:
            name_lineno = id_configuration_section.get_option("name").lineno
            reporter_output = (
                "The `app.manifest` file isn't required, but if present it must contain info.id.name attribute,"
                " which must match the value  of the [id] stanza's `name` attribute in `app.conf`."
                f" `app.conf` [id] name: {id_name}"
                f" [info][id] name: {manifest_name}."
                f" `File`: {filename} or {manifest_filename}, `[id]name Line`: {name_lineno}."
            )
            reporter.fail(reporter_output, manifest_filename)

    except ValueError:
        reporter_output = (
            "No `name` attribute specified under `[info][id]` "
            f"section of app.manifest. File: {manifest_filename}."
        )
        reporter.not_applicable(reporter_output)
        return

    except AttributeError:
        reporter_output = (
            "No `[info]` or `[id]` stanza found in app.manifest."
            f"Or app.manifest file is empty. File: {manifest_filename}"
        )
        reporter.not_applicable(reporter_output)
        return

    except:
        reporter_output = (
            f"The `app.manifest` file can't be loaded properly."
            f" Please submit the file in correct format. File: {manifest_filename}"
        )
        reporter.not_applicable(reporter_output)
        return

@splunk_appinspect.tags("splunk_appinspect")
@splunk_appinspect.cert_version(min="1.6.0")
def check_for_invalid_app_names(app, reporter):
    """Check that `default/app.conf` has `author = <some words are not about Splunk>` must not
    has attributes `label` or `description` with values of `Splunk App for XXXX`.
    """
    if app.file_exists("default", "app.conf"):
        filename = os.path.join("default", "app.conf")
        app_conf = app.app_conf()
        is_author_splunk = _is_author_splunk(app_conf)
        if app_conf.has_option("ui", "label"):
            name = app_conf.get("ui", "label")
            if _is_with_value_of_splunk_app_for(name) and not is_author_splunk:
                lineno = app_conf.get_section("ui").get_option("label").lineno
                reporter_output = (
                    "For the app.conf [ui] stanza's 'label' attribute,"
                    " names of community-built apps must not start with 'Splunk'."
                    " For example 'Splunk app for Awesome' is inappropriate,"
                    f" but 'Awesome app for Splunk' is OK. File: {filename}, Line: {lineno}."
                )
                reporter.fail(reporter_output, filename, lineno)
        if app_conf.has_option("launcher", "description"):
            name = app_conf.get("launcher", "description")
            if _is_with_value_of_splunk_app_for(name) and not is_author_splunk:
                lineno = (
                    app_conf.get_section("launcher").get_option("description").lineno
                )
                reporter_output = (
                    "For the app.conf [launcher] stanza's 'description' attribute,"
                    " apps built by 3rd parties should not have names starting with Splunk."
                    " For example 'Splunk app for Awesome' is inappropriate,"
                    f" but 'Awesome app for Splunk' is OK. File: {filename}, Line: {lineno}."
                )
                reporter.fail(reporter_output, filename, lineno)
    else:
        reporter_output = "`default/app.conf` does not exist."
        reporter.not_applicable(reporter_output)


def _is_with_value_of_splunk_app_for(name):
    # the regex expression is for searching:
    # "splunk (addon|add on|add-on|app)s for"
    return bool(
        re.search(r"splunk\s*(add(\s*|-*)on|app)(s*)\s*for", name, re.IGNORECASE)
    )


def _is_author_splunk(app_conf):
    if app_conf.has_option("launcher", "author"):
        if re.search(r"splunk", app_conf.get("launcher", "author"), re.IGNORECASE):
            return True
    for name in app_conf.section_names():
        if re.search(r"author=", name):
            if re.search(r"splunk", name, re.IGNORECASE):
                return True

            if app_conf.has_option(name, "company"):
                return bool(
                    re.search(r"splunk", app_conf.get(name, "company"), re.IGNORECASE)
                )
    return False


@splunk_appinspect.tags("splunk_appinspect", "cloud", "private_app", "private_victoria", "private_classic", "future")
@splunk_appinspect.cert_version(min="1.6.0")
def check_no_install_source_checksum(app, reporter):
    """Check in `default/app.conf` and 'local/app.conf', install_source_checksum not be set explicitly."""
    file_folder_list = ["default", "local"]
    stanza = "install_source_checksum"
    for folder in file_folder_list:
        if not app.file_exists(folder, "app.conf"):
            reporter_output = f"`{folder}/app.conf` does not exist."
            reporter.not_applicable(reporter_output)
            continue

        filename = os.path.join(folder, "app.conf")
        app_conf = app.app_conf(folder)
        if not app_conf.has_section("install"):
            continue  # Pass - The stanza does not exist.

        if not app_conf.has_option("install", stanza):
            continue  # Pass - The property does not exist

        if not app_conf.get("install", stanza):
            continue  # Pass - The property is empty.

        lineno = (
            app_conf.get_section("install").get_option(stanza).lineno
        )
        reporter_output = (
            f"For the app.conf [install] stanza's `{stanza}` attribute,"
            " it records a checksum of the tarball from which a given app was installed"
            " or a given app's local configuration was installed."
            " Splunk Enterprise will automatically populate this value during installation."
            " Developers should *not* set this value explicitly within their app!"
            f" File: {filename}, Line: {lineno}."
        )
        reporter.warn(reporter_output, filename, lineno)


@splunk_appinspect.tags("splunk_appinspect", "cloud", "private_app", "private_victoria", "private_classic", "future")
@splunk_appinspect.cert_version(min="1.6.0")
def check_no_install_source_local_checksum(app, reporter):
    """Check in `default/app.conf` and 'local/app.conf', install_source_local_checksum not be set explicitly."""
    stanza = "install_source_local_checksum"
    file_folder = ["default", "local"]
    for folder in file_folder:
        if not app.file_exists(folder, "app.conf"):
            reporter_output = f"`{folder}/app.conf` does not exist."
            reporter.not_applicable(reporter_output)
            continue

        filename = os.path.join(folder, "app.conf")
        app_conf = app.app_conf(folder)

        if not app_conf.has_section("install"):
            continue  # Pass - The stanza does not exist.

        if not app_conf.has_option("install", stanza):
            continue  # Pass - The property does not exist

        if not app_conf.get("install", stanza):
            continue  # Pass - The property is empty.

        lineno = (
            app_conf.get_section("install").get_option(stanza).lineno
        )
        reporter_output = (
            f"For the app.conf [install] stanza's `{stanza}` attribute,"
            " it records a checksum of the tarball from which a given app was installed"
            " or a given app's local configuration was installed."
            " Splunk Enterprise will automatically populate this value during installation."
            " Developers should *not* set this value explicitly within their app!"
            f" File: {filename}, Line: {lineno}."
        )
        reporter.warn(reporter_output, filename, lineno)


class CheckForTriggerStanza(Check):
    def __init__(self):
        super().__init__(config=CheckConfig(
            name="check_for_trigger_stanza",
            description="Check that `default/app.conf` or `local/app.cong` doesn't have a `reload.<CONF_FILE>`, "
                        "where CONF_FILE is a non-custom conf. ("
                        "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Appconf#.5Btriggers.5D)",
            depends_on_config=("app",),
            cert_min_version="1.7.2",
            tags=(
                "splunk_appinspect",
                "cloud",
                "private_app",
                "private_classic",
                "private_victoria",
            )
        ))

    def check_config(self, app, config):
        if not config["app"].has_section("triggers"):
            return

        settings = config["app"].get_section("triggers").settings()
        default_meta_path = os.path.join("metadata", "default.meta")
        conf_permissions = (
            _get_conf_permissions(app.get_meta("default.meta"))
            if app.file_exists(default_meta_path)
            else {}
        )

        for conf_name, lineno in _get_reloaded_splunk_confs(settings):
            if _is_exported(conf_name, conf_permissions):
                yield FailMessage(
                    f"{conf_name}.conf is a Splunk defined conf, which should not "
                    "be configured in [trigger] stanza. Per the documentation, "
                    "it should be configured only for custom config file. "
                    "Please remove this line.",
                    file_name=config["app"].get_relative_path(),
                    line_number=lineno,
                )
            else:
                yield WarningMessage(
                    f"{conf_name}.conf is a Splunk defined conf, which should not "
                    "be configured in [trigger] stanza. Per the documentation, "
                    "it should be configured only for custom config file. "
                    f"However, the {conf_name}.conf is not shared with other apps. "
                    "Suggest to remove this line.",
                    file_name=config["app"].get_relative_path(),
                    line_number=lineno,
                )


class CheckForValidUiLabel(Check):
    def __init__(self):
        super().__init__(config=CheckConfig(
            name="check_for_valid_ui_label",
            description="Check that the `default/app.conf` or or `local/app.cong` contains a label key value pair in "
                        "the [ui] stanza and the length is between 5 and 80 characters inclusive.",
            depends_on_config=("app",),
            cert_min_version="2.3.0",
            tags=(
                "splunk_appinspect",
                "cloud",
                "private_app",
                "private_classic",
                "private_victoria",
            )
        ))

    MIN_LENGTH = 5
    MAX_LENGTH = 80

    def check_config(self, app, config):
        # return not_applicable if ui stanza does not exist
        if not config["app"].has_section("ui"):
            yield NotApplicableMessage(
                "`default/app.conf` or `local/app.conf` does not contain [ui] stanza.",
                file_name=config["app"].get_relative_path(),
            )
            return

        # return warning if label field does not exist in ui stanza
        if not config["app"].has_option("ui", "label"):
            yield WarningMessage(
                "`label` is required in [ui] stanza.",
                file_name=config["app"].get_relative_path(),
                line_number=config["app"]["ui"].get_line_number(),
            )
            return

        label_option = config["app"]["ui"]["label"]
        if len(label_option.value) < self.MIN_LENGTH or len(label_option.value) > self.MAX_LENGTH:
            yield WarningMessage(
                "The length of `label` field under [ui] stanza should between 5 to 80 characters.",
                file_name=config["app"].get_relative_path(),
                line_number=config["app"]["ui"]["label"].get_line_number(),
            )
            return

@splunk_appinspect.tags("splunk_appinspect", "cloud", "private_app", "private_victoria", "private_classic")
def check_reload_trigger_for_all_custom_confs(app, reporter):
    """Check that custom conf files have a corresponding reload trigger in app.conf

    Without a reload trigger the app will request a restart on any change to the conf file,
    which may be a negative experience for end-users.
    """

    # Get all custom confs
    custom_confs = []
    for directory, filename, _ in app.iterate_files(
            types=[".conf"], basedir=["default", "local"]
    ):
        if filename not in SPLUNK_DEFINED_CONFS:
            custom_confs.append(filename)

    # Pass the check if there are no custom confs
    if not custom_confs:
        return

    # Get the app config
    app_conf = app.app_conf()
    if not app_conf.has_section("triggers"):
        reporter.fail(
            f"App contains custom conf(s) {custom_confs} but does not have a [triggers] stanza in app.conf. "
            f"Without a reload trigger the app will request a restart on any change to the conf file, "
            f"which may be a negative experience for end-users."
        )
        return

    # Check that all the custom confs have a reload trigger
    # e.g. "banana.conf" -> "reload.banana" in app.conf
    for custom_conf in custom_confs:
        reload_option_name = f"reload.{os.path.splitext(custom_conf)[0]}"
        if app_conf.has_option("triggers", reload_option_name):
            if app_conf.get_option("triggers", reload_option_name).value == "never":
                reporter.warn(
                    f"App contains custom conf(s) {custom_confs} but app.conf "
                    f"have a [triggers] stanza has a setting value for reload of "
                    f"'never' which would trigger restarts on any change to "
                    f"the conf file, which may be a negative experience for end-users."
                )
        else:
            reporter.fail(
                f"Custom conf file {custom_conf} does not have a reload trigger in app.conf. "
                f"Without a reload trigger the app will request a restart on any change to the conf file, "
                f"which may be a negative experience for end-users."
            )

def _get_conf_permissions(default_meta):
    conf_permissions = {}
    meta_stanza_pattern = r"(?=\/).*"
    for section in default_meta.sections():
        name = re.sub(meta_stanza_pattern, "", section.name) or "default"
        is_exported = (
                section.has_option("export")
                and section.get_option("export").value == "system"
        )
        conf_permissions[name] = is_exported
    return conf_permissions


def _get_reloaded_splunk_confs(settings):
    splunk_conf_whitelist = ["passwords.conf"]
    reload_pattern = r"^reload\."
    for setting in settings:
        if re.match(reload_pattern, setting.name):
            conf_name = re.sub(reload_pattern, "", setting.name)
            conf_file_name = f"{conf_name}.conf"
            if (
                    conf_file_name in SPLUNK_DEFINED_CONFS
                    and conf_file_name not in splunk_conf_whitelist
            ):
                yield conf_name, setting.lineno


def _is_exported(conf_name, conf_permissions):
    if conf_name in conf_permissions:
        return conf_permissions[conf_name]

    default_stanza = "default"
    if default_stanza in conf_permissions:
        return conf_permissions[default_stanza]

    return False


def _is_package_id_with_hyphen(package_id):
    """Check that if package id contains '-'"""
    return "-" in package_id.value


def _is_package_id_valid(package_id):
    """
    Check rules for package id:
        1. must contain only letters, numbers, "." (dot), and "_" (underscore) characters.
           Besides, '-' should be add into the white list, see https://jira.splunk.com/browse/ACD-3636.
        2. must not end with a dot character
        3. must not be any of the following names: CON, PRN, AUX, NUL,
           COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9,
           LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, LPT9
    Best practice:
        1. do not endwith '.tar', '.tgz', '.tar.gz' and '.spl'
    """
    blcak_list = [
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    ]

    # check for rule 1
    pattern = re.compile(r"[a-zA-Z_.-][a-zA-Z0-9_.-]*")
    results = re.findall(pattern, package_id.value)
    if not results.__contains__(package_id.value):
        return False
    # check for rule 2 and best practice
    if package_id.value.endswith((".", ".tar", ".tar.gz", ".tgz", ".spl")):
        return False
    # check for rule 3
    if package_id.value in blcak_list:
        return False

    return True


@splunk_appinspect.tags("splunk_appinspect", "cloud", "private_app", "private_victoria", "private_classic")
def check_custom_conf_replication(app, reporter):
    """
    Check that custom .conf files have a a matching conf_replication_include.<conf_file_name> value in server.conf,
    under the [shclustering] stanza, to ensure that configurations are synchronized across Search Head Clusters.
    """
    custom_configs = []
    for directory, filename, _ in app.iterate_files(types=[".conf"], basedir=["default", "local"]):
        if filename not in SPLUNK_DEFINED_CONFS:
            custom_configs.append(os.path.join(directory, filename))

    server_configs = []
    for directory in ["default", "local"]:
        if app.file_exists(directory, "server.conf"):
            server_conf = app.server_conf()
            server_conf.name = os.path.join(directory, "server.conf")
            server_configs.append(server_conf)

    for custom_config in custom_configs:
        custom_config_name = Path(custom_config).stem
        is_found = False
        for server_config in server_configs:
            shclustering_section = server_config.get_section("shclustering")
            for name, value, lineno in shclustering_section.items():
                if name == f"conf_replication_include.{custom_config_name}":
                    is_found = True
                    break
        if not is_found:
            reporter.warn(
                f"{custom_config} exists but conf_replication_include.{custom_config_name} "
                f"setting is not set in server.conf"
            )

    for server_config in server_configs:
        if server_config.has_section("shclustering"):
            shclustering_section = server_config.get_section("shclustering")
            for name, value, lineno in shclustering_section.items():
                if name.startswith("conf_replication_include."):
                    custom_conf = f"{name[len('conf_replication_include.'):]}"
                    if custom_conf not in [Path(c).stem for c in custom_configs]:
                        reporter.warn(
                            f"{name} setting in sever.conf "
                            f"but does not match custom config file. File: {server_config.name}. Line: {lineno}."
                        )
