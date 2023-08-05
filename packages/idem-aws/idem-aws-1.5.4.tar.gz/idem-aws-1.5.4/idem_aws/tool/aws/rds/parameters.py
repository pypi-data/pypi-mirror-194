from typing import Any
from typing import Dict
from typing import List


async def modify_db_parameter_group(
    hub,
    ctx,
    resource_name,
    old_parameters: List[Dict[str, Any]],
    new_parameters: List[Dict[str, Any]],
):
    """
    Modifies the parameters of a DB parameter group

    Args:
        hub:
        ctx:
        resource_name: aws resource name
        old_parameters: list of old parameters
        new_parameters: list of new parameters

    Returns:
        {"result": True|False, "comment": "A message", "ret": None}

    """
    parameters_to_modify = []
    old_parameters_map = {
        parameter.get("ParameterName"): parameter for parameter in old_parameters or []
    }

    if new_parameters is not None:
        for parameter in new_parameters:
            if parameter.get("ParameterName") in old_parameters_map:
                if parameter.get("ParameterValue") != old_parameters_map.get(
                    parameter.get("ParameterName")
                ).get("ParameterValue"):
                    parameters_to_modify.append(parameter)

    result = dict(comment=(), result=True, ret=None)
    if not parameters_to_modify:
        return result
    else:
        if not ctx.get("test", False):
            update_parameters_ret = (
                await hub.exec.boto3.client.rds.modify_db_parameter_group(
                    ctx,
                    DBParameterGroupName=resource_name,
                    Parameters=parameters_to_modify,
                )
            )
            if not update_parameters_ret["result"]:
                result["comment"] = update_parameters_ret["comment"]
                result["result"] = False
                return result

        result["ret"] = {"parameters": parameters_to_modify}
        result["comment"] = result["comment"] + (
            f"Update parameters: Modified {[key.get('ParameterName') for key in parameters_to_modify]}",
        )
    return result


async def modify_db_cluster_parameter_group(
    hub,
    ctx,
    resource_name,
    old_parameters: List[Dict[str, Any]],
    new_parameters: List[Dict[str, Any]],
):
    """
    Modifies the parameters of a DB cluster parameter group

    Args:
        hub:
        ctx:
        resource_name: aws resource name
        old_parameters: list of old parameters
        new_parameters: list of new parameters

    Returns:
        {"result": True|False, "comment": "A message", "ret": None}

    """
    parameters_to_modify = []
    old_parameters_map = {
        parameter.get("ParameterName"): parameter for parameter in old_parameters or []
    }

    if new_parameters is not None:
        for parameter in new_parameters:
            if parameter.get("ParameterName") in old_parameters_map:
                if isinstance(parameter.get("ParameterValue"), int):
                    parameter["ParameterValue"] = str(parameter.get("ParameterValue"))
                if parameter.get("ParameterValue") != old_parameters_map.get(
                    parameter.get("ParameterName")
                ).get("ParameterValue"):
                    parameters_to_modify.append(parameter)

    result = dict(comment=(), result=True, ret=None)
    if not parameters_to_modify:
        return result
    else:
        if not ctx.get("test", False):
            update_parameters_ret = (
                await hub.exec.boto3.client.rds.modify_db_cluster_parameter_group(
                    ctx,
                    DBClusterParameterGroupName=resource_name,
                    Parameters=parameters_to_modify,
                )
            )
            if not update_parameters_ret["result"]:
                result["comment"] = update_parameters_ret["comment"]
                result["result"] = False
                return result

        result["ret"] = {"parameters": parameters_to_modify}
        result["comment"] = result["comment"] + (
            f"Update parameters: Modified {[key.get('ParameterName') for key in parameters_to_modify]}",
        )
    return result
