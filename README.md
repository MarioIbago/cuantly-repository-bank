# Cuantly Problems Bank

Banco de problemas y exámenes de Cuantly migrado desde Google Drive.

Fuente original:

`Cuantly Problems Bank`  
https://drive.google.com/drive/folders/1Xssooej0URvwWicw1GCeVMZyboKXUpiD

## Estructura importada

```text
01_RAW_PDFs/
└── GAU55/
    ├── 2023/Estatal/
    └── 2024/Estatal/

02_JSON_EXAMS/
└── GAU55/
    ├── 2023/Estatal/
    └── 2024/Estatal/

03_SCHEMA_AND_REPORTS/
├── GAU55/
│   ├── 2023/Estatal/
│   └── 2024/Estatal/
├── FUSION/
├── IGL/
└── GAU55_2023_2024_media_structural_audit.json

04_REFERENCE_SOURCES/
└── GAU55/

05_CLASSIFIED_EXAMS/
├── GAU55/
│   ├── 2023/Estatal/
│   └── 2024/Estatal/
├── CUANTLY/Sin fecha/
│   ├── Entrenamiento olímpico/{Álgebra, Geometría, Teoría de números, Probabilidad}/
│   └── Diagnóstico adaptativo/L1-L5/
└── OMM-Canguro/Sin fecha/Banco de práctica/Problemas introductorios/
```

La estructura histórica de GAU55 se conserva desde Drive; los bancos IGL nuevos se documentan en su sección de integración.

Git no representa directorios vacíos, por lo que los niveles clasificados vacíos se mantienen mediante archivos `.gitkeep`.

## Convención

- `01_RAW_PDFs`: PDFs fuente.
- `02_JSON_EXAMS`: exámenes JSON verificados.
- `03_SCHEMA_AND_REPORTS`: reportes y auditorías.
- `04_REFERENCE_SOURCES`: material de referencia.
- `05_CLASSIFIED_EXAMS`: exámenes clasificados y reportes de clasificación.

La documentación o nuevos concursos deben añadirse sin alterar los archivos fuente importados.

<!-- FUSION_PROGRESS_START -->
## FUSIÓN: recuperación revisada

Se preservaron los **32 PDF originales (226 páginas)**. El material de recuperación completo se conserva como borrador sin certificar y no se usa como banco de práctica.

Hay **91 colecciones y 839 problemas publicados**: 753 con respuesta matemática revisada y 86 de práctica guiada, con las ambigüedades o defectos de la fuente explicados. Los 150 problemas GAU55 permanecen disponibles.

La revisión de las **881 apariciones recuperadas está terminada**: 839 están publicadas y otras 42 son variantes de fuente documentadas que no se duplican en el catálogo. No quedan apariciones pendientes. El año se conserva como nulo cuando no está confirmado; no se deduce de la edición.

Consulta el [avance y las rutas publicadas](03_SCHEMA_AND_REPORTS/FUSION/publication_progress.json), el [inventario de fuentes](03_SCHEMA_AND_REPORTS/FUSION/source_manifest.json), las [variantes de fuente](03_SCHEMA_AND_REPORTS/FUSION/source_variant_aliases.json) y el [contrato de respuestas abiertas](03_SCHEMA_AND_REPORTS/FUSION/OPEN_ANSWER_CONTRACT.md). El [borrador de recuperación](04_REFERENCE_SOURCES/FUSION/recovery/working_draft.json) retiene los datos heredados como historial, con advertencias explícitas.

Los lotes incluyen JSON verificados/clasificados, soluciones didácticas, figuras matemáticas limpias y reportes de comparación visual, comprobación matemática, LaTeX y validación estructural. Un validador estructural no demuestra por sí solo corrección matemática.
<!-- FUSION_PROGRESS_END -->

## IGL: bancos de práctica olímpica

Se añadieron **336 problemas en seis colecciones públicas** desde [IGLx0_CUANTLY_CERMAT](https://github.com/MarioIbago/IGLx0_CUANTLY_CERMAT), commit [`61486a2`](https://github.com/MarioIbago/IGLx0_CUANTLY_CERMAT/commit/61486a2a31d239abccd145730073531e1b238477): cuatro lotes de entrenamiento Cuantly por tema (200 problemas), el diagnóstico adaptativo Cuantly (39) y 97 reactivos OMM. La colección visible `OMM-Canguro` conserva `source_competition: "OMM"`; el origen no confirma una edición anual ni que cada reactivo pertenezca a una edición de Canguro.

Los enunciados, respuestas y soluciones existentes se copiaron de IGL. Las 25 figuras geométricas provienen de escenas SVG existentes en IGL; 49 GIF estáticos de OMM se convierten a PNG, con 36 figuras en enunciados y 13 reservadas para las soluciones. El lector muestra estas últimas solo al abrir la solución. No se crearon problemas ni soluciones. Cuando IGL no aporta explicación individual de distractores OMM, `option_analysis` queda vacío; no se generan explicaciones.

Los bancos no identifican año, así que lo conservan como `null` con evidencia. En el diagnóstico, cinco reactivos de razonamiento general quedan sin área porque no existe esa categoría en el esquema publicado. `source_page` conserva el orden de registro empezando en 1, pues el origen es JSON sin paginación; `source_question_label` mantiene el ID original. El informe y las rutas están en [`03_SCHEMA_AND_REPORTS/IGL/`](03_SCHEMA_AND_REPORTS/IGL/README.md). El validador estructural comprueba hashes, dimensiones y decodificación de imágenes de enunciado y solución; no certifica matemáticas ni fidelidad visual.
