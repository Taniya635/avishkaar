from mock_data.profiles import MOCK_PROFILES


def get_profile_by_id(user_id: str):
    """
    Retrieve a user profile using the user's ID.

    Currently uses mock data.
    Later, this function will retrieve data from PostgreSQL.
    """

    profile = MOCK_PROFILES.get(user_id)

    if profile is None:
        return None

    return profile