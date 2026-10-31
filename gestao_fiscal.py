# SISTEMA DE GESTÃO FISCAL (ISS)

import re 
from functools import wraps
from datetime import datetime

# ============================================================

def auditoria_fiscal(funcao):
    """
    Decorador que intercepta o cálculo de impostos e registra 
    um log automático de auditoria sem modificar a lógica da função.
    """
    @wraps(funcao)
    def wrapper(self, *args, **kwargs):
        # Executa a função original
        resultado = funcao(self, *args, **kwargs)
        
        # Registra o log de auditoria
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nome_imposto = funcao.__name__.upper()
        
        print(f"\n{'='*60}")
        print(f"LOG DE AUDITORIA FISCAL")
        print(f"{'='*60}")
        print(f"Timestamp: {timestamp}")
        print(f"Imposto Calculado: {nome_imposto}")
        print(f"Valor Base: R$ {self.valor_base:.2f}")
        print(f"Valor do Imposto: R$ {resultado:.2f}")
        print(f"Percentual: {funcao.__doc__}")
        print(f"{'='*60}\n")
        
        return resultado
    
    return wrapper


# ============================================================

class NotaFiscal:
    """
    Classe para gerenciar notas fiscais e calcular impostos.
    Suporta: ICMS e IPI com auditoria automática.
    (ISS é calculado pela classe Empresa)
    """
    
    def __init__(self, valor_base, numero_nf="", descricao=""):
        self.valor_base = valor_base
        self.numero_nf = numero_nf
        self.descricao = descricao
        self.impostos_calculados = {}
        
    @auditoria_fiscal
    def calcular_icms(self):
        """18%"""
        icms = self.valor_base * 0.18
        self.impostos_calculados['ICMS'] = icms
        return icms
    
    @auditoria_fiscal
    def calcular_ipi(self):
        """5%"""
        ipi = self.valor_base * 0.05
        self.impostos_calculados['IPI'] = ipi
        return ipi
    
    def calcular_todos_impostos(self):
        """Calcula todos os impostos e retorna resumo"""
        print(f"\n{'*'*60}")
        print(f"CALCULANDO TODOS OS IMPOSTOS - NF {self.numero_nf}")
        print(f"{'*'*60}")
        
        icms = self.calcular_icms()
        ipi = self.calcular_ipi()
        
        total_impostos = icms + ipi
        valor_final = self.valor_base + total_impostos
        
        print(f"\n{'='*60}")
        print(f"RESUMO FINAL - NF {self.numero_nf}")
        print(f"{'='*60}")
        print(f"Valor Base: R$ {self.valor_base:.2f}")
        print(f"ICMS (18%): R$ {icms:.2f}")
        print(f"IPI (5%): R$ {ipi:.2f}")
        print(f"{'-'*60}")
        print(f"Total de Impostos: R$ {total_impostos:.2f}")
        print(f"Valor Total da NF: R$ {valor_final:.2f}")
        print(f"{'='*60}\n")
        
        return {
            'valor_base': self.valor_base,
            'icms': icms,
            'ipi': ipi,
            'total_impostos': total_impostos,
            'valor_final': valor_final
        }



# ============================================================

class Empresa:
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        self.tabela_aliquotas = {
            "Consultoria": 7.0,
            "Informática": 3.5,
            "Desenvolvimento": 5.5,
            "Suporte": 3.0
        }
        self.livro_fiscal = {}
        
    def emitir_nf(self, nf, uf, categoria, valor_bruto):
        """Emite uma nota fiscal com cálculo de ISS"""
        if categoria in self.tabela_aliquotas:
            aliquota = self.tabela_aliquotas[categoria]
            imposto = valor_bruto * (aliquota / 100)
            
            self.livro_fiscal[nf] = {
                "estado": uf,
                "servico": categoria,
                "valor_bruto": valor_bruto,
                "iss": imposto
            }
            print(f"Nota {nf} emitida com sucesso!")
            print(f"Valor Bruto: R$ {valor_bruto:.2f}")
            print(f"ISS ({aliquota}%): R$ {imposto:.2f}\n")
        else:
            print(f"Categoria '{categoria}' inválida.")
            print(f"Use: {list(self.tabela_aliquotas.keys())}\n")
    
    def gerar_relatorio(self):
        """Gera relatório fiscal da empresa"""
        if not self.livro_fiscal:
            print("Nenhuma nota fiscal registrada.\n")
            return
            
        print(f"\n{'='*60}")
        print(f"RELATÓRIO FISCAL - {self.nome}")
        print(f"CNPJ: {self.cnpj}")
        print(f"{'='*60}\n")

        total_faturado = 0
        total_iss = 0

        for nf, info in self.livro_fiscal.items():
            print(f"NF: {nf} | UF: {info['estado']} | {info['servico']}")
            print(f"  Bruto: R$ {info['valor_bruto']:.2f} | ISS: R$ {info['iss']:.2f}")
            total_faturado += info['valor_bruto']
            total_iss += info['iss']

        print(f"\n{'-'*60}")
        print(f"Faturamento Total: R$ {total_faturado:.2f}")
        print(f"Total ISS a Pagar: R$ {total_iss:.2f}")
        print(f"{'-'*60}\n")


