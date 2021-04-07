import requests
from api_conversora import dolar_real



def req(link):

    response= requests.get(link)


    text_editavel = response.text



   


    regiao_aux = text_editavel.split('<style>.seller-info__block-scroll { overflow: hidden !important }</style>')[1].split('storeurl=""')[0].split('region="')[1].split('"')[0]

    nome_vendedor = text_editavel.split("username='")[1].split("'")[0]
    estado = regiao_aux.split(',')[0]
    cidade = regiao_aux.split(',')[1]
    nome_anuncio = text_editavel.split("'Title': '")[1].split("'")[0]
    id_anuncio = text_editavel.split("'Ad ID': ")[1].split(',')[0]
    preco = 'R$ '+str(dolar_real(float(text_editavel.split('data-price="$ ')[1].split('"')[0])))
    image_link = 'https://img.yapo.cl/images'+text_editavel.split('<img src="https://img.yapo.cl/images')[1].split('" ')[0]
    

    return {


        'nome_vendedor':nome_vendedor,
        'estado':estado,
        'cidade':cidade,
        'nome_anuncio':nome_anuncio,
        'id_anuncio':id_anuncio,
        'preco':preco,
        'image_link':image_link
    }


