# %%
import pandas as pd

arquivo = '../data/raw/base.csv'
# %%
df = pd.read_csv(arquivo)
df.head()
# %%
# Leitura do arquivo e dimensões
df.shape
# %%
# Lista de todas as colunas
df.columns.to_list()
# %%
# Informações de colunas
df.info()
# %%
# Data mais antiga com registro
df['data_abertura'].min()
# %%
# Data mais recente com registro
df['data_abertura'].max()
# %%
# Quantidade de valores nulos de cada coluna
df.isnull().sum()
# %%
# Quantidade de registros duplicados
df.duplicated().sum()
# %%
# Menor tempo de resolução em horas
df['tempo_resolucao_horas'].min()
# %%
# Maior tempo de resolução em horas
df['tempo_resolucao_horas'].max()
# %%
# Menor tempo da primeiro resposta
df['tempo_primeira_resposta_min'].min()
# %%
# Maior tempo da primeiro resposta
df['tempo_primeira_resposta_min'].max()
# %%
df.columns
# %%
# Verificação de tipos de prioridade existentes
df.groupby('prioridade')['chamado_id'].count()
# %%
# Verificação de tipos de status existentes
df.groupby('status')['chamado_id'].count()
# %%
# Padronização da coluna de data
df['data_abertura'] = pd.to_datetime(df['data_abertura'], format='%Y-%m-%d %H:%M:%S')
# %%
df['data_fechamento'] = pd.to_datetime(df['data_fechamento'], format='mixed').dt.floor('s')
# %%
df.head()
# %%
# Qual é a categoria de chamado mais frequente?
df.groupby('categoria')['chamado_id'].count().sort_values(ascending=False)
# %%
# Qual é a prioridade mais frequente?
df.groupby('prioridade')['chamado_id'].count().sort_values(ascending=False)
# %%
# Qual é o status mais frequente?
df.groupby('status')['chamado_id'].count().sort_values(ascending=False)
# %%
# Qual técnico recebeu mais chamados?
df.groupby('tecnico')['chamado_id'].count().sort_values(ascending=False)

# %%
# Qual setor/departamento abriu mais chamados?
df.groupby('departamento')['chamado_id'].count().sort_values(ascending=False)
# %%
df['mes_abertura'] = df['data_abertura'].dt.month
# %%
# Mês com mais chamados
df.groupby('mes_abertura')['chamado_id'].count().sort_values(ascending=False)
# %%
df['dia_semana'] = df['data_abertura'].dt.dayofweek
# %%
# Dia da semana com maior ocorrência de chamados
df.groupby('dia_semana')['chamado_id'].count().sort_values(ascending=False)
# %%
df['hora_abertura'] = df['data_abertura'].dt.hour
# %%
# Hora do dia com a maior ocorrência de chamados.
df.groupby('hora_abertura')['chamado_id'].count().sort_values(ascending=False)
# %%
# Qual categoria possui maior volume de chamados críticos/alta prioridade?
prioritario = df[df['prioridade'] == 'Crítica'].groupby(['categoria','prioridade'])['chamado_id'].count().sort_values(ascending=False)
prioritario.head()
# %%
#Qual é o tempo médio de resolução?
    
#Qual é o tempo mediano de resolução?
    
#Qual categoria demora mais para ser resolvida?
    
#Qual técnico possui o maior tempo médio de resolução?
    
#Qual percentual dos chamados está dentro do SLA?
    
#Qual categoria possui o pior cumprimento de SLA?