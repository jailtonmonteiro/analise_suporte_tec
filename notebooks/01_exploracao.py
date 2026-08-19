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
df.groupby('prioridade')['chamado_id'].size()
# %%
# Verificação de tipos de status existentes
df.groupby('status')['chamado_id'].size()
# %%
# Padronização da coluna de data
df['data_abertura'] = pd.to_datetime(df['data_abertura'], format='%Y-%m-%d %H:%M:%S')
# %%
df['data_fechamento'] = pd.to_datetime(df['data_fechamento'], format='mixed').dt.floor('s')
# %%
df.head()
# %%
# Qual é a categoria de chamado mais frequente?
df.groupby('categoria')['chamado_id'].size().sort_values(ascending=False)
# %%
# Qual é a prioridade mais frequente?
df.groupby('prioridade')['chamado_id'].size().sort_values(ascending=False)
# %%
# Qual é o status mais frequente?
df.groupby('status')['chamado_id'].size().sort_values(ascending=False)
# %%
# Qual técnico recebeu mais chamados?
df.groupby('tecnico')['chamado_id'].size().sort_values(ascending=False)

# %%
# Qual setor/departamento abriu mais chamados?
df.groupby('departamento')['chamado_id'].size().sort_values(ascending=False)
# %%
df['mes_ano'] = df['data_abertura'].dt.to_period('M')
# %%
# Mês com mais chamados
df.groupby('mes_ano')['chamado_id'].size().sort_values(ascending=False)
# %%
dias = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}
df['dia_semana'] = df['data_abertura'].dt.dayofweek.map(dias)
# %%
# Dia da semana com maior ocorrência de chamados
df.groupby('dia_semana')['chamado_id'].size().sort_values(ascending=False)
# %%
df['hora_abertura'] = df['data_abertura'].dt.hour
# %%
# Hora do dia com a maior ocorrência de chamados.
df.groupby('hora_abertura')['chamado_id'].size().sort_values(ascending=False)
# %%
# Qual categoria possui maior volume de chamados críticos/alta prioridade?
prioritario = df[df['prioridade'] == 'Crítica'].groupby(['categoria','prioridade'])['chamado_id'].size().sort_values(ascending=False)
prioritario.head()
# %%
#Qual é o tempo médio de resolução?    
#Qual é o tempo mediano de resolução?
tempo_medio = df['tempo_resolucao_horas'].describe()
tempo_medio
# %%
#Qual categoria demora mais para ser resolvida?
pd.to_timedelta((df.groupby('categoria')['tempo_resolucao_horas'].median()), unit='h').sort_values(ascending=False)

# %%
#Qual técnico possui o maior tempo médio de resolução?
pd.to_timedelta((df.groupby('tecnico')['tempo_resolucao_horas'].mean()), unit='h').sort_values(ascending=False)

# %%
#Qual percentual dos chamados está dentro do SLA?
((df.groupby('dentro_sla')['chamado_id'].size() / df.shape[0]) * 100).round(2)

#%%
#Qual categoria possui o pior cumprimento de SLA?
total_sla = df.groupby('categoria')['chamado_id'].size().sort_values(ascending=False).reset_index().rename(columns = {'chamado_id':'total_chamados'})
pior_sla = df[df['dentro_sla'].eq('Não')].groupby('categoria')['chamado_id'].size().reset_index().rename(columns = {'chamado_id':'fora_sla'})
diff_sla = pd.merge(total_sla, pior_sla, on='categoria')
diff_sla['%_fora_sla'] = (diff_sla['fora_sla'] / diff_sla['total_chamados'] * 100).round(2)
diff_sla
# %%
# Quantos chamados existem?
total_chamados = df['chamado_id'].count()
# Quantos foram encerrados?
chamado_encerrado = df[df['status'] == 'Fechado']['chamado_id'].count() + df[df['status'] == 'Resolvido']['chamado_id'].count()
#Quantos ainda estão abertos?
chamados_pendentes = df[df['status'] == 'Aberto']['chamado_id'].count() + df[df['status'] == 'Em andamento']['chamado_id'].count()
# Quantos são de alta/criticidade elevada?
chamados_criticos = df[df['prioridade'] == 'Crítica']['chamado_id'].count()
# Quanto tempo, em média, o suporte leva para resolver?
media_resolucao = pd.to_timedelta(df['tempo_resolucao_horas'].mean().round(1), unit='h')
# Qual é o tempo mediano de resolução?
mediana_resolucao = pd.to_timedelta(df['tempo_resolucao_horas'].median().round(1), unit='h')
# Qual % dos chamados respeitou o SLA?
sla_cumprido = (df['dentro_sla'].eq('Sim').mean() * 100).round(2)
# %%
print(f"""
    Total de chamados:          {total_chamados}
    Chamados resolvidos:        {chamado_encerrado}
    Chamados pendentes:         {chamados_pendentes}
    Alta prioridade:            {chamados_criticos}
    Tempo médio resolução:      {media_resolucao}
    Mediana resolução:          {mediana_resolucao}
    SLA cumprido:               {sla_cumprido} %
""")

