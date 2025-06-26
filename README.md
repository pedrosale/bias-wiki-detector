🧠 Bias Wiki Detector
Ferramenta de análise de viés em artigos da Wikipedia sobre inteligência artificial.

🎯 Objetivo
Permitir que o usuário pesquise um termo (ex: "inteligência artificial") e analise os artigos mais recentes relacionados a esse termo, com foco em possíveis trechos tendenciosos, opiniões disfarçadas de fatos e ausência de contrapontos relevantes.

⚙️ Como usar
Clone o repositório:

bash
Copiar
Editar
git clone https://github.com/seu_usuario/seu_repositorio.git
cd seu_repositorio
Execute main.py para buscar os artigos mais atuais da Wikipedia contendo o termo desejado.

A análise de viés é feita posteriormente ao executar a função analisar_artigos(df), utilizando LLMs.

📊 Exemplo de saída esperada
Artigo	Link	Data de edição
Inteligência artificial	https://pt.wikipedia.org/wiki/Intelig%C3%AAncia_artificial	2025-06-15T00:24:45Z
Engenharia de IA	https://pt.wikipedia.org/wiki/Engenharia_de_intelig%C3%AAncia_artificial	2025-06-10T18:31:02Z

🔎 Tipos de análise
A ferramenta aplica três tipos de avaliação ao conteúdo dos artigos:

1. Linguagem tendenciosa (Bias linguístico)
Detecta exageros, adjetivação de valor, generalizações ou suposições que comprometam a neutralidade do texto.

Exemplo:

Trecho: "O interesse cresceu vertiginosamente..."

Viés: Sensacionalismo

Reescrita neutra: "O interesse aumentou nas últimas décadas."

2. Opinião disfarçada de fato
Identifica trechos em que uma opinião é apresentada como se fosse um fato objetivo, sem evidência ou sem deixar claro o caráter interpretativo.

Exemplo:

Trecho: "A empresa foi uma das que mais cresceram..."

Motivo: Não há dados apresentados para validar essa afirmação.

Reescrita: "A empresa relatou crescimento no período..."

3. Ausência de contraponto relevante
Aponta quando um artigo omite perspectivas críticas, dados conflitantes ou impactos relevantes relacionados ao tema tratado.

Exemplo:

Tema ausente: Impactos éticos e sociais da IA

Importância: Essencial para compreensão das consequências da IA na sociedade

Como incluir: Adicionar seção com exemplos de impactos no mercado de trabalho, privacidade e justiça

🔧 Observações técnicas
Utiliza a API da Wikipedia (MediaWiki API)

LLMs são acessadas via API OpenAI (gpt-4o, gpt-4o-mini, ou outro definido via variável OPENAI_MODEL)

Os modelos devem retornar respostas em JSON válido

Apenas artigos com o termo exato no título são considerados

Limite de ~6.000 caracteres por artigo para análise

📂 Estrutura esperada dos dados
A análise gera um DataFrame com as seguintes colunas:

Artigo

Link

Trecho (Tendencioso)

Tipo de Viés

Explicação (Viés)

Reescrita (Viés)

Trecho (Opinião disfarçada)

Motivo (Opinião)

Reescrita (Opinião)

Tema ausente

Importância do Contraponto

Sugestão de Inclusão

🪪 Licença
MIT © 2025 — Pedro Amorim
