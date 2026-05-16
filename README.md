# Build with AI Medellín 2026

https://docs.google.com/presentation/d/1iftaDMtfRWuMSKFUjyaXYRzzkfLwLiFTUa2Wm_7RAGA/edit?usp=sharing

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
                                    [done o max 3]
                                         ↓
                                  generate_summary → END
```

**Agentes:**
- **Clasificador de Incidentes** — Categoriza incidentes por tipo y severidad
- **Analizador de Logs** — Analiza trazas, spans y métricas para identificar causas raíz
- **Especialista en Mitigación** — Propone correcciones basadas en el análisis y runbooks
- **Resumen Ejecutivo** — Genera resúmenes listos para liderazgo

---

## Prerrequisitos

- Python 3.10+
- Docker con Docker Compose ([Docker Desktop](https://docs.docker.com/get-docker/) en Windows/macOS)
- API key de Google Gemini ([obtén una aquí](https://aistudio.google.com/apikey))

---

## Inicio Rápido

Los comandos son idénticos en Linux, macOS y Windows.

### 1. Clonar el repositorio

```bash
git clone https://github.com/andresqb198/build-with-ai-2026.git
cd build-with-ai-2026
```

### 2. Instalar dependencias y crear `.env`

```bash
python run.py setup
```

Esto crea el archivo `.env` desde `.env.example` e instala las dependencias de Python.
Abre `.env` y agrega tu `GOOGLE_API_KEY`.

### 3. Iniciar Langfuse

```bash
python run.py start
```

Levanta todos los contenedores (PostgreSQL, ClickHouse, Redis, MinIO, Langfuse web + worker).

### 4. Crear cuenta y API keys en Langfuse

1. Abre [http://localhost:3000](http://localhost:3000) en tu navegador
2. Crea una cuenta (solo local, sin verificación de correo)
3. Crea un nuevo proyecto
4. Ve a **Settings → API Keys** y copia las claves a tu archivo `.env`:

```
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_BASE_URL="http://localhost:3000"
```

### 5. Ejecutar el sistema

```bash
python run.py run
```

Selecciona un incidente del panel y observa el pipeline de agentes en acción.

---

## Variables de Entorno

| Variable | Requerida | Descripción |
|---|---|---|
| `GOOGLE_API_KEY` | Sí | API key de Gemini |
| `LANGFUSE_PUBLIC_KEY` | Sí* | Desde Settings → API Keys en Langfuse |
| `LANGFUSE_SECRET_KEY` | Sí* | Desde Settings → API Keys en Langfuse |
| `LANGFUSE_BASE_URL` | No | Por defecto: `http://localhost:3000` |

*Requeridas para el rastreo. Configúralas después del primer inicio de Langfuse (paso 4).

---

## Comandos Disponibles

```bash
python run.py help      # Mostrar todos los comandos
python run.py setup     # Instalar dependencias y crear .env
python run.py start     # Iniciar Langfuse + validar entorno
python run.py run       # Ejecutar el sistema de respuesta a incidentes
python run.py stop      # Detener Langfuse
python run.py reset     # Reiniciar todos los datos de Langfuse
python run.py validate  # Verificar la configuración del entorno
```

---

## Estructura del Proyecto

```
run.py                  # CLI cross-platform (reemplaza make en Windows/macOS/Linux)
app/
├── agents/             # Agentes: clasificador, analizador, mitigación, resumen
├── graphs/             # Orquestación LangGraph y definición de estado
├── prompts/            # Plantillas de prompts para cada agente
├── tools/              # Herramientas: carga de datos, análisis de trazas, runbooks
├── datasets/           # Datasets locales en JSON (incidentes, trazas, métricas)
├── telemetry/          # Integración con Langfuse
├── main.py             # Punto de entrada CLI
└── config.py           # Configuración del entorno
observability/
├── docker-compose.yml  # Stack completo: Postgres, ClickHouse, Redis, MinIO, Langfuse
└── clickhouse-config.xml
```

---

## Infraestructura de Observabilidad

El stack levantado por `python run.py start` incluye:

| Servicio | Puerto | Rol |
|---|---|---|
| Langfuse UI | 3000 | Panel de trazas y métricas |
| Langfuse Worker | — | Procesa eventos de Redis → ClickHouse |
| PostgreSQL | 5432 | Metadatos de proyectos y usuarios |
| ClickHouse | 8123 / 9000 | Almacenamiento de trazas y spans |
| Redis | 6379 | Cola de eventos de ingesta |
| MinIO | 9002 / 9001 | Almacenamiento de eventos y media (S3-compatible) |

---

## El Taller

Selecciona un incidente del panel, ejecuta el pipeline de agentes y observa la ejecución en Langfuse. Busca:

- Trazas de ejecución y cronogramas de spans
- Uso de tokens por paso del agente
- Patrones de latencia a lo largo del pipeline
- Flujos de decisión y enrutamiento de agentes
- Anomalías en los datos de trazas

El sistema tiene problemas intencionales que debes descubrir a través de la observabilidad. ¡Buena depuración!
