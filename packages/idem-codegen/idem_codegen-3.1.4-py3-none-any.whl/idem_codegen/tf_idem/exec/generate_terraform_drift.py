"""
This file compares terraform and sls files and reports
any missing resources in idem or terraform.
"""
import base64
import os
import re

try:
    import colorama

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)
from jinja2 import Environment, FileSystemLoader

AWS_PRESENT_PATTERN = re.compile(r"aws\.[^${}]+\.present:")
K8_PRESENT_PATTERN = re.compile(r"k8s\.[^${}]+\.present:")
SPOTINIST_PRESENT_PATTERN = re.compile(r"spotinst\.[^${}]+\.present:")
HELM_PRESENT_PATTERN = re.compile(r"helm\.[^${}]+\.present:")


async def _get_params_data(hub, final_params_directory, common_path):
    final_params = {}
    for params_file in os.listdir(final_params_directory):
        if params_file.endswith(".sls") and params_file != "init.sls":
            params = hub.idem_codegen.tool.utils.parse_sls_data(
                os.path.join(final_params_directory, params_file)
            )
            final_params.update(params)
    if common_path and os.path.isfile(
        os.path.join(common_path, "common-variables.sls")
    ):
        common_params = hub.idem_codegen.tool.utils.parse_sls_data(
            os.path.join(common_path, "common-variables.sls")
        )
        final_params.update(common_params)

    return final_params


def _print_output(hub, final_output):
    strs = []
    endc = colorama.Fore.RESET
    total_files = len(final_output)
    no_drift_files = 0
    drift_files = 0
    missing_idem_files = 0
    for final_output_obj in final_output:
        result = final_output_obj["result"]
        changes = final_output_obj.get("drift")
        is_no_drift = False
        missing_file = False
        if result is True and changes:
            if changes == "1":
                tcolor = colorama.Fore.CYAN
                drift_files = drift_files + 1
            else:
                tcolor = colorama.Fore.RED
                missing_file = True
                missing_idem_files = missing_idem_files + 1
        elif result is True:
            no_drift_files = no_drift_files + 1
            tcolor = colorama.Fore.GREEN
            is_no_drift = True
        elif result is None:
            tcolor = colorama.Fore.LIGHTYELLOW_EX
        elif result is False:
            tcolor = colorama.Fore.LIGHTRED_EX
        else:
            tcolor = colorama.Fore.RESET

        if not (hub.OPT.idem_codegen.hide_output_if_no_drifts and is_no_drift):
            strs.append(f"\n")
            strs.append(f"{tcolor}--------{endc}")
            strs.append(f"{tcolor} path: {final_output_obj['path']}{endc}")
            strs.append(f"{tcolor} Result: {final_output_obj['result']}{endc}")
            strs.append(f"{tcolor} Comment: {final_output_obj['comment']}{endc}")
            if not missing_file:
                for drift_resource in final_output_obj["drifted_resources"]:
                    strs.append(f"{tcolor} Drifted Resources: ")
                    strs.append(
                        f"{tcolor}   type: {drift_resource['type']}  name: {drift_resource['name']} "
                    )

    strs.append(f"\n")
    strs.append(f" Total number of files compared: {total_files}\n")
    tcolor = colorama.Fore.GREEN
    strs.append(f"{tcolor} Number of files with no drifts: {no_drift_files}\n")
    tcolor = colorama.Fore.CYAN
    strs.append(f"{tcolor} Number of files with drift: {drift_files}\n")
    tcolor = colorama.Fore.RED

    for unmapped_resource in set(UNMAPPED_RESOURCES):
        strs.append(f"{tcolor} unmapped resource: {unmapped_resource}\n")

    print("\n".join(strs))


UNMAPPED_RESOURCES = []


def _get_drifted_resources(hub, terraform_resources, idem_resources, idem_file_data):
    drifted_resources = []
    if len(terraform_resources) != len(idem_resources):
        for tf_resource in terraform_resources:
            tf_resource_type = list(tf_resource.keys())[0]
            idem_resource_type = hub.tf_idem.tool.utils.tf_idem_resource_type_map.get(
                tf_resource_type
            )
            if idem_resource_type:
                if idem_resource_type in idem_resources:
                    idem_resources.pop(idem_resources.index(idem_resource_type))
                else:
                    tf_resource_val = list(tf_resource[tf_resource_type].keys())[0]
                    drifted_resources.append(
                        {"type": tf_resource_type, "name": tf_resource_val}
                    )
            else:
                UNMAPPED_RESOURCES.append(tf_resource_type)
                print(
                    f"terraform idem resource_type mapping not present {tf_resource_type}"
                )

    return drifted_resources


