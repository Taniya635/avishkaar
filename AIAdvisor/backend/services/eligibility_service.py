
from repositories.eligibility_repository import get_eligibility_results


def get_eligibility_summary(user_id: str):
    """
    Prepare an eligibility summary for a user.

    Counts are calculated using Python,
    not the AI model.
    """

    results = get_eligibility_results(user_id)

    if results is None:
        return None

    eligible = []
    ineligible = []
    pending = []

    for scheme in results:

        status = scheme.get("status")

        if status == "eligible":
            eligible.append(scheme)

        elif status == "ineligible":
            ineligible.append(scheme)

        elif status == "pending":
            pending.append(scheme)

    return {
        "total_schemes": len(results),
        "eligible_count": len(eligible),
        "ineligible_count": len(ineligible),
        "pending_count": len(pending),
        "eligible_schemes": eligible,
        "ineligible_schemes": ineligible,
        "pending_schemes": pending
    }
