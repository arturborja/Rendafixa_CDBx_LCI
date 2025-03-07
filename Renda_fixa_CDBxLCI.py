import numpy as np
import matplotlib.pyplot as plt

anos = 3
# Criando a linha do tempo de 1 a 60 meses
meses = np.arange(1, anos * 12 + 1)
capital = 1000  # Capital inicial
taxa_di = 0.1315  # 13,15% ao ano
LCI_tx = 0.96
CDB_tx = 1.05
LCI = LCI_tx * taxa_di  # 96% do DI
CDB = CDB_tx * taxa_di  # 105% do DI

# Cálculo do rendimento mensal correto
rendimento_lci = (1 + LCI) ** (1/12) - 1
rendimento_cdb = (1 + CDB) ** (1/12) - 1

# Calculando os montantes ao longo do tempo
montante_lci_tempo = capital * (1 + rendimento_lci) ** meses
montante_cdb_bruto_tempo = capital * (1 + rendimento_cdb) ** meses

# Função para definir a alíquota do IR conforme o tempo
def calcular_aliquota(m):
    if m <= 6:
        return 0.225  # 22,5% até 6 meses
    elif m <= 12:
        return 0.20  # 20% de 6 a 12 meses
    elif m <= 24:
        return 0.175  # 17,5% de 12 a 24 meses
    elif m <= 36:
        return 0.15  # 15% de 24 a 36 meses
    else:
        return 0.15  # 15% após 36 meses

# Aplicando a alíquota de IR para cada mês
aliquotas_ir = np.array([calcular_aliquota(m) for m in meses])

# Calculando imposto e montante líquido do CDB
lucro_cdb_tempo = montante_cdb_bruto_tempo - capital
imposto_cdb_tempo = lucro_cdb_tempo * aliquotas_ir
montante_cdb_liquido_tempo = montante_cdb_bruto_tempo - imposto_cdb_tempo

# Calculando os juros totais líquidos
juros_liquido_lci_tempo = montante_lci_tempo - capital
juros_liquido_cdb_tempo = montante_cdb_liquido_tempo - capital

# Calculando a diferença entre CDB e LCI
diferenca_cdb_lci = juros_liquido_lci_tempo - juros_liquido_cdb_tempo

# Criando a figura e o primeiro eixo
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plotando LCI e CDB no eixo primário
ax1.plot(meses, juros_liquido_lci_tempo, label=f"LCI ({LCI_tx*100}% do DI)", color='blue')
ax1.plot(meses, juros_liquido_cdb_tempo, label=f"CDB ({CDB_tx*100}% do DI, líquido)", color='red', linestyle="--")

ax1.set_xlabel("Meses")
ax1.set_ylabel("Juros Total Líquido (R$)")
ax1.set_title("Evolução do Juros Total Líquido e Diferença entre CDB e LCI")
ax1.legend(loc="upper left")
ax1.grid(True)

# Criando o eixo secundário
ax2 = ax1.twinx()
ax2.plot(meses, diferenca_cdb_lci, label="LCI-CDB", color='green', linestyle=":")
ax2.set_ylabel("Diferença CDB - LCI (R$)")
ax2.legend(loc="upper right")

# Adicionando rótulos a cada 5 meses
for i in range(0, len(meses), 5):
    ax1.annotate(f"{juros_liquido_lci_tempo[i]:.0f}", (meses[i], juros_liquido_lci_tempo[i]), 
                 textcoords="offset points", xytext=(-10,5), ha='center', fontsize=9, color='blue')
    ax1.annotate(f"{juros_liquido_cdb_tempo[i]:.0f}", (meses[i], juros_liquido_cdb_tempo[i]), 
                 textcoords="offset points", xytext=(-10,-15), ha='center', fontsize=9, color='red')
    ax2.annotate(f"{diferenca_cdb_lci[i]:.0f}", (meses[i], diferenca_cdb_lci[i]), 
                 textcoords="offset points", xytext=(10,0), ha='center', fontsize=9, color='green')

plt.show()

plt.show()
