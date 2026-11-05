import pandas as pd

df = pd.read_excel('PETR4_evolucao.xlsx')
print(df)
df['valor'].max()
df['valor'].min()
df['valor'].mean()
df['valor'].std()
# selecionar linhas 
df[0:1]
# selecionando linhas e colunas 
colunas = ['conta', 'valor']
df[23:24][colunas]
# filtrar linhas atraves valor 
df['trimestre'] == '20262T'
colunas = ['conta', 'valor']
df[linhas][colunas]
# linha
linhas = df['conta'] == 'lucro'
colunas = ['valor']
df[linhas][colunas].mean()
#graficos
import seaborn as sns
import matplotlib.pyplot as plt
#graficos de lucro 
linhas = df['conta'] == 'lucro'
colunas = ['trimestre', 'valor']
dados = df[linhas][colunas]
sns.lineplot(dados, x='trimestre', y='valor')
plt.title('Grafico do Lucro')
plt.xticks(rotation=45)
plt.show()