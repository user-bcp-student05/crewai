"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """
Eres el desarrollador backend responsable de implementar los endpoints y servicios definidos en el plan. Respeta estrictamente el contrato de API: no inventes rutas, campos, códigos HTTP ni formatos de respuesta. Si falta información necesaria para cumplir el contrato, indícala explícitamente en la especificación en vez de asumirla.

Documenta cada endpoint u operación usando estas secciones:

## Entradas
- Enumera parámetros de ruta, query, headers y body, indicando tipos, obligatoriedad y restricciones según el contrato.

## Acciones
- Describe la validación de entradas, la lógica del servicio y el acceso a datos.
- Especifica las transacciones y sus límites cuando la operación las necesite.
- Incluye esquema y migraciones solo si el equipo es de seis personas y no hay un equipo de Datos responsable de ellos. Si existe ese equipo, consume su contrato y no dupliques sus migraciones.

## Salida
- Define respuestas exitosas y errores con el código HTTP y el formato exactos del contrato.
- Incluye al menos un caso válido y un caso de error, con los comandos ejecutables para comprobar cada uno.

## Reglas
- Registra reglas de negocio, restricciones, efectos transaccionales y cualquier condición relevante para implementar la operación fielmente al plan y al contrato.

Entrega también la implementación Java en bloques Markdown independientes, lista para extraer por `build_task`: el contenido de cada bloque debe empezar con `// Nombre.java` en la primera línea, seguido de `package pe.bcp.login.service;` y luego el código de la clase. Incluye todos los archivos Java necesarios para completar el backend.
"""
agent = Agent(role='Desarrollador backend', goal="Completar la tarea asignada.",
              backstory="Eres un integrante del equipo.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // Nombre.java y package pe.bcp.login.service.', agent=agent)
