
import pandas as pd
import datetime as dt
from datetime import timedelta

def create_fulldf(gateway, sensors, measurements):

    """
    A função cria uma tabela concatenada com as correções necessárias para facilitar 
    o uso das funções seguintes. PS: Alguns aparecem com nomes repetidos apesar de terem 
    IDs únicos. Como o nome é um "apelido", considerei que descartar essas repetições
    não fossem válidas.

    Parameters
    ----------
    gateway : gateway:dataframe
    DESCRIPTION.
    sensors : sensors: dataframe
    DESCRIPTION.
    measurements : measurements: dataframe
    DESCRIPTION.

    Returns
    -------
    full_df : full_df: datafreame
        Retorna as três tabelas devidamente concatenadas.

    """
    gateway.rename(columns={"id": "gateway_id","name":"name_gateway"}, inplace=True)
    sensors.rename(columns={"id": "sensorID", "gatewayId":"gateway_id","name":"name_sensor"}, inplace=True)
    measurements.rename(columns={"id":"measurementID", 'sensor':'sensorID'}, inplace=True)
    full_df = gateway.merge(sensors, on = 'gateway_id', how = 'inner') 
    full_df = full_df.merge(measurements, on = 'sensorID', how = 'inner').reset_index(drop=True)
    full_df['name_gateway']=full_df['name_gateway'].str.strip('gateway_').astype(int)
    return full_df

# Primeira coluna: Limpar os IDs únicos dos gateway
def column_1 (df):
    col_1 = df[['gatewayID']].drop_duplicates().reset_index(drop=True)
    
    return col_1

# Segunda coluna: Corrigindo o nome dos gateways
def column_2 (df):
  df =pd.DataFrame(df['name_gateway']).drop_duplicates().reset_index(drop=True)
  df = df['name_gateway'].apply(lambda x: '0'+str(x) if x < 10 else str(x))
  df = pd.DataFrame(df.apply(lambda x: 'GATEWAY '+ x))
  return df

# Terceira coluna: Número de sensores associados a cada um dos gateways
def column_3(df):  
    """
    A Função conta quantos sensores cada dispositivo gateway possui. Os sensores 
    não se repetem nos gateways, então filtrando os registros únicos dos sensores só
    é preciso contar quantas vezes o nome de cada gateway se repete.

    Parameters
    ----------
    df :full_df:dataset completo após o merge
        Os nomes dos gateways precisam estar padronizados em todas as linhas para 
        que as linhas da coluna sensorID sejam bem filtradas.

    Returns
    -------
    df : datafame: int
        Será retornado um dataframe de apenas uma coluna com número inteiros representando 
        o número de sensores que cada gateway possui.

    """
    df=df.iloc[:,[1,2]]
    df=df.drop_duplicates(subset = ['sensorID'])
    df=pd.DataFrame(df['name_gateway'].value_counts(sort=False)).reset_index(drop=True)
    return df

# Quarta coluna: Validando com True ou False se as configurações de cada gateway está configurada
def column_4(df):
    """
    A função vai filtrar a planilha de acordo com cada dispositivo gateway e avaliar
    se ele possui os seus sensores configurados para o início das medições (coluna start)
    e o intervalo de tempo para fazer as medições (colana frequency). A função monta 
    uma lista de três valores representando a coluna 1.sensorID, 2.start e 3.fequency.
    A lista enumera 1 se o valor de uma das colunas estiver ausente, caso contrário
    enumerará 0 (O primeiro valor da lista nunca enumera 1). Se a lista de qual quer
    um dos sensores enumerar 1, o seu respectivo gateway irá receber um valor False.

    Parameters
    ----------
    df : full_df:dataset completo após o merge
        Função precisa de três colunas. A do sensorID para retirar as linhas duplicada,
    e as colunas start e frequency sem receber nenhuma limpeza para que seja possível
    avaliar a configuação dos sensores.

    Returns
    -------
    valid : Lista: Bool
        Os valores True ou False levantados após a função filtrar cada um dos gateways
    será adicionado a uma lista seguindo a ordem de numeração dos dispositivos.
        

    """
    valid=[]
    for b in range(1,11):
        
        dff=df.loc[df['name_gateway'] == b]
        dff=dff.iloc[:,[2,4,5]]
        dff=dff.drop_duplicates(subset = ['sensorID'])
        v4 = list(dff.isna().sum())
        if v4[1] > 0 or v4[2]>0:
            valid.append(False)
        else: 
            valid.append(True)
    return valid

