
from fastapi import APIRouter, HTTPException

from services.eligibility_service import get_eligibility_summary
from services.eligibility_ai_service import generate_eligibility_explanation

from schemas.eligibility_schema import EligibilitySummaryResponse

router = APIRouter(
    prefix="/api/eligibility",
    tags=["Eligibility Advisor"]
)


@router.get("/{user_id}", response_model=EligibilitySummaryResponse)
def get_user_eligibility(user_id: str):

    try:
        summary = get_eligibility_summary(user_id)

        if summary is None:
            raise HTTPException(
                status_code=404,
                detail="Eligibility results not found for this user"
            )

        return EligibilitySummaryResponse(
            user_id=user_id,
            **summary
        )

    except HTTPException:
        raise

    except Exception as error:
        print("Eligibility API Error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve eligibility results"
        )


@router.get("/{user_id}/explanation")
def get_eligibility_explanation(user_id: str):

    try:
        # Step 1: Fetch eligibility summary
        summary = get_eligibility_summary(user_id)

        if summary is None:
            raise HTTPException(
                status_code=404,
                detail="Eligibility results not found for this user"
            )

        # Step 2: Generate Gemini explanation
        explanation = generate_eligibility_explanation(summary)

        # Step 3: Return explanation
        return {
            "user_id": user_id,
            "explanation": explanation
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Eligibility Explanation API Error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate eligibility explanation"
        )
