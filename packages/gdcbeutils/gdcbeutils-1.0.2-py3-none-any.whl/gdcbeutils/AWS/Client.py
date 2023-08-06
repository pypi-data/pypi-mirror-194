from Helper.Environment import set_variable_to_env


def set_profile_region(profile: str = None, region: str = None):
    if profile:
        set_variable_to_env("AWS_PROFILE", profile)

    if region:
        set_variable_to_env("AWS_DEFAULT_REGION", region)
