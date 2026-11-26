
import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from repositories.scheme_repository import get_all_schemes

# Load environment variables
load_dotenv()

# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini models in priority order
GEMINI_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-3-flash-preview",
    "gemini-3.5-flash"
]

# Initialize Gemini client
client = None

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=types.HttpOptions(
            timeout=120000
        )
    )


def generate_ai_response(
    user_message: str,
    user_context: dict,
    conversation_history: list[dict] | None = None
):
    """
    Generate a government scheme-focused AI response
    using Gemini, profile context, scheme data and recent
    conversation history.
    """

    if client is None:
        return "AI service is not configured. Please add your Gemini API key."

    # Get available schemes
    schemes = get_all_schemes()

    # Convert profile data into JSON
    context_data = json.dumps(
        user_context or {},
        indent=2
    )

    # Convert scheme data into JSON
    schemes_data = json.dumps(
        schemes,
        indent=2
    )

    # Keep only the latest six valid conversation messages
    recent_history = []

    for item in (conversation_history or [])[-6:]:

        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if (
            role in ["user", "assistant"]
            and isinstance(content, str)
            and content.strip()
        ):
            recent_history.append({
                "role": role,
                "content": content.strip()[:2000]
            })

    # Convert conversation history into JSON
    history_data = json.dumps(
        recent_history,
        indent=2
    )

    # Create AI prompt
    prompt = f"""
    You are a helpful Government Scheme Advisor for a platform
    focused on helping people discover and understand government schemes.

    Your purpose is to:
    - Help users discover relevant government schemes.
    - Explain scheme information in simple language.
    - Guide users towards official government sources.
    - Explain available eligibility results when provided by the
      eligibility engine.

    USER PROFILE:
    {context_data}

    AVAILABLE SCHEME DATA:
    {schemes_data}

    RECENT CONVERSATION HISTORY:
    {history_data}

    CURRENT USER QUESTION:
    {user_message}

    IMPORTANT RULES:

    1. The available dataset contains 38 mock scheme records
       prepared for development and testing. The records use
       scheme names and references collected from official
       Maharashtra government and scheme portals.

    2. Treat the dataset as reference data for development.
       Do not claim that its information is currently verified,
       exhaustive, or proof that applications are open.

    3. Use the available scheme data when answering questions
       about specific schemes.

    4. The scheme records contain these fields:
       - scheme_id
       - scheme_name
       - category
       - implementing_department
       - short_description
       - state
       - listing_status
       - application_status
       - eligibility
       - application_url
       - source_refs

    5. Do not invent scheme benefits, eligibility criteria,
       income limits, required documents, deadlines, financial
       assistance amounts or application procedures.

    6. The eligibility field may contain only a reference to
       current scheme guidelines or a Government Resolution.
       If exact eligibility details are unavailable, explain that
       the user must check the current official guidelines.


    6A. STRICT SOURCE RULE:
        Only describe scheme information using facts explicitly
        available in the provided scheme record.

        Use short_description for the scheme's description.
        Do not generate additional benefits, purposes,
        financial assistance details or eligibility conditions
        from general knowledge.

        If a detail is missing from the record, say:
        "This information is not available in our current
        scheme records. Please check the official guidelines."

    6B. Do not assume that a scheme is suitable for a user
        merely because they belong to a broad group such as
        students, farmers or women.

        If specific eligibility information is missing,
        recommend checking the official guidelines rather
        than suggesting that the user qualifies.

    6C. Clearly distinguish between:
        - Scheme information available in the mock dataset.
        - Information that requires official verification.
        - Eligibility confirmed by the eligibility engine.


    6D. EXACT SCHEME INFORMATION:

        When recommending a scheme, reproduce its
        short_description as provided in the dataset.

        Do not expand, embellish, or add claims to the description.

        Always use the exact scheme_name, scheme_id and
        application_url from the corresponding record.

        Do not use the same application URL for every scheme
        unless that is the URL stored in its record.

        If a user asks for details not available in the record,
        clearly state that those details require official verification.



    7. A scheme being listed in the dataset does NOT mean
       applications are currently open.

       If application_status says verify_on_official_portal,
       clearly tell the user to check the official portal for
       current application availability.

    8. Use the application_url provided in the dataset when
       directing users to a scheme's official application portal.
       Never invent or modify application links.

    9. If the user asks for scheme recommendations, suggest
       up to 4-5 relevant schemes from the available dataset.

       If fewer schemes are relevant, suggest only those schemes.
       Do not recommend unrelated schemes just to reach five.

    10. Use the user's profile when it is available and relevant.
        Do not unnecessarily repeat or expose personal profile
        information in your response.

    11. For guest users, answer without personal profile information.

    12. Never independently decide whether a user is eligible
        for a scheme. Only the eligibility engine determines
        eligibility.

    13. If eligibility results are provided, explain their
        existing status and reasons in simple language.
        Never change or override the eligibility engine's result.

    14. If requested information is unavailable in the dataset,
        clearly say that it is not available in the current
        scheme records and direct the user to the official source.

    15. For general questions outside government schemes,
        provide a brief helpful answer while keeping your main
        purpose focused on government scheme guidance.

    16. Use conversation history to understand follow-up questions
        and references such as "the first one", "that scheme",
        or "tell me more".

    17. Conversation history is context, not verified scheme data.
        Always prioritize the available scheme records for
        scheme-specific facts.

    18. Give priority to the CURRENT USER QUESTION.
        Do not unnecessarily repeat previous answers.

    RESPONSE STYLE:
    - Use simple, clear and friendly language.
    - Use headings when helpful.
    - Prefer short paragraphs and bullet points.
    - Mention scheme names clearly.
    - Include official links when relevant.
    - Avoid unnecessarily lengthy answers.

    Now answer the user's current question.
    """

    # Try each Gemini model one by one
    for model_name in GEMINI_MODELS:

        try:
            print(f"\nTrying Gemini model: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if response.text:
                print(f"SUCCESS: Response generated using {model_name}")
                return response.text

            print(f"Empty response from {model_name}. Trying next model...")

        except Exception as error:

            print(f"FAILED: {model_name}")
            print("Gemini Error:", repr(error))

            status_code = getattr(error, "code", None)

            if status_code is None:
                status_code = getattr(error, "status_code", None)

            error_text = str(error).upper()

            # Errors for which we should try another model
            retryable_status_codes = [404, 429, 500, 502, 503, 504]

            if (
                status_code in retryable_status_codes
                or any(
                    code in error_text
                    for code in [
                        "404",
                        "429",
                        "500",
                        "502",
                        "503",
                        "504",
                        "UNAVAILABLE",
                        "DEADLINE_EXCEEDED",
                        "RESOURCE_EXHAUSTED"
                    ]
                )
            ):
                print("Switching to the next Gemini model...")
                continue

            # Stop for other errors
            print("Non-retryable error. Stopping model fallback.")

            return (
                "The AI service encountered an error. "
                "Please try again later."
            )

    # All models failed
    print("\nAll Gemini models failed.")

    return (
        "All Gemini models are currently unavailable. "
        "Please try again later."
    )
