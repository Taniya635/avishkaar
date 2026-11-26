from repositories.profile_repository import get_profile_by_id


def get_user_context(user_id: str):
    """
    Fetch user profile and prepare it as context
    for the AI Advisor.
    """

    profile = get_profile_by_id(user_id)

    if profile is None:
        return None

    context = {
        "name": profile["full_name"],
        "age": profile["age"],
        "gender": profile["gender"],
        "state": profile["state"],
        "district": profile["district"],
        "education": profile["education"],
        "occupation": profile["occupation"],
        "annual_family_income": profile["annual_family_income"],
        "category": profile["category"],
        "is_person_with_disability": profile["is_person_with_disability"],
        "is_farmer": profile["is_farmer"],
        "marital_status": profile["marital_status"]
    }

    return context