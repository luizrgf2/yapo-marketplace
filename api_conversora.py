import requests





def dolar_real(valor_dolar:float):

    resposta = requests.get('https://www.google.com/search?q=pre%C3%A7o+dolar&sxsrf=ALeKk03jZmajJotkZ_B4B8AkzuJLVXWzTg%3A1617294963197&ei=c_ZlYJfAC6XD5OUPs6WtsA8&oq=pre%C3%A7o+dola&gs_lcp=Cgdnd3Mtd2l6EAMYADIFCAAQsQMyBQgAELEDMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6BwgAEEcQsAM6BAgjECc6BAgAEEM6CAguELEDEIMBOgUILhCxAzoICAAQsQMQgwE6BwguELEDEEM6CQgjECcQRhD5AToKCAAQsQMQgwEQQzoHCAAQyQMQQzoHCAAQsQMQQzoPCAAQsQMQgwEQQxBGEIICUKM_WKFLYKBTaANwAngAgAHeAYgBzBGSAQUwLjMuOJgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=gws-wiz')
    
    text_init = resposta.text.split('class="BNeawe iBp4i AP7Wnd"><div><div class="BNeawe iBp4i AP7Wnd">')[1].split(' Real brasileiro</div></div>')[0]

    valor_final = float(text_init.split(',')[0]+'.'+text_init.split(',')[1])

    print(valor_final)

    valor_aux = float(valor_dolar*valor_final).real

    valor_string = ''
    try:
        valor_string = str(valor_aux).split('.')[0]+','+str(valor_aux).split('.')[1]+'.'+str(valor_aux).split('.')[2]
    except:
        valor_string = str(valor_aux).split('.')[0]+','+str(valor_aux).split('.')[1]
    return valor_string