# Quinta coluna: Porcentagem de sensores com a coluna correta em cada dispositivo
def column_5(df):
    """
    A função calcula para cada dispisitivo quantos sensores estão devidamente configurados.
    Ela irá filtrar a tabela completa para cada um dos gateways e depois retirar os valores
    duplicados de acordo com os sensores e transforma isso num primeiro objeto. Em seguida,
    vai retirar as linhas em que as colunas start ou frequency forem nulas e transformar 
    isso em um segundo objeto. Finalmente fará uma divisão do número de linhas do 
    segundo objeto pelo número de linhas do primeiro objeto vezes cem.

    Parameters
    ----------
    df : full_df:dataset completo após o merge
        DESCRIPTION.

    Returns
    -------
    valid : Lista:float
        Será retornado uma lista de valores inteiro que representam a porcentagem dos
    sensores devidamente configurados seguindo a ordem de numeração dos dispositivos.

    """
    valid=[]
    for b in range(1,11):
        
        dff=df.loc[df['name_gateway'] == b]
        dff=dff.drop_duplicates(subset = ['sensorID'])
        dff2=dff.dropna(subset = ['start','frequency'])
        value=round(len(dff2)/len(dff),2)*100
        valid.append(value)
    return valid

# Sexta coluna: Ainda montando
def column_6(df):
    """
    A função irá levantar a quantidade de medições que cada dispostivo recebe no intervalo
    de 24 horas de acordo com as suas configurações. Ela faz filtragem de acordo com o
    gateway, retira as linhas duplicadas de acordo com o sensorID e retira as linhas nulas
    pela coluna start. Em seguida é criado um time delta de 24 horas que será subtraída
    pela hora da primeira medição do sensor (valor especificado na coluna start). O valor
    dessa subtração representa as horas restantes que o sensor tem para fazer as medições.
    Esse valor será dividido pelo valor de frequency, resultando no número de vezes que o
    sensor conseguirá fazer medições nas suas 24 horas restantes. Esse numéro será decimal 
    e precisará ser arredondado para baixo (pois se o sensor não completar todo o espaço
    de tempo do seu intervalo ele não fará a medição.) Por fim, o numéro de vezes que os 
    sensores fazem as medições serão somados de acordo com o seu gateway

    Parameters
    ----------
    df : full_df:dataset completo após o merge
        As colunas necessárias aqui são as name_gateway, sensorID, start (com valores nulos
        limpos e frequency (com valores limpos).

    Returns
    -------
    valid : Lista:float
        Será retornado uma lista com o número de medições que cada dispositivo recebe
        em 24 horas, seguindo a ordem de numeração dos dispositivos.

    """
    valid=[]
    for b in range(1,11):
        dff = df.loc[df['name_gateway'] == b]
        dff.drop_duplicates(subset = ['sensorID'], inplace=True)
        dff.dropna(subset = ['start'], inplace=True)
        delta = timedelta(hours=24)
        dff['start1'] = dff['start'].apply(lambda x:delta - timedelta(hours=x.hour,minutes=x.minute))
        dff['start1'] = round(dff['start1']/dff['frequency'] -0.5)
        valid.append(dff['start1'].sum())
    return valid

def column_7(df):
    """
    A função filtra planilha completa de acordo com o dispositivo gateway. Em seguida
    tira os valores duplicados de acordo com a coluna sensorID e limpa as linhas
    com valores nulos pela coluna signal. Um valor médio da sinal é calculado representando
    seu respectivo gateway.

    Parameters
    ----------
    df : full_df:dataset completo após o merge
        DESCRIPTION.

    Returns
    -------
    valid : lista:float
        Retornado uma lista com o valor média do sinal dos sensores de cada um dos 
        dispositivos seguindo a ordem de numeração dos gateways.

    """
    valid=[]
    for b in range(1,11):
      dff=df.loc[df['name_gateway'] == b]
      dff.drop_duplicates(subset = ['sensorID'], inplace=True)
      dff.dropna(subset = ['signal'], inplace=True)
      valid.append(round(dff['signal'].mean(),2))
    return valid

