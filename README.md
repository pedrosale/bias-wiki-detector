# 🧠 Bias Wiki Detector

Ferramenta que examina artigos da Wikipédia sobre inteligência artificial e destaca três dimensões de desequilíbrio textual:

| Dimensão analisada | O que procura no texto? | Sub-tipos detectados |
|--------------------|-------------------------|----------------------|
| **1. Linguagem tendenciosa** | Palavras ou construções que induzem parcialidade. | • Favoritismo<br>• Preconceito<br>• Sensacionalismo<br>• Generalização indevida<br>• Adjetivação de valor<br>• Verbo carregado<br>• Suposição implícita |
| **2. Opinião disfarçada de fato** | Frases que aparentam ser factuais, mas contêm julgamento, interpretação ou suposição não-comprovada. | — |
| **3. Ausência de contraponto** | Pontos de vista alternativos, dados ou impactos relevantes omitidos que comprometeriam a imparcialidade. | — |

### Definições rápidas dos sub-tipos

| Sub-tipo | Descrição concisa |
|----------|------------------|
| **Favoritismo** | Linguagem que exalta positivamente algo sem base objetiva. |
| **Preconceito** | Linguagem que desvaloriza ou estereotipa negativamente. |
| **Sensacionalismo** | Uso de termos exagerados ou alarmistas. |
| **Generalização indevida** | Conclusões amplas a partir de poucos casos ou sem considerar exceções. |
| **Adjetivação de valor** | Adjetivos subjetivos que emitem juízo (ex.: “brilhante”, “desastroso”). |
| **Verbo carregado** | Verbos que sugerem avaliação ou emoção (ex.: “impôs”, “destruiu”). |
| **Suposição implícita** | Relações de causa/efeito ou intenções assumidas sem evidência. |

A saída da ferramenta apresenta, para cada artigo:

- **Trecho** problemático identificado  
- **Classificação** (sub-tipo ou dimensão)  
- **Explicação** breve do viés  
- **Reescrita sugerida** em tom neutro  
- **Contraponto ausente** (quando aplicável) e sugestão de inclusão
