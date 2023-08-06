"""
    Support for dict serialization
"""


def nest_flat_dict(flat_dict: dict, delimiter: str = "_"):
    """
    Convert a flat dictionary to a nested dictionary assuming that the keys are separated by a common delimiter
    """

    # Start an empty dictionary
    nested_dict = {}

    for key, value in flat_dict.items():
        # Point back to the root
        dict_pointer = nested_dict

        # For each sub_key after splitting, create a new level on the dictionary
        sub_key = key.split(delimiter)
        for index in range(len(sub_key)):
            # We just want to create an empty nested dict while we have sub_keys
            if (index + 1) < len(sub_key):
                # If the new level does not exist, create it
                if not dict_pointer.get(sub_key[index]):
                    dict_pointer[sub_key[index]] = {}

                # Move one level into the structure
                dict_pointer = dict_pointer[sub_key[index]]

        # Associate the value after all sub_keys have been processed
        dict_pointer[sub_key[index]] = value

    return nested_dict
