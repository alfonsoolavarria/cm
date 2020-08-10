from maracay.config import KEYSENDI, STRANS, SCONT
import requests


def sendinblue_contact(headers,nombre,apellido,telefono,direccion,email):
    contact = {
        "email":email,
        "emailBlacklisted":False,
        "smsBlacklisted":False,
        "listIds":[14],
        "updateEnabled":True,
        "attributes":{"Nombre":nombre, "Apellido":apellido, "telefono":telefono, "direccion":direccion}
    }
    requests.request("POST",SCONT,json=contact,headers=headers)


def sendinblue_send(template,email,nombre,apellido,extra=None):
    try:
        headers = {
            'accept': 'application/json',
            'api-key': KEYSENDI,
            'content-type': 'application/json',
            'content-length': '606',
            }
        params = {
            "email":email,"nombre":nombre,
            "apellido":apellido,
            }
        to = [{"email":email,"nombre":nombre}]


        if template == "registro":
            tempid = 1

        if template == "contacto":
            tempid = 2
            params = {
                "email":email,"asunto":extra['asunto'],
                "mensaje":extra['mensaje'],
                "codigo":extra['codigo'],
                "attachment":extra['attachment']
                }
            to = [{"email":"criollitosmarket@gmail.com","nombre":"admin"}]

        if template == "forgot":
            tempid = 4
            params = {
                "email":email,"token":extra['token'],
                }

        if template == "detallescompra":
            tempid = 5
            params = {
                "asunto":extra["asunto"],
                'payment_type':['payment_type'],
                'email':extra['email'],
                'carro':extra['carro'],
                'totalGeneral':extra['totalGeneral'],
                'totalCompleto':extra['totalCompleto'],
                'codigo':extra['codigo'],
                'costoEnvio':extra['costoEnvio'],
                'direction':extra['direction'],
            }


        transaction = {
            "to":to,
            # "subject": subject,
            "templateId":tempid,
            "params":params
            }
        response = requests.request("POST",STRANS,json=transaction,headers=headers)
        print("--->",response.status_code)
        print("--->",response.text)
        return response.text
    except Exception as e:
        print("sendinblue",e)


def sendinblue_get_bounce(email,templateId,eid,sid,user_id):
    from functions import exceptions
    from ast import literal_eval
    import time
    time.sleep(30)
    querystring = {"limit":"50","offset":"0","email":email,"templateId":templateId}

    headers = {
        'accept': "application/json",
        'api-key': KEYSENDI
        }

    response = requests.request("GET", BOUNCE, headers=headers, params=querystring)
    str_error_sendin = literal_eval(response.text)
    data = str_error_sendin.get("events")
    if (data and len(data) > 1):
        error_sendin = data[1]["event"]
        if error_sendin != "delivered":
            exceptions('sending_blue', data, eid, sid, user_id)
            return True
    return False
