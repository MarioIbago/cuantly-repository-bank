# Integración de bancos de IGL

Esta carpeta conserva la trazabilidad de los bancos públicos de práctica olímpica copiados desde [MarioIbago/IGLx0_CUANTLY_CERMAT](https://github.com/MarioIbago/IGLx0_CUANTLY_CERMAT). La importación se basó en el commit [`61486a2a31d239abccd145730073531e1b238477`](https://github.com/MarioIbago/IGLx0_CUANTLY_CERMAT/commit/61486a2a31d239abccd145730073531e1b238477).

## Colecciones

| Colección | Problemas | Contenido fuente |
| --- | ---: | --- |
| CUANTLY · Entrenamiento olímpico · Álgebra | 50 | `src/data/olimpico-algebra-extension.json` |
| CUANTLY · Entrenamiento olímpico · Geometría | 50 | `src/data/olimpico-geometry-extension.json` |
| CUANTLY · Entrenamiento olímpico · Teoría de números | 50 | `src/data/olimpico-number-theory-extension.json` |
| CUANTLY · Entrenamiento olímpico · Probabilidad | 50 | `src/data/olimpico-probability-extension.json` |
| CUANTLY · Diagnóstico adaptativo · L1-L5 | 39 | `src/data/cuantly_olimpiada_diagnostico.json` |
| OMM-Canguro · Banco de práctica · Problemas introductorios | 97 | `api/final_json/organized/all_complete.json` |

La última colección conserva `source_competition: "OMM"` como identifica el archivo IGL. El nombre visible `OMM-Canguro` facilita su navegación; el banco no asigna una edición anual. Todos los años son `null` con `year_status: "not_confirmed"` y evidencia.

## Conservación del contenido

Enunciados, opciones, respuestas y soluciones provienen de los JSON de IGL. Se conservan los análisis de distractores de Cuantly cuando existen; OMM no incluye análisis por distractor, así que su lista queda vacía. No se escribieron soluciones nuevas. El diagnóstico incluye cinco reactivos de razonamiento general sin clasificación de área porque el esquema público no ofrece esa categoría.

Las 25 escenas SVG de geometría reutilizan las definiciones de `src/components/GeometryDiagram.tsx` y se rasterizaron a PNG para el lector. Los 49 GIF estáticos vinculados por OMM se convirtieron a PNG: 36 figuras acompañan enunciados y 13 forman parte de las soluciones. El lector público muestra `solution_images` solo cuando se abre la solución. Los hashes, dimensiones y datos de origen de todas las figuras están embebidos en el banco.

Las fuentes son JSON sin paginación. Por eso `source_page` conserva el índice de registro empezando en 1 y `source_question_label` conserva el identificador original; no representa una página física.

## Validación y manifiesto

[`olympiad_import_2026-10-28.json`](olympiad_import_2026-10-28.json) registra hashes de los archivos fuente, conteos, conversión de figuras, rutas y notas del mapeo. El importador estructural confirma respuestas y soluciones presentes según los validadores de IGL y conserva sus valores. [`../FUSION/validate_bank.py`](../FUSION/validate_bank.py) comprueba estructura, opciones, clasificación, Base64, MIME, dimensiones, decodificación y hashes de figuras de enunciado y solución. La herramienta no prueba la corrección matemática, la fidelidad visual ni el renderizado de LaTeX.
