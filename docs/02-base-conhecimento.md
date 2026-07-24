# Base de Conhecimento: DBA Mentor 📚

> [!TIP]
> **Prompt usado para esta etapa:**
> 
> Organize a base de conhecimento do agente "DBA Mentor" considerando que agora possuímos um único arquivo consolidado contendo todas as regras de negócios, conceitos de modelagem e scripts SQL. Explique para que serve esse arquivo e monte um exemplo de contexto formatado que será enviado para o LLM.

## 📂 Dados Utilizados

| Arquivo | Formato | Para que serve no DBA Mentor? |
|---------|---------|-------------------------------|
| `conhecimento_sql.txt` | TXT | Arquivo único e consolidado contendo todo o "cérebro" do assistente: conceitos de SGBD, regras de mapeamento conceitual/lógico, normalização (1FN a 3FN), comandos DDL/DML e melhores práticas de fluxo de desenvolvimento. |

---

## 🛠️ Adaptações nos Dados

> **Você modificou ou expandiu os dados mockados? Descreva aqui.**

Em vez de dividir a base em múltiplos arquivos estruturados, optei por consolidar todo o conhecimento técnico em um único documento de texto (`conhecimento_sql.txt`). Isso simplifica a arquitetura do projeto e facilita a manutenção, garantindo que o LLM tenha acesso sequencial e lógico a todos os conceitos (desde o básico sobre o que é dado/informação até agregação avançada com JOINs).

---

## 🔗 Estratégia de Integração

### Como os dados são carregados?
> **Descreva como seu agente acessa a base de conhecimento.**

Como a base de conhecimento agora é um único arquivo textual, a integração no código fonte fica muito mais simples. Em Python, basta carregar o conteúdo deste arquivo para dentro de uma variável:

```python
# Carregando a base de conhecimento consolidada
with open('./data/conhecimento_sql.txt', 'r', encoding='utf-8') as file:
    base_conhecimento = file.read()
```

### Como os dados são usados no prompt?
> **Os dados vão no system prompt? São consultados dinamicamente?**

O conteúdo integral é injetado diretamente como instrução de sistema (System Prompt). O agente usará esse documento como sua base técnica restrita para responder.

```text
Você é o DBA Mentor. Use EXCLUSIVAMENTE a base de conhecimento abaixo para embasar suas respostas.

--- INÍCIO DA BASE DE CONHECIMENTO ---
[Conteúdo integral do arquivo conhecimento_sql.txt é injetado aqui]
--- FIM DA BASE DE CONHECIMENTO ---

Pergunta do Usuário: "Como resolvo uma relação N:N no meu modelo lógico?"
```

---

## 🧩 Exemplo de Contexto Montado

> **Mostre um exemplo de como os dados são formatados para o agente.**

Quando o usuário faz uma pergunta, o LLM recebe o prompt de sistema, a base de conhecimento e a dúvida do usuário. A IA vai buscar no texto exatamente a regra correspondente:

```text
DÚVIDA DO USUÁRIO: "Como transformar um relacionamento N:N do modelo conceitual para o lógico?"

INSTRUÇÃO PARA O LLM:
Busque a resposta na seção "3. REGRAS DE MAPEAMENTO (CONCEITUAL -> LÓGICO)" da sua base de conhecimento.

RESPOSTA ESPERADA BASEADA NO CONTEXTO:
Segundo nossas regras de mapeamento, para um relacionamento N:N, cria-se uma nova tabela (tabela associativa) cuja chave primária é a composição das chaves estrangeiras das entidades relacionadas, incluindo também os atributos próprios do relacionamento.
```
