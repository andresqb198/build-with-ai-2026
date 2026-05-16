def search_traces(traces: list[dict], pattern: str) -> list[dict]:
    """Search traces for spans matching a pattern by name or status."""
    results = []
    pattern_lower = pattern.lower()
    for trace in traces:
        for span in trace.get("spans", []):
            if (
                pattern_lower in span.get("name", "").lower()
                or pattern_lower in span.get("status", "").lower()
                or pattern_lower in str(span.get("metadata", {})).lower()
            ):
                results.append(
                    {"trace_id": trace["trace_id"], "span": span}
                )
    return results


def compute_trace_statistics(traces: list[dict]) -> dict:
    """Compute aggregate statistics across all spans in the traces."""
    total_spans = 0
    total_duration_ms = 0
    total_input_tokens = 0
    total_output_tokens = 0
    error_count = 0
    span_names: list[str] = []

    for trace in traces:
        for span in trace.get("spans", []):
            total_spans += 1
            total_duration_ms += span.get("duration_ms", 0)
            total_input_tokens += span.get("input_tokens", 0)
            total_output_tokens += span.get("output_tokens", 0)
            if span.get("status") == "error":
                error_count += 1
            span_names.append(span.get("name", "unknown"))

    return {
        "total_spans": total_spans,
        "total_duration_ms": total_duration_ms,
        "avg_duration_ms": round(total_duration_ms / total_spans, 2) if total_spans else 0,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "error_count": error_count,
        "error_rate": round(error_count / total_spans, 4) if total_spans else 0,
        "span_names": span_names,
    }


def detect_duplicate_spans(traces: list[dict]) -> list[dict]:
    """Find spans that appear to be duplicate calls (same name, similar inputs)."""
    duplicates = []
    seen: dict[str, list[dict]] = {}

    for trace in traces:
        for span in trace.get("spans", []):
            name = span.get("name", "")
            key = f"{trace['trace_id']}:{name}"
            if key not in seen:
                seen[key] = []
            seen[key].append(span)

    for key, spans in seen.items():
        if len(spans) > 1:
            trace_id = key.split(":")[0]
            duplicates.append(
                {
                    "trace_id": trace_id,
                    "span_name": spans[0]["name"],
                    "occurrence_count": len(spans),
                    "total_wasted_duration_ms": sum(
                        s.get("duration_ms", 0) for s in spans[1:]
                    ),
                    "total_wasted_tokens": sum(
                        s.get("input_tokens", 0) + s.get("output_tokens", 0)
                        for s in spans[1:]
                    ),
                }
            )

    return duplicates
