RUNBOOKS = {
    "hallucination": (
        "1. Habilitar validación de salida contra datos de origen\n"
        "2. Agregar generación aumentada por recuperación (RAG) con requisitos de citas\n"
        "3. Implementar puntuación de confianza con fallback basado en umbrales\n"
        "4. Agregar revisión humana en el bucle para salidas de baja confianza\n"
        "5. Registrar todos los identificadores generados y cruzarlos con la base de datos"
    ),
    "latency": (
        "1. Perfilar la ejecución del agente para identificar spans cuello de botella\n"
        "2. Verificar llamadas redundantes o secuenciales que podrían paralelizarse\n"
        "3. Implementar tiempo de espera de solicitudes con degradación elegante\n"
        "4. Agregar caché para llamadas repetidas de embedding o recuperación\n"
        "5. Considerar cambiar a un modelo más ligero en pasos intermedios no críticos"
    ),
    "security": (
        "1. Implementar sanitización de entradas y detección de inyección de prompts\n"
        "2. Fortalecer el prompt del sistema con instrucciones explícitas de ignorar sobreescrituras\n"
        "3. Separar el contenido del usuario de las instrucciones del sistema con tokens delimitadores\n"
        "4. Habilitar filtrado de salida para respuestas que violan políticas\n"
        "5. Agregar registro de auditoría para todas las decisiones relacionadas con cumplimiento"
    ),
    "cost": (
        "1. Auditar el uso de tokens por paso del agente para identificar desperdicios\n"
        "2. Implementar presupuestos de tokens por solicitud con terminación anticipada\n"
        "3. Eliminar pasos redundantes de reformateo o cadena de pensamiento\n"
        "4. Cachear datos solicitados frecuentemente para evitar reprocesamiento\n"
        "5. Configurar alertas de costo y estrangulamiento automático en umbrales de gasto"
    ),
    "tool_misuse": (
        "1. Agregar lógica de deduplicación antes de la ejecución de herramientas\n"
        "2. Implementar caché de llamadas de herramientas con TTL para entradas idénticas\n"
        "3. Establecer un máximo de invocaciones de herramientas por solicitud\n"
        "4. Agregar circuit breaker para llamadas idénticas repetidas\n"
        "5. Revisar el prompt del agente para reducir bucles de verificación innecesarios"
    ),
    "infrastructure": (
        "1. Implementar lógica de reintentos con retroceso exponencial\n"
        "2. Agregar circuit breaker para servicios externos con fallas\n"
        "3. Configurar fuentes de datos de respaldo o respuestas en caché\n"
        "4. Configurar verificaciones de salud y alertas para servicios dependientes\n"
        "5. Asegurarse de que el agente comunique contexto parcial a los usuarios"
    ),
    "unknown": (
        "1. Recopilar datos de diagnóstico adicionales y trazas\n"
        "2. Escalar al equipo de ingeniería de guardia\n"
        "3. Habilitar registro detallado para el servicio afectado\n"
        "4. Revisar despliegues recientes y cambios de configuración\n"
        "5. Abrir una sala de guerra si se confirma impacto en clientes"
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
