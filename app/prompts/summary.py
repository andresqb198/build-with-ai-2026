SUMMARY_SYSTEM_PROMPT = """You are an executive communications specialist.
Create a brief, clear summary of this incident for leadership.
Keep it under 200 words. Focus on business impact and resolution status.
Make the summary accessible to non-technical stakeholders.
Include estimated customer impact and timeline for resolution."""

SUMMARY_USER_TEMPLATE = """Incident: {title}
Category: {category} | Severity: {severity}

Analysis:
{analysis}

Root Cause: {root_cause_hypothesis}

Mitigation Plan: {mitigation_plan}

Recommended Actions:
{recommended_actions}

Original Incident Description:
{description}

Write the executive summary."""
