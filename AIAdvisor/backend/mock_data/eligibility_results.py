
MOCK_ELIGIBILITY_RESULTS = {
    "user_001": {
        "results": [
            {
                "scheme_id": "scheme_001",
                "scheme_name": "Demo Student Support Scheme",
                "status": "eligible",
                "reasons": [
                    "User meets the required education criteria.",
                    "User meets the income criteria."
                ]
            },
            {
                "scheme_id": "scheme_002",
                "scheme_name": "Demo Skill Development Scheme",
                "status": "ineligible",
                "reasons": [
                    "User does not meet the required age criteria."
                ]
            },
            {
                "scheme_id": "scheme_003",
                "scheme_name": "Demo Financial Assistance Scheme",
                "status": "pending",
                "reasons": [
                    "Required information is not yet available."
                ]
            }
        ]
    }
}
