# Sistema de Gestão Fiscal (ISS, ICMS e IPI)

Primeiro projeto autônomo em Python, criado para praticar lógica de programação aplicada a uma rotina fiscal. Todos os dados são fictícios.

# Como o sistema funciona na prática

[▶ Assistir à demonstração](Como%20o%20sistema%20funciona%20na%20pr%C3%A1tica.mp4)

Neste vídeo: emito uma nota com ISS, calculo ICMS e IPI com log de auditoria, importo guias (as inválidas são rejeitadas com o motivo) e gero o relatório final.

# O que faz

- Emite notas fiscais de serviço com cálculo de ISS por categoria
- Calcula ICMS e IPI com **decorador de auditoria** (log automático de cada cálculo)
- Importa guias de ISS em texto, validando com **expressões regulares** (UF, serviço, alíquota e valor) e registra as válidas no livro fiscal
- Gera relatório de faturamento e ISS a pagar
- Menu interativo no terminal

## Conceitos Praticados

Funções, classes e métodos, decoradores (`functools.wraps`), regex (`re`), dicionários e listas, tratamento de erros (`try/except`), validação de entrada.
