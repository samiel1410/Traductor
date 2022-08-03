from django.shortcuts import render
from django.http import HttpResponse
import requests, uuid, json, xmltodict, numpy
import collections


def traductor(request,cadena):
    cadenaLim = cadena# Limpieza de cadena de texto

# Llave de suscripcion
    subscription_key = "df29dad4900e48588eef8b0f94d74934"
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = "eastus"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': ['en'],  # idioma
        'includeAlignment': 'true'  # alinieamiento
    }

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        # entrada de cadena
        'text': cadenaLim
    }]
    # parametros
    request = requests.post(constructed_url, params=params, headers=headers, json=body)

    resultado1 = request.json()

    # impresion de la traduccion y alineamiento
    for tra in resultado1:
        alineamiento = tra['translations'][0]['alignment']['proj']
        resul = tra['translations'][0]['text']
    print("Alineamiento:", alineamiento)
    print("Traduccion:", resul)

    # transformacion en un array para mejor uso
    string_list = alineamiento.split()
    arry = numpy.array(string_list)
    # print(string_list)
    contador = numpy.size(arry)
    # print(contador)


    arry_ali=[]
    remplazo = alineamiento.replace(" ", "-").replace(":", "-")
    separados = remplazo.split("-")



    # print(separados)
    # print(cadena)
    # print(resul)
    # espanol=list(cadenaLim)
    ingles=list(resul)


    # funcion para tokenizar el alineamiento

    test_list2 = separados
    #print("Test",test_list2, "tamanio",len(test_list2))
    int_list = list(map(int, test_list2))
    #print("Lista Nueva",int_list)
    # print(test_list2.replace("'"," "))
    test1=[]
    for i in range(len(test_list2)):
        test1.append(int(test_list2[i]))


    n = 2

    output = [test1[i:i + n] for i in range(0, len(test1), n)]




    # Enviar cadena de texto en ingles al metamap
    data = {
        'data': resul,
    }

    response2 = requests.post('http://localhost:80/metamap', data=data)
    # transformar resultados de xml a json
    datos = xmltodict.parse(response2.text)
    json_object = json.dumps(datos)
    #print("Metamap............")
    #print(json_object)

    p = json.loads(json_object)


    ############################################
    def contador(iterable):
        contador_array = []

        if type(iterable) is not str:
            if type(iterable) is dict:
                for k, v, in iterable.items():
                    if k == 'MappingCandidates':
                        contador_array.append(v)
                    else:
                        contador_array.extend(contador(v))
            elif type(iterable) is list:
                for x in iterable:
                    contador_array.extend(contador(x))

        return contador_array


    count_array = []
    for contador_array in contador(p):
        count_array.append(contador_array)

    count_array_num = numpy.size(count_array)
    count = 0
    for i in range(count_array_num):
        count = count + int(count_array[i]['@Total'])
        #print("COntador", count)


    ###############################################
    def PosLen(iterable):
        poslen = []

        if type(iterable) is not str:
            if type(iterable) is dict:
                for k, v, in iterable.items():
                    if k == 'ConceptPIs':
                        poslen.append(v)
                    else:
                        poslen.extend(PosLen(v))
            elif type(iterable) is list:
                for x in iterable:
                    poslen.extend(PosLen(x))

        return poslen


    poslen_array = []
    for poslen in PosLen(p):
        poslen_array.append(poslen)
        #print("POS_ARRAY",poslen_array)

    count_poslen = numpy.size(poslen_array)

    ###################################

    ingles = resul
    espanol = cadenaLim

    pos = []
    leng = []
    posleng = []
    in_ingles = []
    fin_ingles = []
    posi_uni = []
    pala_com=[]
    star=[]
    leng2=[]
    q =2
    pos_star_in=[]
    pos_fin_in=[]
    pos_ing=[]
    var100=0
    var_contador_unido=0
    ingles_mas=[]
    ingles_mas_unido=[]
    #print("Tamanio POS",count_poslen)
    for i in range((count_poslen)):
        #print("COUNT",poslen_array[i]['@Count'])
        var12=i
    # print("VAI",i)
        va122 = poslen_array[i]['ConceptPI']

        if (int(poslen_array[i]['@Count']) == 1):
            #print("POS_STAR", poslen_array[i]['ConceptPI'])

            pos.append(poslen_array[i]['ConceptPI']['StartPos'])
            leng.append(poslen_array[i]['ConceptPI']['Length'])
            #print("POSSSS",pos,"LENG",leng)

            posleng.append(int(pos[var100]) + int(leng[var100]))

            ingles_array = ingles[int(pos[var100]):int(posleng[var100])]
            #print("Palabra en ingles:", ingles[int(pos[var100]):int(posleng[var100])])
            in_ingles.append(pos[var100])
            fin_ingles.append(int(pos[var100]) + int(leng[var100]) - 1)
                # print("Ingles:",fin_ingles)
            #print("Nueva1:", in_ingles[var100])
            #print("Nueva2:", fin_ingles[var100])
                # print("Array:",ingles_array.split())
            posi_uni.append(int(in_ingles[var100]))
            posi_uni.append(fin_ingles[var100])
            #print("PPP", posi_uni)
            pala_com.append(ingles_array)
            #print("Pala", pala_com)
            var100 += 1



        if(int(poslen_array[i]['@Count'])>1):
            var_count=int(poslen_array[i]['@Count'])

            for x in range(var_count):
                #print("POS_STAR",poslen_array[i]['ConceptPI'])
                star.append(poslen_array[i]['ConceptPI'][x]['StartPos'])
                leng2.append(poslen_array[i]['ConceptPI'][x]['Length'])

                #print("POS-LENG",star[x],leng2[x])
                pos_star_in.append(int(star[x]))
                pos_fin_in.append(int(star[x]) + int(leng2[x]))
                ingles_mas.append(ingles[int(pos_star_in[x]):int(pos_fin_in[x])])
                pos_ing.append(pos_star_in[x])
                pos_ing.append(pos_fin_in[x])

            #print("Ingles_mas", ingles_mas)
            salida_unidas = [ingles_mas[i:i + q] for i in range(0, len(ingles_mas), q)]
            ingles_mas_unido.append(" ".join(salida_unidas[var_contador_unido]))
            #print(ingles_mas_unido)
            pala_com.append(ingles_mas_unido[var_contador_unido]) #cambiar para funcionar con mas casos , usar funcion salida1 para separar
            var_contador_unido+=1
            salida1 = [pos_ing[i:i + q] for i in range(0, len(pos_ing), q)]
            for i in range(var_count):
                posi_uni.append(salida1[i])




    salida = [posi_uni[i:i + q] for i in range(0, len(posi_uni), q)]



    #################################################################################
    #Creacion de Diccionario##############
    var =ingles_array.split()





    ###############################
    ############CandidateCUI#####################
    def CandidateCUI(iterable):
        candidate_cui = []

        if type(iterable) is not str:
            if type(iterable) is dict:
                for k, v, in iterable.items():
                    if k == 'CandidateCUI':
                        candidate_cui.append(v)
                    else:
                        candidate_cui.extend(CandidateCUI(v))
            elif type(iterable) is list:
                for x in iterable:
                    candidate_cui.extend(CandidateCUI(x))

        return candidate_cui


    candidate_cui_array = []
    for candidate_cui in CandidateCUI(p):
        candidate_cui_array.append(candidate_cui)

    count = numpy.size(candidate_cui_array)


    ######################################################
    ##################CandidateMatched#####################
    def CandidateMatched(iterable):
        candidate_matched = []

        if type(iterable) is not str:
            if type(iterable) is dict:
                for k, v, in iterable.items():
                    if k == 'CandidateMatched':
                        candidate_matched.append(v)
                    else:
                        candidate_matched.extend(CandidateMatched(v))
            elif type(iterable) is list:
                for x in iterable:
                    candidate_matched.extend(CandidateMatched(x))

        return candidate_matched


    candidate_matched_array = []
    for candidate_matched in CandidateMatched(p):
        candidate_matched_array.append(candidate_matched)


    ##############################################
    #####################CandidateScore###############
    def CandidateScore(iterable):
        candidate_score = []

        if type(iterable) is not str:
            if type(iterable) is dict:
                for k, v, in iterable.items():
                    if k == 'CandidateScore':
                        candidate_score.append(v)
                    else:
                        candidate_score.extend(CandidateScore(v))
            elif type(iterable) is list:
                for x in iterable:
                    candidate_score.extend(CandidateScore(x))

        return candidate_score


    candidate_score_array = []
    for candidate_score in CandidateScore(p):
        candidate_score_array.append(candidate_score)


    ########################
    def one(iterable):
        ones = []

        if type(iterable) is not str:
            if type(iterable) is dict:
                for k, v, in iterable.items():
                    if k == 'Candidate':
                        ones.append(v)
                    else:
                        ones.extend(one(v))
            elif type(iterable) is list:
                for x in iterable:
                    ones.extend(one(x))

        return ones



    #############################
    c=2
    mylist1=[]
    for i in range(len(pala_com)):
        mylist1.append(pala_com[i])
        mylist1.append(salida[i])
    #print("Mi Lista",mylist1)

    salida_lista1 = [mylist1[i:i + c] for i in range(0, len(mylist1), c)]
    #print(salida_lista1)


    mylist2=[]
    for i in range(len(pala_com)):
        mylist2.append(pala_com[i])
        mylist2.append(candidate_cui_array[i])
    #print("Mi Lista2",mylist2)


    salida_lista2 = [mylist2[i:i + c] for i in range(0, len(mylist2), c)]
    #print(salida_lista2)

    mylist3=[]
    for i in range(len(pala_com)):
        mylist3.append(pala_com[i])
        mylist3.append(int(poslen_array[i]['@Count']))
    #print("Mi Lista3",mylist3)

    salida_lista3 = [mylist3[i:i + c] for i in range(0, len(mylist3), c)]
    #print(salida_lista3)
    print()

    mylist4=[]
    for i in range(len(pala_com)):
        #print("CAndiadte",candidate_matched_array[i])
        mylist4.append(pala_com[i])
        mylist4.append(candidate_matched_array[i])
    #print("Mi Lista4",mylist4)

    salida_lista4 = [mylist4[i:i + c] for i in range(0, len(mylist4), c)]
    #print(salida_lista4)



    ######################eliminar datos duplicado############

    resultantList_palabras = []
    resultantList_codigo = []
    resultantList_tamanio_pos = []
    resultantList_pala_com=[]
    resultantList_coincidencia=[]
    for element in salida_lista1:
        if element not in resultantList_palabras:
            resultantList_palabras.append(element)
    #print("Palabras COmbinadas",resultantList_palabras)
    for element in salida_lista3:
        if element not in resultantList_tamanio_pos:
            resultantList_tamanio_pos.append(element)

    for element in salida_lista2:
        if element not in resultantList_codigo:
                resultantList_codigo.append(element)
    #print("lista3",resultantList_tamanio_pos)


    #######################################################
    for element in pala_com:
        if element not in resultantList_pala_com:
                resultantList_pala_com.append(element)

    for element in salida_lista4:
        if element not in resultantList_coincidencia:
                resultantList_coincidencia.append(element)


    ######################Codigo Unidos########################


    codigo_unidos = collections.defaultdict(list)

    for k, v in resultantList_codigo:
        codigo_unidos[k].append(v)
    #####################Palabras Unidads########################

    palabras_pos_unidas = collections.defaultdict(list)
    for k, v in resultantList_palabras:
        palabras_pos_unidas[k].append(v)
    #####################Coincidencia Unida########################
    coincidencia_unidos = collections.defaultdict(list)
    for k, v in resultantList_coincidencia:
        coincidencia_unidos[k].append(v)

    ###################Codigo para saber los corchetes############
    arry=[]
    trasnformados_str=[]
    va=0
    for i in range(len(resultantList_pala_com)):
        trasnformados_str.append(str(palabras_pos_unidas[resultantList_pala_com[i]]))

    for e in range(len(resultantList_pala_com)):
        pala=trasnformados_str[e]
        for n in range(len(trasnformados_str[e])):
            if (pala[n] == '['):
                va = va + 1
            else:
                break
        arry.append(va)
        va = 0
    ###################Segundo codigo para contar ########################



    #############################
    tama = []
    array_final=[]
    #print("AA22",len(var))

    w=2
    salida_int = [int_list[i:i + w] for i in range(0, len(int_list), w)]





    array_posicones_bus=[]
    #########################################
    array_posicones_bus = []
    
    tamanio_palabras = []
    var_tamanio=0
    pos_unidas_bus=[]
   
    arrray_pala_pos=[]
    
  
    posicion_final=[]

    array_auxiliar=[]
    for i in range(len(resultantList_pala_com)):
        var_x=resultantList_pala_com[i].split()
        var_y=palabras_pos_unidas[resultantList_pala_com[i]]
        posicion_final.append(var_y)
        va_n=var_y[0][0]
        if (len(resultantList_pala_com[i].split()) == 1):
            array_posicones_bus.append((resultantList_palabras[i][1]))
            arrray_pala_pos.append(resultantList_pala_com[i])
            arrray_pala_pos.append(resultantList_palabras[i][1])
        if (len(resultantList_pala_com[i].split()) > 1):
            arrray_pala_pos.append(resultantList_pala_com[i])
            #print(resultantList_pala_com[i], resultantList_palabras[i][1])
            palabras_sepa = resultantList_pala_com[i].split()
            #print("Palabras",palabras_sepa)
            for a in range(1):
                #print("VariableA",a)
                #print("PalabrasTamanio", len(palabras_sepa[a])-1)
                var_palabras=len(palabras_sepa)
                for x in range(var_palabras):
                    tamanio_palabras.append(len(palabras_sepa[x]))
                    salida_posi = [tamanio_palabras[:i + 1] for i in range(0, len(tamanio_palabras), 1)]
                    #print("Salida Posicion", salida_posi)
                #print(int(resultantList_tamanio_pos[i][1]))

                if(arry[i]==2):
                    var_suma_pos=int(len(palabras_pos_unidas[resultantList_pala_com[i]]))
                    var_suma_tamanio = int(len(palabras_pos_unidas[resultantList_pala_com[i]])) + 2
                    #print("var_suma_tamanio1",var_suma_tamanio)
                elif(arry[i]==3):
                    var_aux2=palabras_pos_unidas[resultantList_pala_com[i]]
                    #print(var_aux2[0][0])
                    var_suma_pos=int(len(var_aux2[0]))
                    #print(var_suma_pos)
                    var_suma_tamanio = (int(len(var_aux2[0]))*2)-1
                    #print("var_suma_tamanio2", var_suma_tamanio)



                for c in range(var_suma_pos):
                    var_n=var_suma_pos
                    #print("C",c)
                    var_aux = palabras_pos_unidas[resultantList_pala_com[i]]
                    if (arry[i] == 2):
                        #print("C", c)
                        pos_unidas_bus.append(var_aux[0][0])

                    else:
                        pos_unidas_bus.append(var_aux[0][c][0])



                    for b in range(var_suma_tamanio):
                        #print("C", c)

                        #print("VariableB", b,var_tamanio)
                        #print(pos_unidas_bus)
                        if (b % 2 == 0):
                            #print("Par",var_tamanio)
                            pos_unidas_bus.append(pos_unidas_bus[b] + int(tamanio_palabras[var_tamanio])-1)
                            var_tamanio += 1
                            #print(pos_unidas_bus)

                        else:
                            #print("Impar")
                            pos_unidas_bus.append(pos_unidas_bus[b] + 2)
                            #print(pos_unidas_bus)



                    for l in range(len(pos_unidas_bus)):
                        array_auxiliar.append(pos_unidas_bus[l])
                    pos_unidas_bus=[]

                    #print("C", c)
                    var_tamanio = 0
                    p#rint("C", c)

                tamanio_palabras.clear()


            for t in range(len(array_auxiliar)):
                array_final.append(array_auxiliar[t])
            array_auxiliar=[]


            salida_datos_agru = [array_final[i:i + q] for i in range(0, len(array_final), q)]

            arrray_pala_pos.append(salida_datos_agru)

            array_final.clear()

            #print("SALIDA", salida_datos_agru)
            salida_datos_agru=[]





    ###################FUncion busqueda de Plaabara###############

    array_final2=[]
    for i in range(len(arrray_pala_pos)):
        if(i%2==1):
            array_final2.append(arrray_pala_pos[i])


    arry2=[]
    va2=0
    for i in range(len(array_final2)):
        x=len(str(array_final2[i]))
        y=str(array_final2[i])
        for j in range(x):
            if(y[j]=='['):
                va2 = va2 + 1
            else:
                break
        arry2.append(va2)
        va2 = 0
    array_tama=[]
    for i in range(len(arry2)):
        if(arry2[i]>1):
            array_tama.append(len(array_final2[i]))
        else:
            array_tama.append(1)
    #print(array_final2)
    array_posi_enco=[]
    array_posi_enco_aux=[]


    for i in range(len(array_final2)):
        m=array_final2[i]
    # print(m)
        #print(array_tama[i])
        if(array_tama[i]>1):
            for j in range(len(m)):
            # print(m[j],len(m[j]))
                if(int(len(m[j]))>1):
                # print(m[j])
                    indices = [a for a in range(len(output)) if output[a] == m[j]]
                    array_posi_enco_aux.append(indices)
                else:
                    array_posi_enco_aux.append([])
            array_posi_enco.append(array_posi_enco_aux)
            array_posi_enco_aux = []
        else:
            indices = [a for a in range(len(output)) if output[a] == m]
            array_posi_enco.append(indices)

    array_espanol=[]
    array_espanol_aux=[]
    var_contador=0
    for i in range(len(array_posi_enco)):
        if (arry2[i] > 1):

            for j in range(len(array_posi_enco[i])):
                #print(array_posi_enco[i])
                x = array_posi_enco[i][var_contador]
                #print("X",x,len(x))
                if(len(x)>=1):

                    #print(int(x[0]))
                    posicion_espanol=output[int(x[0])-1]
                    #print(posicion_espanol)
                    #print("uni:",posicion_espanol[0],"dos",posicion_espanol[1])
                    espanol=cadena[posicion_espanol[0]:posicion_espanol[1]+1]
                    #print(espanol)
                    array_espanol_aux.append(espanol)
                    var_contador+=1



            array_espanol.append(array_espanol_aux)
            array_espanol_aux = []
            var_contador = 0
        else:
            x = array_posi_enco[i]
            if(len(x)>=1):

                posicion_espanol = output[int(x[0]) - 1]
                #print(posicion_espanol)
                #print("uni:", posicion_espanol[0], "dos", posicion_espanol[1])
                espanol = cadena[posicion_espanol[0]:posicion_espanol[1]+1]
                #print(espanol)
                array_espanol.append(espanol)
            else:
                array_espanol.append("--")
    ingles_finales=[]
    codigos_finales=[]
    espanol_finales=[]

    for i in range(len(resultantList_pala_com)):
        print("Palabra #", i + 1)

        print("Palabra en ingles:", resultantList_pala_com[i] )###borrrar palabras repetidas
        ingles_finales.append(resultantList_pala_com[i])


        if (arry2[i] > 1):
            print("Palabras en español:", " ".join(array_espanol[i]))
            espanol_finales.append(" ".join(array_espanol[i]))
        else:
            print("Palabras en español:", array_espanol[i])
            espanol_finales.append(array_espanol[i])

            # print("Alineniamiento:",ali[i][0],"-",ali[i][1])
        print("Codigo:", codigo_unidos[resultantList_pala_com[i]])
        codigos_finales.append(codigo_unidos[resultantList_pala_com[i]])
        print("Coincidencia:", coincidencia_unidos[resultantList_pala_com[i]])
        print("Porcentaje de Coincidencia:", candidate_score_array[i])

    data = {}
    data['datos'] = []
    for i in range(len(ingles_finales)):
        data['datos'].append({
        'entidad': espanol_finales[i],
        'codigo': codigos_finales[i],
        'posicion':posicion_final[i]
        })
    print("DATA",data)
    contexto=data['datos']
    return contexto