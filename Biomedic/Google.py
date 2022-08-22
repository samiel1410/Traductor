import uuid

import requests
from requests.structures import CaseInsensitiveDict

import Parametros


def all(alineamiento, resul, output, cadena):

    url = "https://healthcare.googleapis.com/v1/projects/proyecto-5e4b9/locations/us-central1/services/nlp:analyzeEntities"

    remplazo = alineamiento.replace(" ", "-").replace(":", "-")
    separados = remplazo.split("-")

    test_list2 = separados
    test1=[]
    for i in range(len(test_list2)):
        test1.append(int(test_list2[i]))

    n = 2

    output = [test1[i:i + n] for i in range(0, len(test1), n)]
    ali = output



    data2="'"+resul+"'"
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer ya29.A0AVA9y1uCwHETr1HQbSqsIsZk-xjb-wax0KJmvjcgbfwKj8vLz2vzEoopQMYSRUAS710kOvn6P0L6xpvbaNqnd5ZUZ9qFvTlxwpzMGtNvhDwIUMM8LJDiyUnBAoPs0qE0h2YP6VDtKyfLnDRKKHVc3IKnVsg_rwY8C-YbnmDsjybUMoEwEtAnKqFdxbDu0tbl4HtFfSv1uR21VRLTXCnRJO0FZgRVRqfUPgTBJUQStPhs2Vna7xIhj1T38lBrhaff8nED2gaCgYKATASATASFQE65dr8E2Frg4WpcQX_DYqZoiTlUg0269"
    headers["Content-Type"] = "application/json"

    data = """
    {
        'nlpService':'projects/proyecto-5e4b9/locations/us-central1/services/nlp',
        'documentContent':"""+data2+"""
       }
    """


    resp = requests.post(url, headers=headers, data=data)

    #print(resp.json())
    respuesta=resp.json()

    def entityMentions(iterable):
        entity = []

        if type(iterable) is not str:
            if type(iterable) is dict:
                for k, v, in iterable.items():
                    if k == 'entityMentions':
                        entity.append(v)
                    else:
                        entity.extend(entityMentions(v))
            elif type(iterable) is list:
                for x in iterable:
                    entity.extend(entityMentions(x))

        return entity


    entity_array = []
    for candidate_matched in entityMentions(respuesta):
        entity_array.append(candidate_matched)

    array_cui=[]
    array_cui_aux=[]
    for i in range(len(entity_array[0])):
        x='linkedEntities' in entity_array[0][i]
        #print(x)
        if(x ==True):
            for j in range(len(entity_array[0][i]['linkedEntities'])):
                #print(entity_array[0][i]['linkedEntities'][j]['entityId'])
                array_cui_aux.append(entity_array[0][i]['linkedEntities'][j]['entityId'])
            array_cui.append(array_cui_aux)
            array_cui_aux=[]
        else:
            array_cui.append("No hay UMLS")



    ###########FUncion calcular posicion ingles#############
    array_pos=[]
    array_tamanio=[]
    array_tamanio_aux=[]
    posiciones=[]

    for i in range(len(entity_array[0])):
        tamanio_aux = entity_array[0][i]['text']['content']
        if(len(tamanio_aux.split())>1):
            aux=tamanio_aux.split()
            for j in range(len(tamanio_aux.split())):
                array_tamanio_aux.append(len(aux[j]))
            array_tamanio.append(array_tamanio_aux)
            array_tamanio_aux=[]
        else:
            array_tamanio_aux.append(len(tamanio_aux))
            array_tamanio.append(array_tamanio_aux)
            array_tamanio_aux=[]

    for i in range(len(entity_array[0])):
        tamanio_aux=entity_array[0][i]['text']['content']
        array_pos.append(int(entity_array[0][i]['text']['beginOffset']))
    array_busqueda=[]
    array_busqueda_aux=[]
    var_tamanio=0
    bucle1=0
    bucle2=0



    for i in range(len(entity_array[0])):
        if(len(array_tamanio[i])>1):
            array_busqueda_aux.append(array_pos[i])
            #print(array_tamanio[i],len(array_tamanio[i]))
            n=(len(array_tamanio[i])*2)-1
            for j in range(n):
                if(j% 2 == 0):
                    array_busqueda_aux.append(array_busqueda_aux[j]+int(array_tamanio[i][var_tamanio])-1)
                    var_tamanio+=1
                    #bucle1 += 1
                else:
                    array_busqueda_aux.append(array_busqueda_aux[j]+2)
            array_busqueda.append(array_busqueda_aux)
            array_busqueda_aux=[]
            var_tamanio=0
        else:
            array_busqueda_aux.append(array_pos[i])
            array_busqueda_aux.append(array_busqueda_aux[0]+int(array_tamanio[i][0]-1))
            array_busqueda.append(array_busqueda_aux)
            array_busqueda_aux = []
            bucle2+=1
    bucle=0
    array_bus_pos=[]
    for i in range(len(array_busqueda)):
        if(len(array_busqueda[i])>2):
            aux=array_busqueda[i]
            w = 2
            salida_int = [aux[i:i + w] for i in range(0, len(aux), w)]
            array_bus_pos.append(salida_int)
        else:
            aux=array_busqueda[i]
            array_bus_pos.append(aux)

    arry=[]
    va=0
    for i in range(len(array_bus_pos)):
        x=len(str(array_bus_pos[i]))
        y=str(array_bus_pos[i])
        for j in range(x):
            if(y[j]=='['):
                va = va + 1
            else:
                break
        arry.append(va)
        va = 0



    array_posi_enco=[]
    array_posi_enco_aux=[]
    for i in range(len(array_bus_pos)):
        if(arry[i]>1):
            for j in range(len(array_bus_pos[i])):
                m=array_bus_pos[i][j]
                indices = [a for a in range(len(output)) if output[a] == array_bus_pos[i][j]]
                array_posi_enco_aux.append(indices)
            array_posi_enco.append(array_posi_enco_aux)
            array_posi_enco_aux=[]
        else:
            indices = [a for a in range(len(output)) if output[a] == array_bus_pos[i]]
            array_posi_enco.append(indices)


    array_espanol=[]
    array_espanol_aux=[]
    var_contador=0
    for i in range(len(array_posi_enco)):
        if (arry[i] > 1):

            for j in range(len(array_posi_enco[i])):

                x = array_posi_enco[i][var_contador]
                #print("X",x,len(x))
                if(len(x)>=1):
                    posicion_espanol=output[int(x[0])-1]
                    #print("uni:",posicion_espanol[0],"dos",posicion_espanol[1])
                    espanol=cadena[posicion_espanol[0]:posicion_espanol[1]+1]
                    array_espanol_aux.append(espanol)
                    var_contador+=1

            array_espanol.append(array_espanol_aux)
            array_espanol_aux = []
            var_contador = 0
        else:
            x = array_posi_enco[i]
            if(len(x)>=1):

                posicion_espanol = output[int(x[0]) - 1]

                #print("uni:", posicion_espanol[0], "dos", posicion_espanol[1])
                espanol = cadena[posicion_espanol[0]:posicion_espanol[1]+1]

                array_espanol.append(espanol)
            else:
                array_espanol.append("--")
    return entity_array,arry,array_espanol,array_cui,array_bus_pos


def imprimir(alineamiento, resul, output, cadena):
    entity_array, arry, array_espanol,array_cui,array_bus_pos=all(alineamiento, resul, output, cadena)
    entity_var=[]
    cui=[]
    for i in range(len(entity_array[0])):
        #print("Palabras #",i+1)
        #print("Palabras en ingles:",entity_array[0][i]['text']['content'])

        if(arry[i]==2):
            #print("Palabras en español:", " ".join(array_espanol[i]))
            entity_var.append(" ".join(array_espanol[i]))
        else:
            #print("Palabras en español:", array_espanol[i])
            entity_var.append(array_espanol[i])
        #print("Codigos:", array_cui[i])
        cui.append(array_cui[i])
        #print("Coincidenia:",entity_array[0][i]['type'])
        #print("Porcentaje de Coincidenia:", entity_array[0][i]['confidence'],"%")
    return entity_var,cui,array_bus_pos



