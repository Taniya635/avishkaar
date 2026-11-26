
from fastapi import APIRouter, HTTPException

from schemas.chat_schema import ChatRequest, ChatResponse
from services.context_service import get_user_context
from services.ai_service import generate_ai_response

router = APIRouter(prefix="/api/chat", tags=["AI Advisor"])


# Suggested questions for guest users
GUEST_SUGGESTIONS = [
    "What government schemes are available for students?",
    "What schemes support women entrepreneurs?",
    "What government benefits are available for farmers?",
    "How can I apply for government schemes?",
    "What documents are generally required for government schemes?"
]


def get_personalized_suggestions(user_context: dict):
    occupation = user_context.get("occupation", "").lower()
    state = user_context.get("state", "")

    suggestions = []

    if occupation == "student":
        suggestions = [
            "Which government schemes are available for students?",
            "What educational financial assistance schemes can I explore?",
            "Are there any skill development schemes for me?",
            "What documents are generally required for student schemes?",
            "What benefits can I explore in my state?"
        ]

    elif occupation == "farmer":
        suggestions = [
            "What government schemes are available for farmers?",
            "What agricultural assistance can I explore?",
            "Are there any farming equipment support schemes?",
            "What documents are generally required for farmer schemes?",
            "What agricultural benefits can I explore in my state?"
        ]

    else:
        suggestions = [
            "Which government schemes may be relevant to me?",
            "What financial assistance schemes can I explore?",
            "Are there any skill development schemes?",
            "What documents are generally required for government schemes?",
            "What government benefits can I explore?"
        ]

    # Add the user's state to suggestions where relevant
    if state:
        suggestions[0] = suggestions[0].replace(
            "students?",
            f"students in {state}?"
        ) if occupation == "student" else suggestions[0]

    return suggestions


@router.get("/suggestions")
def get_suggestions(user_id: str = None):

    try:
        # Guest user
        if user_id is None:
            return {
                "user_type": "guest",
                "suggestions": GUEST_SUGGESTIONS
            }

        # Logged-in demo user
        user_context = get_user_context(user_id)

        if user_context is None:
            raise HTTPException(
                status_code=404,
                detail="User profile not found"
            )

        return {
            "user_type": "logged_in",
            "suggestions": get_personalized_suggestions(user_context)
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Suggestion API Error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to load suggestions."
        )


@router.post("/", response_model=ChatResponse)
def chat_with_ai(request: ChatRequest):

    try:
        # Guest user: no profile context
        if request.user_id is None:
            user_context = {}

        # Logged-in demo user: fetch profile
        else:
            user_context = get_user_context(request.user_id)

            if user_context is None:
                raise HTTPException(
                    status_code=404,
                    detail="User profile not found"
                )

        conversation_history = request.conversation_history

        # Generate AI response with conversation history
        ai_response = generate_ai_response(
            user_message=request.message,
            user_context=user_context,
            conversation_history=conversation_history
        )

        return ChatResponse(
            user_id=request.user_id,
            message=request.message,
            response=ai_response
        )

    except HTTPException:
        raise

    except Exception as error:
        print("Chat API Error:", error)

        raise HTTPException(
            status_code=500,
            detail="Something went wrong. Please try again later."
        )