# %%
# Qual categoria possui mais chamados?
df.groupby('categoria')['chamado_id'].size().sort_values(ascending=False)

# %%
# Qual categoria possui o maior tempo médio de resolução?
df.groupby('categoria')['tempo_resolucao_horas'].mean().sort_values(ascending=False).round(1)

# %%
# Qual categoria possui mais chamados de alta prioridade?
df[df['prioridade'] == 'Crítica'].groupby('categoria')['chamado_id'].size().sort_values(ascending=False)

#%%
# Qual categoria possui o pior SLA?
pd.to_timedelta(df[df['dentro_sla'] == 'Não'].groupby('categoria')['tempo_resolucao_horas'].median(), unit='h')

# %%
# Quem resolve mais chamados?
df.groupby('tecnico')['chamado_id'].size().sort_values(ascending=False)

# %%
# Quem possui o menor tempo médio de resolução?
df.groupby('tecnico')['tempo_resolucao_horas'].mean().sort_values()

# %%
# Existe algum técnico com volume muito maior que os outros?
vol_atendimento = df.groupby('tecnico')['chamado_id'].size().sort_values(ascending=False).reset_index().rename(columns={'chamado_id':'qtd_chamado'})
vol_atendimento['atend_relativo'] = (vol_atendimento['qtd_chamado'] / vol_atendimento['qtd_chamado'].sum() * 100).round(1)
vol_atendimento['diff_atendimento'] = vol_atendimento['atend_relativo'].diff()
vol_atendimento.sort_values('atend_relativo', ascending=False)
# %%
# Existe algum técnico com SLA significativamente pior?
sla_tec = df.groupby('tecnico')['chamado_id'].size().sort_values(ascending=False).reset_index().rename(columns={'chamado_id': 'total_chamado'})
sla_tec_neg = df[df['dentro_sla'].eq('Não')].groupby('tecnico')['chamado_id'].size().reset_index().rename(columns={'chamado_id': 'fora_sla'})
diff_sla_tec = pd.merge(sla_tec, sla_tec_neg, on='tecnico')
diff_sla_tec['%_fora'] = (diff_sla_tec['fora_sla'] / diff_sla_tec['total_chamado'] * 100).round(2)
diff_sla_tec
# %%
# Qual mês teve mais chamados?
df.groupby('mes_ano')['chamado_id'].size().sort_values(ascending=False).reset_index().rename(columns={'chamado_id':'qtd_chamado'})

# %%
# O volume de chamados está aumentando ou diminuindo?
vol_chamados = df.groupby(['mes_ano'])['chamado_id'].size().reset_index().rename(columns={'chamado_id':'qtd_chamado'})
vol_chamados['variacao'] = vol_chamados['qtd_chamado'].astype('Int64').diff()
vol_chamados['%_variacao'] = (vol_chamados['qtd_chamado'].pct_change() * 100).round(2)
vol_chamados

# %%
# Existe algum dia da semana com concentração de chamados?

ocor_semanal = df.groupby('dia_semana')['chamado_id'].size().sort_values(ascending=False).reset_index().rename(columns={'chamado_id':'qtd_chamado'})
ocor_semanal
# %%

relat_tec = df.groupby('tecnico').agg(
    qtd_total=('chamado_id', 'count'),
    tempo_medio=('tempo_resolucao_horas', 'mean'),
    sla_expirado=('dentro_sla', lambda x: (x == 'Não').sum()),
    perc_sla_expirado=('dentro_sla', lambda x: (x == 'Não').mean() * 100)
)

relat_tec['tempo_medio'] = pd.to_timedelta(relat_tec['tempo_medio'], unit='h').dt.floor('s')
relat_tec['perc_sla_expirado'] = relat_tec['perc_sla_expirado'].round(2)
relat_tec
# %%
faixas = ['Bom desempenho', 'Atenção', 'Crítico']
cortes = [0, 27, 28, float('inf')]

relat_tec['classificacao'] = pd.cut(
    x=relat_tec['perc_sla_expirado'],
    bins=cortes,
    labels=faixas
)
relat_tec
# %%
