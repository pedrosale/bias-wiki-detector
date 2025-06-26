# 🧠 Bias Wiki Detector

Ferramenta de análise de viés em artigos da Wikipedia sobre inteligência artificial.

## Objetivo
Permitir que o usuário pesquise um termo (ex: "inteligência artificial") e analise os artigos mais recentes relacionados a esse termo, com foco em possíveis trechos tendenciosos.

## Como usar

1. Clone o repositório
2. Execute `main.py` para buscar os artigos
3. A análise de viés é feita posteriormente usando LLMs com o conteúdo obtido

## Exemplo de saída esperada
| Artigo                        | Link                                                       | Data de edição         |
|------------------------------|------------------------------------------------------------|------------------------|
| Inteligência artificial      | https://pt.wikipedia.org/wiki/Intelig%C3%AAncia_artificial | 2025-06-15T00:24:45Z   |
| Engenharia de IA             | https://pt.wikipedia.org/wiki/Engenharia_de_intelig%C3%AAncia_artificial | 2025-06-10T18:31:02Z   |

## Observações
- Utiliza a API da Wikipedia
- Apenas artigos com o termo exato no título são considerados
