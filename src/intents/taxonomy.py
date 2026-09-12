from typing import List, Dict, Any

INTENT_TAXONOMY = [
    {
        "intent_name": "Ride & Payment Issues",
        "description": "Issues concerning trip charges, unauthorized transactions, payment method failures, and cancellation fees.",
        "example_messages": ["My card was charged for a trip I never took.", "Why was I charged a cancellation fee?"],
        "example_count": 50,
        "rationale": "High frequency support category dealing with financial transactions and charge disputes."
    },
    {
        "intent_name": "Fare & Price Problems",
        "description": "Disputes over surge pricing, estimated vs. final fares, and route overcharges.",
        "example_messages": ["The fare was much higher than the upfront estimate.", "Why did my trip cost so much more due to surge?"],
        "example_count": 50,
        "rationale": "Critical for rider trust regarding pricing transparency."
    },
    {
        "intent_name": "Refund Issues",
        "description": "Inquiries and follow-ups regarding status and processing of requested refunds.",
        "example_messages": ["When will I receive my refund for the cancelled ride?", "I requested a refund three days ago."],
        "example_count": 50,
        "rationale": "Common post-resolution support request requiring clear financial tracking."
    },
    {
        "intent_name": "Account & Login Problems",
        "description": "Troubleshooting account access, locked profiles, phone number updates, and password resets.",
        "example_messages": ["I cannot log into my account because my phone number changed.", "My account was locked."],
        "example_count": 50,
        "rationale": "Essential security and access gateway category."
    },
    {
        "intent_name": "Driver-Related Issues",
        "description": "Complaints regarding driver conduct, navigation errors, unprofessional behavior, or cash payment requests.",
        "example_messages": ["My driver was extremely rude and unsafe during the trip.", "Driver asked me to pay in cash."],
        "example_count": 50,
        "rationale": "Directly impacts platform safety and service quality standards."
    },
    {
        "intent_name": "Trip Cancellation",
        "description": "Disputes surrounding rider or driver cancellations, cancellation fees, and ride reliability.",
        "example_messages": ["Driver cancelled my ride after waiting 15 minutes.", "Why am I getting charged when I cancelled immediately?"],
        "example_count": 50,
        "rationale": "High friction operational issue affecting ride completion."
    },
    {
        "intent_name": "Lost Items",
        "description": "Assistance with recovering personal items left behind in vehicles.",
        "example_messages": ["I left my phone in the back seat of the Uber car.", "How do I contact my driver about a lost item?"],
        "example_count": 50,
        "rationale": "Unique physical world customer support workflow requiring driver coordination."
    },
    {
        "intent_name": "Promotion & Discount Problems",
        "description": "Troubleshooting promo codes, expired discounts, or unapplied referral credits.",
        "example_messages": ["My promo code did not apply to my trip fare.", "Discount code says expired."],
        "example_count": 50,
        "rationale": "Marketing and promotional incentive support."
    },
    {
        "intent_name": "App & Technical Problems",
        "description": "Technical bugs, app crashes, map loading failures, and GPS connectivity errors.",
        "example_messages": ["The app crashes every time I try to request a ride.", "Map loading error 503."],
        "example_count": 50,
        "rationale": "Platform technical stability and UX issue resolution."
    },
    {
        "intent_name": "Safety-Related Issues",
        "description": "High-priority complaints regarding accidents, harassment, threats, or urgent safety emergencies.",
        "example_messages": ["I was involved in an accident during my Uber trip.", "Threatening behavior from individual."],
        "example_count": 50,
        "rationale": "Zero-tolerance high-risk category requiring immediate human escalation and priority triage."
    }
]
