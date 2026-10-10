# Respuestas abiertas en el banco público

El formato `open_answer` conserva `options: []`, `correct_option_label: null` y `option_analysis: []`. No se inventan distractores. La solución se compara manualmente en la biblioteca; el marcado como resuelto no crea aciertos ni intentos.

`verified_open_answer` indica una respuesta matemática revisada, con `answer_checked: true` y `latex_checked: true`. `all_options_checked: null` significa que no hay opciones que comprobar. Los enunciados ambiguos usan un estado guiado y explican la limitación; no reciben una respuesta única ficticia.

El validador adjunto comprueba estructura, hashes, clasificación y figuras; no certifica por sí mismo las matemáticas, la fidelidad visual ni el renderizado de LaTeX. Los reportes de cada lote registran esos controles separados.

## Año no confirmado

El campo `exam.year` admite un entero positivo confirmado o `null` cuando la fuente no permite confirmarlo. El caso nulo requiere `year_status: "not_confirmed"` y una explicación en `year_evidence`. La biblioteca muestra **Sin fecha** y usa ese segmento en la identidad de colección. No se infiere el año a partir de la edición. El validador conserva los controles anteriores para bancos con año conocido.
