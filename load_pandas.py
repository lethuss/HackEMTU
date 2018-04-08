import pandas, os

'''Lista todos dados dentro do diretorio "2017"'''
files = [os.path.join(dp, f)
         for dp, dn, fn in os.walk(os.path.expanduser("2017/07/"))
            for f in fn]
clean_files = [file for file in files if r'.csv' in file][:100]

result_dataframe = pandas.DataFrame(columns=['latitude', 'longitude', 'prefixoVeiculo', 'timestampModulo'])
for file in clean_files:
    for chunk in pandas.read_csv(file, engine='python', chunksize=10):
        chunk = chunk.drop(
'id,version,alertaAutorizacao,alertaForaDeRota,alertaInspecao,alertaPanico,alertaSemPontosCarregados,alertaTempoParado,alertaVelocidade,audioMudo,bateriaConectada,codigoLinha,codigoLinhaPlan,codigoRetorno,codigoTeclaTd,dentroRota,difGeracaoProc,difPontos,direcao,distanciaPonto,emPonto,entradaPonto,evAbriuViagem,evChegada,evFechouViagem,evPartida,evPassagemPonto,gprsOnline,gpsValido,hodometro,idPontoAprox,idRota,ignicaoLigada,linhaValidador,numSequenciaModulo,placaVeiculo,pontoAnterior,pontoGaragem,qtdPassageirosValidador,qtdSatelitesGPS,saidaPonto,sensorPortaEntradaAberta,sensorPortaSaidaAberta,sentido,sentidoValidador,seqPonto,seqPontoAprox,seqUltimoPonto,seqViagem,serialModulo,serialValidador,sinalGSM,statusVeiculo,tdConectado,temperatura,tensao,timestampProc,timestampValidador,validadorConectado,velocidade,velocidadeMedia,viagemAberta'.split(','), axis=1)
        result_dataframe = pandas.concat([result_dataframe, chunk])
print("Transmissoes carregadas")

dataframe_bilhetagem = pandas.DataFrame(columns=['cartao', 'timestampModulo', 'Linha', 'prefixoVeiculo'])
for chunk in pandas.read_csv('merged.csv', engine='python', delimiter=';',
                             chunksize=443, header=0, index_col=0,
                             usecols=['cartao', 'timestampModulo', 'Linha', 'prefixoVeiculo', 'sentido', 'tipo'],
                           names=['cartao', 'timestampModulo', 'Linha', 'sentido', 'tipo', 'prefixoVeiculo']):
    dataframe_bilhetagem = pandas.concat([dataframe_bilhetagem, chunk])

    day = str(chunk.head(1)['timestampModulo'])


    if day[19:21].strip() == '07':
        dataframe_bilhetagem = pandas.concat([dataframe_bilhetagem, chunk])
print("Bilhetagem carregada")

result_dataframe['timestampModulo'] = pandas.to_datetime(result_dataframe.timestampModulo)
dataframe_bilhetagem['timestampModulo'] = pandas.to_datetime(dataframe_bilhetagem.timestampModulo)
result_dataframe.sort_values('timestampModulo', inplace=True)
dataframe_bilhetagem.sort_values('timestampModulo', inplace=True)
aux = []
for time in dataframe_bilhetagem['timestampModulo']:
    index = result_dataframe['timestampModulo'].searchsorted(time)[0]
    time_delta = pandas.Timedelta('10s')
    if list(result_dataframe['timestampModulo'])[index - 1] > time:
        index -= 1
    if list(result_dataframe['timestampModulo'])[index] - time >= time_delta >= time - list(result_dataframe['timestampModulo'])[index - 1]:
        aux.append(list(result_dataframe['timestampModulo'])[index])
    else:
        aux.append(time)

aux_dataframe = pandas.DataFrame(aux, columns=['timestampModulo'])
dataframe_bilhetagem = dataframe_bilhetagem.drop(['timestampModulo'], axis=1)
dataframe_bilhetagem = pandas.concat([dataframe_bilhetagem, aux_dataframe], axis=1)
print("Tempo normalizado")

merged = result_dataframe.merge(dataframe_bilhetagem, on=['timestampModulo','prefixoVeiculo'])
