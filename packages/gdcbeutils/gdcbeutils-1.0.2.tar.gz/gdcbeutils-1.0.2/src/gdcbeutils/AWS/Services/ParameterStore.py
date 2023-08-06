from boto3 import client


def slash_directory_path_to_dict(ssm_tree: dict, lowest_level: int = 1) -> dict:
    """
    Convert aws returned list of parameters to a fully fledged python dict to more easily work with the variables

    @params:
        dict: ssm_tree -> dict with an AWS structured path ultimately pointing to the desired variable, with each directory separated by a forward slash
        lowest_level -> dictates, in the directory tree, the first level that will be integrated to the dictionary
    """

    unstructured_array = [
        {
            "nameArray": param_array["Name"].split(
                "/"
            ),  # creates an array with each directory as a level, and the last level being the parameter
            "value": param_array["Value"],
        }
        for param_array in ssm_tree["Parameters"]
    ]

    dict_obj = {}
    dict_pointer = dict_obj

    # For each path, go and assemble the dictionary
    for item in unstructured_array:
        dict_pointer = dict_obj  # points our "pointer" to the original base dict

        # for each directory, put the parameter where it belongs in the dict, hierarchycally speaking
        for level in range(lowest_level, len(item["nameArray"])):
            # Check wether this is the final level of a given path
            if not item["nameArray"][level] in dict_pointer.keys():
                dict_pointer[item["nameArray"][level]] = {}

                if level + 1 == len(item["nameArray"]):
                    dict_pointer[item["nameArray"][level]] = item["value"]

            dict_pointer = dict_pointer[item["nameArray"][level]]

    return dict_obj


def get_parameter_by_path(
    path: str = "/", recursive: bool = True, lowest_level: int = 2
) -> dict:
    """
    Uses AWS method to retrieve all the parameters specified in a subpath whose parent matches with the argument path provided. Note that subpaths must be delimited by a forward slash in this method

    @params
        string: path -> root directory from which to get parameters
        bool: Recursive ->
            True: will go as deep as the lowest subpath under the root folder.
            False: Will go only one level deep
        int: lowest_level -> Dictates the final dictionary root key/pair value and wether it will be nested under another dict
    """

    ssm = client("ssm")

    full_params = {}
    partial_params = ssm.get_parameters_by_path(Path=path, Recursive=recursive)
    full_params["Parameters"] = partial_params["Parameters"]

    while "NextToken" in partial_params.keys():
        partial_params = ssm.get_parameters_by_path(
            Path=path, Recursive=recursive, NextToken=partialParams["NextToken"]
        )
        full_params["Parameters"].extend(partial_params["Parameters"])

    dict_params = slash_directory_path_to_dict(full_params, lowest_level=lowest_level)
    return dict_params
