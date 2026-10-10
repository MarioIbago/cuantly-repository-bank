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
└── GAU55_2023_2024_media_structural_audit.json

04_REFERENCE_SOURCES/
└── GAU55/

05_CLASSIFIED_EXAMS/
└── GAU55/
    ├── 2023/Estatal/
    └── 2024/Estatal/
```

La jerarquía, nombres de archivo y contenido se conservan desde Drive.

Git no representa directorios vacíos, por lo que los niveles clasificados vacíos se mantienen mediante archivos `.gitkeep`.

## Convención

- `01_RAW_PDFs`: PDFs fuente.
- `02_JSON_EXAMS`: exámenes JSON verificados.
- `03_SCHEMA_AND_REPORTS`: reportes y auditorías.
- `04_REFERENCE_SOURCES`: material de referencia.
- `05_CLASSIFIED_EXAMS`: exámenes clasificados y reportes de clasificación.

La documentación o nuevos concursos deben añadirse sin alterar los archivos fuente importados.

<!-- FUSION_PROGRESS_START -->
## FUSIÓN: publicación progresiva

Se preservaron los **32 PDF originales (226 páginas)**. El material de recuperación completo se conserva como borrador sin certificar y no se usa como banco de práctica.

Hay **80 colecciones y 663 problemas publicados**: 585 con respuesta matemática revisada y 78 de práctica guiada, con las ambigüedades o defectos de la fuente explicados. Los 150 problemas GAU55 permanecen disponibles.

Quedan **176 apariciones pendientes**. Otras 42 son variantes de fuente documentadas y no se duplican en el catálogo. El año se conserva como nulo cuando no está confirmado; no se deduce de la edición.

Consulta el [avance y las rutas publicadas](03_SCHEMA_AND_REPORTS/FUSION/publication_progress.json), el [inventario de fuentes](03_SCHEMA_AND_REPORTS/FUSION/source_manifest.json), las [variantes de fuente](03_SCHEMA_AND_REPORTS/FUSION/source_variant_aliases.json) y el [contrato de respuestas abiertas](03_SCHEMA_AND_REPORTS/FUSION/OPEN_ANSWER_CONTRACT.md). El [borrador de recuperación](04_REFERENCE_SOURCES/FUSION/recovery/working_draft.json) retiene los registros pendientes con advertencias explícitas.

Los lotes incluyen JSON verificados/clasificados, soluciones didácticas, figuras matemáticas limpias y reportes de comparación visual, comprobación matemática, LaTeX y validación estructural. Un validador estructural no demuestra por sí solo corrección matemática.
<!-- FUSION_PROGRESS_END -->
