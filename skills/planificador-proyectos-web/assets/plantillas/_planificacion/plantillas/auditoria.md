# Auditoría NN · Título

| Metadato | Valor |
| :------- | :---- |
| Fecha | AAAA-MM-DD |
| Auditor | herramienta y modelo, o persona |
| Commit auditado | hash y rama |
| Alcance | qué se auditó: una épica, sus iteraciones y commits, o los insumos iniciales |
| Método | qué se leyó y qué se ejecutó de verdad (comandos, mediciones) |
| Limitaciones | lo que no se pudo revisar y por qué |

> Se guarda como `00_producto/auditorias/auditoria-NN.md`, donde NN es el último número del índice de `auditoria-tecnica.md` más uno. Los hallazgos nuevos se agregan también a la tabla de ese índice, que es donde se actualiza su estado. Esta auditoría no se edita después de entregada.

## 1. Veredicto

Tres a cinco líneas: si lo auditado cumple lo que dice cumplir y qué es lo más importante que encontraste.

## 2. Qué se implementó bien

- …

## 3. Verificaciones técnicas

| Verificación | Comando o medición | Resultado |
| :----------- | :----------------- | :-------- |
| … | … | … |

## 4. Trazabilidad del plan a la implementación

> Para la auditoría de una épica: cada criterio marcado como cumplido, comparado con lo que realmente existe. Si la auditoría es de insumos iniciales, borra la sección.

| Iteración | Criterio | Marcado | Comprobado | Observación |
| :-------- | :------- | :------ | :--------- | :---------- |
| XX-YY | … | Sí | Sí / No | … |

## 5. Conformidad con DESIGN.md y AGENTS.md

- Estándares de calidad, reglas técnicas y de diseño: qué se cumple y qué no, con ejemplos concretos.
- Documentos fuera de `.claude/hooks/documentos-permitidos.md`: cuáles hay, o «ninguno».

## 6. Hallazgos

| ID | Severidad | Área | Hallazgo | Dónde | Acción recomendada |
| :- | :-------- | :--- | :------- | :---- | :----------------- |
| AUD-NN-001 | Alta / Media / Baja | … | … | archivo o carpeta | … |

## 7. Cierre de hallazgos anteriores

> Hallazgos abiertos de auditorías previas que esta revisión comprobó como resueltos, con la evidencia. Si no hay, escribe «Ninguno».

- AUD-NN-MMM: resuelto en XX-YY (medido en …).
