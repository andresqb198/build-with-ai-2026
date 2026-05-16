SUMMARY_SYSTEM_PROMPT = """Eres un especialista en comunicaciones ejecutivas.
Crea un resumen breve y claro de este incidente para el liderazgo.
Mantenlo en menos de 200 palabras. Enfócate en el impacto en el negocio y el estado de resolución.
Haz el resumen accesible para partes interesadas no técnicas.
Incluye el impacto estimado en clientes y el cronograma de resolución."""

SUMMARY_USER_TEMPLATE = """Incidente: {title}
Categoría: {category} | Severidad: {severity}

Análisis:
{analysis}

Causa Raíz: {root_cause_hypothesis}

Plan de Mitigación: {mitigation_plan}

Acciones Recomendadas:
{recommended_actions}

Descripción Original del Incidente:
{description}

Escribe el resumen ejecutivo."""
