# Build with AI Medellín 2026

**Taller de Confiabilidad y Observabilidad de Sistemas de IA**

Un taller práctico donde actúas como el nuevo Equipo de Confiabilidad de IA en Google Cloud. Tu misión: estabilizar y observar un sistema de respuesta a incidentes de IA con fallas intencionales, usando LangGraph, Gemini y Langfuse.

## Arquitectura

```
START → classify_incident
  ├──[low severity]──→ propose_mitigation ──→ generate_summary → END
  └──[med/high/critical]──→ analyze_logs → propose_mitigation
                                ↑                    │
                                └──[reanalysis loop]─┘
                                         │
                                    [done or max 3]
                                         ↓
                                  generate_summary → END
```

**Agentes:**
- **Clasificador de Incidentes** — Categoriza incidentes por tipo y severidad
- **Analizador de Logs** — Analiza trazas, spans y métricas para identificar causas raíz
- **Especialista en Mitigación** — Propone correcciones basadas en el análisis y runbooks
- **Resumen Ejecutivo** — Genera resúmenes listos para liderazgo

## Prerrequisitos

- Python 3.11+
- Docker & Docker Compose
- API key de Google Gemini ([obtén una aquí](https://aistudio.google.com/apikey))

## Inicio Rápido

```bash
# 1. Clonar y entrar al proyecto
git clone https://github.com/andresqb198/build-with-ai-2026.git
cd build-with-ai-2026

# 2. Configurar el entorno
cp .env.example .env
# Editar .env y agregar tu GOOGLE_API_KEY

# 3. Instalar dependencias e iniciar servicios
make setup
make start

# 4. Abrir Langfuse y crear una cuenta
# Visitar http://localhost:3000
# Crear un proyecto y copiar las API keys a tu archivo .env

# 5. Ejecutar el sistema
make run
```

## Variables de Entorno

| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| `GOOGLE_API_KEY` | Sí | API key de Gemini |
| `LANGFUSE_PUBLIC_KEY` | Sí* | Desde la configuración del proyecto en Langfuse |
| `LANGFUSE_SECRET_KEY` | Sí* | Desde la configuración del proyecto en Langfuse |
| `LANGFUSE_HOST` | No | Por defecto: `http://localhost:3000` |

*Requeridas para el rastreo. Configurar después del primer inicio de Langfuse.

## Configuración de Langfuse

1. Ejecutar `make start` para lanzar Langfuse
2. Abrir http://localhost:3000
3. Crear una cuenta (solo local, sin verificación de correo)
4. Crear un nuevo proyecto
5. Ir a **Settings → API Keys** y copiar las claves a tu archivo `.env`

## Comandos Disponibles

```bash
make help       # Mostrar todos los comandos
make setup      # Instalar dependencias
make start      # Iniciar Langfuse + validar entorno
make run        # Ejecutar el sistema de respuesta a incidentes
make stop       # Detener Langfuse
make reset      # Reiniciar todos los datos de Langfuse
make validate   # Verificar la configuración del entorno
```

## Estructura del Proyecto

```
app/
├── agents/         # Implementación de agentes (clasificador, analizador, mitigación, resumen)
├── graphs/         # Orquestación LangGraph y definición de estado
├── prompts/        # Plantillas de prompts para cada agente
├── tools/          # Funciones de herramientas (carga de datos, análisis de trazas, runbooks)
├── datasets/       # Datasets locales en JSON (incidentes, trazas, métricas)
├── telemetry/      # Integración con Langfuse
├── main.py         # Punto de entrada CLI
└── config.py       # Configuración del entorno
langfuse/
└── docker-compose.yml
scripts/
├── start.sh        # Script de inicio completo
├── reset.sh        # Reiniciar el estado del taller
└── validate_env.sh # Validación del entorno
```

## Taller

Selecciona un incidente del panel, ejecuta el pipeline de agentes y observa la ejecución en Langfuse. Busca:

- Trazas de ejecución y cronogramas de spans
- Uso de tokens por paso del agente
- Patrones de latencia a lo largo del pipeline
- Flujos de decisión y enrutamiento de agentes
- Anomalías en los datos de trazas

El sistema tiene problemas intencionales que debes descubrir a través de la observabilidad. ¡Buena depuración!
