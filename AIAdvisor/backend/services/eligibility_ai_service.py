
import json

from services.ai_service import client, GEMINI_MODELS


def generate_eligibility_explanation(eligibility_summary: dict):

    if client is None:
        return "AI service is not configured. Please try again later."

    # Convert eligibility results into JSON
    results_data = json.dumps(
        eligibility_summary,
        indent=2
    )

    prompt = f"""
    You are a helpful Government Scheme Eligibility Advisor.

    Your task is to explain the eligibility results provided below.

    IMPORTANT RULES:

    1. The eligibility engine has already determined the status.
    2. Never change or question the eligibility status.
    3. Never independently decide whether someone is eligible.
    4. Explain the recorded reasons in simple language.
    5. For pending schemes, explain that no final decision
       has been made yet.
    6. Never invent missing documents, eligibility rules,
       deadlines or government scheme information.
    7. Suggest next steps only when supported by the
       information provided.
    8. Keep the explanation clear and organized.

    Eligibility Results:

    {results_data}

    Explain the results using these sections:

    1. Overall Summary
    2. Eligible Schemes
    3. Ineligible Schemes
    4. Pending Schemes
    5. Recommended Next Steps
    """

    for model_name in GEMINI_MODELS:

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if response.text:
                return response.text

        except Exception as error:
            print(f"Gemini Error ({model_name}):", error)

            continue

    return "Sorry, I could not explain the eligibility results right now. Please try again later."
