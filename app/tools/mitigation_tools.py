RUNBOOKS = {
    "hallucination": (
        "1. Enable output validation against source data\n"
        "2. Add retrieval-augmented generation (RAG) with citation requirements\n"
        "3. Implement confidence scoring with threshold-based fallback\n"
        "4. Add human-in-the-loop review for low-confidence outputs\n"
        "5. Log all generated identifiers and cross-reference with database"
    ),
    "latency": (
        "1. Profile the agent execution to identify bottleneck spans\n"
        "2. Check for redundant or sequential calls that could be parallelized\n"
        "3. Implement request timeout with graceful degradation\n"
        "4. Add caching for repeated embedding or retrieval calls\n"
        "5. Consider model downgrade for non-critical intermediate steps"
    ),
    "security": (
        "1. Implement input sanitization and prompt injection detection\n"
        "2. Add system prompt hardening with explicit ignore-override instructions\n"
        "3. Separate user content from system instructions with delimiter tokens\n"
        "4. Enable output filtering for policy-violating responses\n"
        "5. Add audit logging for all compliance-related decisions"
    ),
    "cost": (
        "1. Audit token usage per agent step to identify waste\n"
        "2. Implement token budgets per request with early termination\n"
        "3. Remove redundant reformatting or chain-of-thought steps\n"
        "4. Cache frequently requested data to avoid re-processing\n"
        "5. Set up cost alerts and automatic throttling at spend thresholds"
    ),
    "tool_misuse": (
        "1. Add deduplication logic before tool execution\n"
        "2. Implement tool call caching with TTL for identical inputs\n"
        "3. Set maximum tool invocations per request\n"
        "4. Add circuit breaker for repeated identical calls\n"
        "5. Review agent prompt to reduce unnecessary verification loops"
    ),
    "infrastructure": (
        "1. Implement retry logic with exponential backoff\n"
        "2. Add circuit breaker for failing external services\n"
        "3. Configure fallback data sources or cached responses\n"
        "4. Set up health checks and alerting for dependent services\n"
        "5. Ensure the agent communicates partial context to users"
    ),
    "unknown": (
        "1. Collect additional diagnostic data and traces\n"
        "2. Escalate to the on-call engineering team\n"
        "3. Enable verbose logging for the affected service\n"
        "4. Review recent deployments and configuration changes\n"
        "5. Open a war room if customer impact is confirmed"
    ),
}

CIRCUIT_BREAKER_STATUS = {
    "customer-support-agent": {"status": "closed", "failure_count": 2, "last_failure": "2026-05-14T08:20:00Z"},
    "doc-summarizer-agent": {"status": "half-open", "failure_count": 15, "last_failure": "2026-05-13T14:09:00Z"},
    "compliance-review-agent": {"status": "closed", "failure_count": 0, "last_failure": None},
    "research-assistant-agent": {"status": "closed", "failure_count": 1, "last_failure": "2026-05-12T19:28:00Z"},
    "data-retrieval-agent": {"status": "open", "failure_count": 42, "last_failure": "2026-05-13T11:14:00Z"},
    "knowledge-base-agent": {"status": "half-open", "failure_count": 28, "last_failure": "2026-05-14T05:58:00Z"},
    "code-review-agent": {"status": "closed", "failure_count": 3, "last_failure": "2026-05-13T16:42:00Z"},
}


def get_runbook(category: str) -> str:
    """Return the standard runbook for a given incident category."""
    return RUNBOOKS.get(category, RUNBOOKS["unknown"])


def check_circuit_breaker_status(service: str) -> dict:
    """Check the circuit breaker status for a given service."""
    return CIRCUIT_BREAKER_STATUS.get(
        service,
        {"status": "unknown", "failure_count": 0, "last_failure": None},
    )
