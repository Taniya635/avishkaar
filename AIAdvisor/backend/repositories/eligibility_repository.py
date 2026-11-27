
from mock_data.eligibility_results import MOCK_ELIGIBILITY_RESULTS


def get_eligibility_results(user_id: str):
    """
    Retrieve eligibility results for a user.

    Currently uses mock data.
    Later, this will connect to the actual
    eligibility engine developed by the team.
    """

    user_data = MOCK_ELIGIBILITY_RESULTS.get(user_id)

    if user_data is None:
        return None

    return user_data.get("results", [])