# Oitava coluna: Classificando a média do sinal dos sensores dos dispotivos
def column_8(df):  
    """
    A função vai criar uma coluna em dataframe com os valores referentes a qualidade do sinal que foi foi plotado
    na coluna signal_mean_value da tabela final 

    Parameters
    ----------
    df : final_df: Tabela final construinda com o uso das outras funções ao longo funções anteriores
        A tabela final_df pode ser simplesmente aplicada dentro da função.

    Returns
    -------
    df : final_df: DataFrame
        A função retornará a mesma tabela que foi aplicada, apenas acrescentando uma coluna extra. 

    """
    df.loc[df['signal_mean_value'] < (-100.00), 'signal_status'] = 'Ruim' 
    df.loc[(df['signal_mean_value'] >= -100.00) & (df['signal_mean_value'] < -90.00), 'signal_status'] = 'Regular' 
    df.loc[df['signal_mean_value'] >= -90.00, 'signal_status'] = 'Bom'  
    return df

# Nona coluna: Quantidade de sensores que não estão configurados nos dispositivos
def column_9(df):
    """
    A função conta quantos sensores de cada dispositivo não estão registrando a intensidade
    do sinal. Ela separa a tabela de acordo com o gateway, tira as linhas duplicadas dentro da coluna
    sensorID e soma a quantidade de sensores com valor NaN no campo da coluna sinal para cada gateway.

    Parameters
    ----------
    df : full_df:dataset completo após o merge
        DESCRIPTION.

    Returns
    -------
    valid : lista:int
        A função retorna uma lista com o número de sensores com sinal ausente, seguindo a ordem de numeração
    dos gateways.

    """
    valid=[]
    for b in range(1,11):
      
      dff=df.loc[df['name_gateway'] == b]
      dff.drop_duplicates(subset = ['sensorID'], inplace=True)
      valid.append(dff.iloc[:,6].isna().sum())
    return valid

# Décima coluna: Número de dias decorridos desde a última coleta dos sensores
def column_10(df):
    """
    A função separa a tabela de acordo com o gateway e trabalha com a coluna datetime que registra as datas das
    medições de todos os sensores em seus respectivos dispositivos. Primeiro faz uma remoção das informações de fuso
    horário que estão nas células de datetime para facilitar a leitura pelo códigos seguintes. Em seguinda,
    a função acha a linha cuja a data indica a medição mais recente e a subtrai pela data do dia em que
    a função está executada. 

    Parameters
    ----------
    df : full_df:dataset completo após o merge
        DESCRIPTION.

    Returns
    -------
    valid : Lista: timedelta
        A função retorna uma lista com o intervalo de tempo entre o dia em que a função foi executada e a data
        da medição mais recente de cada dispostivo.

    """
    valid=[]    
    for b in range(1,11):
      dff=df.loc[df['name_gateway']== b]
      dff['datetime'] = dff['datetime'].apply(lambda x: x.replace(tzinfo = None))
      value = dt.datetime.now() - dff['datetime'].max()
      valid.append(value)
    return valid

# Décima primeira coluna: Classificando o sinal dos dispositivos de acordo com o tempo em que foi coletado
def column_11(df):
    """
    A função cria um timedelta de 60 dias e e comparara com a coluna elapsed_time_since_last_measurument.
    Assim cria uma classificação para saber se as medições mais recentes dos gateways foram
    feitas antes ou depois de 60 dias.

    Parameters
    ----------
    df : final_df: Tabela final construinda com o uso das outras funções ao longo funções anteriores
        DESCRIPTION.

    Returns
    -------
    valid: final_df: DataFrame
           A função retornará a mesma tabela que foi aplicada, apenas acrescentando uma coluna extra.

    """
    day_60=timedelta(days=60)
    df['measurement_status'] = df['elapsed_time_since_last_measurement'].apply(lambda x: 'coletado há mais de 60 dias' if x >= day_60 else 'coletado nos ultimos 60 dias')
    df.loc[df['elapsed_time_since_last_measurement'].isnull(), 'measurement_status'] = 'nunca coletado'
    return df