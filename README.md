# Sistema de Gestão Fiscal (ISS, ICMS e IPI)

Primeiro projeto autônomo em Python, criado para praticar lógica de programação aplicada a uma rotina fiscal. Todos os dados são fictícios.

## Como o sistema funciona na prática

[▶ Assistir à demonstração]([Como%20o%20sistema%20funciona%20na%20pr%C3%A1tica.mp4](https://youtu.be/HocqjTOFzcI))

Neste vídeo: emito uma nota com ISS, calculo ICMS e IPI com log de auditoria, importo guias (as inválidas são rejeitadas com o motivo) e gero o relatório final.

## O que faz

- Emite notas fiscais de serviço com cálculo de ISS por categoria
- Calcula ICMS e IPI com **decorador de auditoria** (log automático de cada cálculo)
- Importa guias de ISS em texto, validando com **expressões regulares** (UF, serviço, alíquota e valor) e registra as válidas no livro fiscal
- Gera relatório de faturamento e ISS a pagar
- Menu interativo no terminal

## Conceitos praticados

Funções, classes e métodos, decoradores (`functools.wraps`), regex (`re`), dicionários e listas, tratamento de erros (`try/except`), validação de entrada.

## Como rodar

Para executar o programa, abra o terminal na pasta do projeto e digite `python gestao_fiscal.py`.

## Limitações e próximos passos

- As alíquotas de ICMS (18%) e IPI (5%) são fixas e ilustrativas, não refletem a legislação real, que varia por produto e UF
- Os valores usam `float`; o ideal para dinheiro é `Decimal`
- Faltam testes automatizados

## Como usei IA neste projeto

Usei IA como tutora: pedi que explicasse cada parte do código (decoradores, regex, classes) e depois reescrevi e testei por conta própria para garantir que entendi. A lógica fiscal e as regras de validação (como a faixa de 2% a 5% do ISS) vieram da minha rotina de estudo e trabalho na área tributária. Também encontrei e corrigi inconsistências, como a tabela de alíquotas que não batia com a validação da importação.