async def init(hub):
    input_dir_path = hub.OPT.idem_codegen.terraform_directory_path
    idem_files_location = hub.OPT.idem_codegen.output_directory_path
    os.chdir(hub.OPT.idem_codegen.terraform_directory_path)
    output_terraform = []

    final_output = []
    absolute_path_of_module_source = os.path.abspath(input_dir_path)
    for root, _, _ in os.walk(absolute_path_of_module_source):
        for f in os.listdir(root):
            if not f.endswith(".tf"):
                continue
            tf_file_path = os.path.join(root, f)
            _, tf_file_name = os.path.split(tf_file_path)
            tf_file_data = hub.tf_idem.tool.utils.parse_tf_data(tf_file_path, None)
            output_terraform.append(
                {
                    "path": f,
                    "full_path": tf_file_path,
                    "resources": tf_file_data.get("resource", {}),
                }
            )
    os.chdir(hub.OPT.idem_codegen.output_directory_path)
    for terraform_file in output_terraform:
        idem_file_path, final_params_directory = _get_idem_file_path(
            terraform_file, os.path.abspath(idem_files_location)
        )
        if terraform_file.get("resources"):
            terraform_file_path = terraform_file["full_path"]
            # final_params = await _get_params_data(hub, final_params_directory, idem_files_location)
            state_data = await _parse_jinja_file(
                hub, idem_file_path, terraform_file.get("resources")
            )
            if state_data["result"]:
                try:
                    parsed_state_data = state_data["state"]
                    if len(terraform_file["resources"]) != len(parsed_state_data):
                        final_output.append(
                            {
                                "result": True,
                                "path": terraform_file_path,
                                "drift": "1",
                                "drifted_resources": state_data["drift"],
                                "comment": f"There is a drift between terraform and Idem resources for "
                                f"terraform file {terraform_file_path}",
                            }
                        )
                    else:
                        final_output.append(
                            {
                                "result": True,
                                "path": terraform_file_path,
                                "comment": f"No drift exists for terraform file {terraform_file_path}",
                            }
                        )
                except Exception as exw:
                    print(f"I am in ecp {exw}")
                    final_output.append(
                        {
                            "result": True,
                            "path": terraform_file_path,
                            "comment": f"No drift exists for terraform file {terraform_file_path}",
                        }
                    )
            elif state_data["code"] == "-1":
                final_output.append(
                    {
                        "result": True,
                        "path": terraform_file_path,
                        "comment": f"{state_data['comment']}. Missing idem file for terraform file "
                        f"{terraform_file_path}",
                        "drift": "2",
                    }
                )
            elif state_data["code"] == "-2":
                final_output.append(
                    {
                        "result": False,
                        "path": terraform_file_path,
                        "comment": f"{state_data['comment']}.Unable to parse idem file for terraform file."
                        f"{terraform_file_path}. Please compare manually",
                    }
                )
    _print_output(hub, final_output)
    return final_output


def _get_idem_file_path(terraform_file, idem_files_location):
    final_sls_path = os.path.join(
        idem_files_location, "sls", terraform_file["path"].replace(".tf", ".sls")
    )
    final_params_directory = os.path.join(idem_files_location, "params")
    return final_sls_path, final_params_directory


async def _parse_jinja_file(hub, file_path, terraform_resources):
    try:
        if os.path.isfile(file_path):
            with open(file_path, "rb") as rfh:
                in_memory_file = rfh.read()
            try:
                params_removed = (
                    str(in_memory_file)
                    .replace("params[", "params.get(")
                    .replace("]", ")")
                )
                states = (
                    AWS_PRESENT_PATTERN.findall(params_removed)
                    + K8_PRESENT_PATTERN.findall(params_removed)
                    + SPOTINIST_PRESENT_PATTERN.findall(params_removed)
                    + HELM_PRESENT_PATTERN.findall(params_removed)
                )
                filtered_states = _filter_states(states)
                return {
                    "result": True,
                    "comment": "state data found",
                    "code": "1",
                    "state": filtered_states,
                    "drift": _get_drifted_resources(
                        hub, terraform_resources, filtered_states, params_removed
                    ),
                }
            except Exception as ex:
                msg = f"Error while parsing '{file_path}': {ex}"
                hub.log.debug(msg)
                ex.args = (msg,)
                return {
                    "result": False,
                    "comment": f"SLS file not found, {e}",
                    "code": "-2",
                }
        else:
            return {"result": False, "comment": "SLS file not found", "code": "-1"}
    except Exception as exce:
        print(exce)


def _base64encode(string):
    if string is None:
        return ""
    return base64.b64encode(string.encode()).decode()


def _base64decode(string):
    if string is None:
        return ""
    return base64.b64decode(string.encode()).decode()


def _filter_states(states):
    new_states = []
    for state in states:
        if "\\n" not in state:
            if len(state.split(".")) > 3:
                new_states.append(state.replace(".present:", ""))
    return new_states
