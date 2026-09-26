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