# ============================================================
# FUNÇÕES DE IMPORTAÇÃO (MANTIDAS DO ORIGINAL)
# ============================================================

guias_recebidas = [
    "GUIA-ISS:SP35Consultoria-2.0%-10000.00",      # Válida
    "GUIA-ISS:RJ33Desenvolvimento-6.5%-5000.00",   # Erro: Alíquota Abusiva (> 5%)
    "GUIA-ISS:MG12Marketing-3.0%-2000.00",         # Erro: Serviço Inválido
    "GUIA-ISS:PR41Produtos-4.0%-0.00",             # Erro: Valor Inválido (= 0)
    "GUIA-ISS:XY35Consultoria-2.0%-10000.00"       # Erro: Estado Inválido
]

def importar_nf():
    """Processa importação de notas fiscais com validação"""
    print("\n=== PROCESSANDO IMPORTAÇÃO DE NOTAS FISCAIS ===")
    
    ufs_validas = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
    servicos_validos = ["Consultoria", "Desenvolvimento", "Suporte", "Informática"]
    padrao_estrutura = r"^GUIA-ISS:(?P<uf>[A-Z]{2})\d{2}(?P<servico>[A-Za-zÇçáéíóúÁÉÍÓÚ]+)-(?P<aliquota>[\d.]+)%-(?P<valor>[\d.]+)$"
    
    notas_importadas_com_sucesso = []
    
    for i, guia in enumerate(guias_recebidas, 1):
        print(f"\nAnalisando Guia {i}: '{guia}'")
        
        match = re.match(padrao_estrutura, guia, re.IGNORECASE)
        
        if not match:
            print("ERRO: Estrutura geral da guia inválida.")
            continue
            
        dados = match.groupdict()
        uf = dados['uf'].upper()
        servico = dados['servico'].capitalize()
        aliquota = float(dados['aliquota'])
        valor = float(dados['valor'])
        
        erros_encontrados = []
        
        if uf not in ufs_validas:
            erros_encontrados.append(f"Estado Inválido ('{uf}')")
        if servico not in servicos_validos:
            erros_encontrados.append(f"Serviço Inválido ('{servico}')")
        if aliquota < 2.0 or aliquota > 5.0:
            erros_encontrados.append(f"Alíquota Inválida ({aliquota}%)")
        if valor <= 0:
            erros_encontrados.append(f"Valor Inválido (R$ {valor})")
            
        if erros_encontrados:
            for erro in erros_encontrados:
                print(f"ERRO: {erro}")
        else:
            print(f"SUCESSO: Guia válida!")
            print(f"UF: {uf} | {servico} | {aliquota}% | R$ {valor:.2f}")
            
            notas_importadas_com_sucesso.append({
                "uf": uf,
                "servico": servico,
                "aliquota": aliquota,
                "valor": valor
            })
            
    print("\n" + "="*60 + "\n")
    
    return notas_importadas_com_sucesso


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu_principal():
    """Menu interativo do sistema"""
    print("\n" + "="*60)
    print("SISTEMA DE GESTÃO FISCAL (ISS, ICMS, IPI)")
    print("="*60)
    
    nome_usuario = input("\nDigite o nome da empresa: ").strip()
    cnpj_usuario = input("Digite o CNPJ da empresa: ").strip()
    
    minha_empresa = Empresa(nome_usuario, cnpj_usuario)
    
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("1 - Emitir Nota Fiscal (ISS)")
        print("2 - Calcular Impostos com Auditoria (ICMS e IPI)")
        print("3 - Importar Notas Fiscais")
        print("4 - Gerar Relatório")
        print("5 - Sair")
        print("="*60)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n--- EMITIR NOTA FISCAL ---")
            num = input("Número da nota: ").strip()
            est = input("Unidade federativa (ex: SP): ").strip().upper()
            print(f"\nCategorias aceitas: {list(minha_empresa.tabela_aliquotas.keys())}")
            cat = input("Categoria do serviço: ").strip()
            
            try:
                v_bruto = float(input("Valor bruto (R$): "))
                if v_bruto <= 0:
                    print("Valor deve ser positivo!\n")
                else:
                    minha_empresa.emitir_nf(num, est, cat, v_bruto)
            except ValueError:
                print("Valor inválido!\n")
        
        elif opcao == "2":
            print("\n--- CALCULAR IMPOSTOS COM AUDITORIA ---")
            try:
                nf_num = input("Número da Nota Fiscal: ").strip()
                valor = float(input("Valor base (R$): "))
                
                if valor <= 0:
                    print("Valor deve ser positivo!\n")
                else:
                    nota = NotaFiscal(valor, numero_nf=nf_num)
                    nota.calcular_todos_impostos()
            except ValueError:
                print("Valor inválido!\n")
        
        elif opcao == "3":
            importar_nf()
        
        elif opcao == "4":
            minha_empresa.gerar_relatorio()
        
        elif opcao == "5":
            print("\nSaindo do sistema... Até logo!")
            break
        
        else:
            print("\nOpção inválida. Tente novamente.\n")


if __name__ == "__main__":
    menu_principal()