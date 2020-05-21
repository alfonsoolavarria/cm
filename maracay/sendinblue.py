from maracay.config import KEYSENDI, STRANS, SCONT
import requests


# def sendinblue_contact_update(email,dictionary):
#     headers = {
#         'accept': 'application/json',
#         'api-key': KEYSENDI,
#         'content-type': 'application/json'
#         }
#     contact = {
#         "email":email,
#         "emailBlacklisted":False,
#         "smsBlacklisted":False,
#         "listIds":[14],
#         "updateEnabled":True,
#         "attributes":dictionary
#         }
#     requests.request("PUT",SCONT+"/"+email,json=contact,headers=headers)

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
    headers = {
        'accept': 'application/json',
        'api-key': KEYSENDI,
        'content-type': 'application/json'
        }
    params = {
        "email":email,"nombre":nombre,
        "apellido":apellido,
        }
    to = [{"email":email,"name":firstname}]


    if template == "registro":
        tempid = 1

    # if template == "Approvedinvoice":
    #     if lang == "en":
    #         subject = "Approved invoice"
    #     elif lang == "de":
    #         subject = "Genehmigte Rechnung"
    #     elif lang == "fr":
    #         subject = "Facture approuvée"
    #     elif lang == "it":
    #         subject = "Fattura approvata"
    #     else:
    #         subject = "Factura aprobada"
    #     tempid = 39
    #     params = {
    #         "locale":lang,"email":email,"firstname":firstname,"firstname_lastnameap":extra['firstname_lastnameap'],
    #         "confirmation":confirmation,"lastname":lastname,"company":extra['company'],
    #         "entry_date":extra['entry_date'],"total":extra['total']
    #         }
    #
    # if template == "approval" or template == "newuserbexio":
    #     if lang == "en":
    #         subject = "Your Account approval"
    #     elif lang == "de":
    #         subject = "Ihre Konto wurde genehmigt"
    #     elif lang == "fr":
    #         subject = "Approbation de votre compte"
    #     elif lang == "it":
    #         subject = "Approvazione del vostro conto"
    #     else:
    #         subject = "Aprobador de Cuenta"
    #     tempid = 3
    #
    # if template == "pending_approval":
    #     if lang == "en":
    #         subject = "Pending to Approve"
    #     elif lang == "de":
    #         subject = "Genehmigung ausstehend"
    #     elif lang == "fr":
    #         subject = "En attente d'approbation"
    #     elif lang == "it":
    #         subject = "In attesa di approvazione"
    #     else:
    #         subject = "Pendiente por Aprobar"
    #     tempid = 7
    #
    #     params = {
    #         "locale":lang,"email":email,"firstname":firstname,
    #         "lastname":lastname,"confirmation":confirmation,"hash":hash,
    #         "name":extra.company_to_add['name'],"sid":extra.company_to_add['sid'],
    #         "country":extra.country,"role":extra.role,"registration_date":str(extra.registration_date),
    #         "language":extra.language
    #         }
    #     to = [{"email":"info@indagia.com","name":"admin"}]
    #
    # if template == "register":
    #     if lang == "en":
    #         subject = "Your Account activation"
    #     elif lang == "de":
    #         subject = "Ihre Kontoaktivierung"
    #     elif lang == "fr":
    #         subject = "Activation du compte"
    #     elif lang == "it":
    #         subject = "Attivazione del conto"
    #     else:
    #         subject = "Activación de cuenta"
    #     tempid = 6
    #
    # if template == "forgot":
    #     if lang == "en":
    #         subject = "Change of Password"
    #     elif lang == "de":
    #         subject = "Kennwort ändern"
    #     elif lang == "fr":
    #         subject = "Changement de mot de passe"
    #     elif lang == "it":
    #         subject = "Cambio di password"
    #     else:
    #         subject = "Cambio de Clave"
    #     tempid = 8
    #
    # if template == "join_company":
    #     if lang == "en":
    #         subject = "Join a company"
    #     elif lang == "de":
    #         subject = "Einladung zum Eintritt ins Unternehmen"
    #     elif lang == "fr":
    #         subject = "Invitation à rejoindre la société"
    #     elif lang == "it":
    #         subject = "Invito ad aderire all'azienda"
    #     else:
    #         subject = "Invitación enviada para unirse a la empresa"
    #     tempid = 15
    #     params = {
    #         "from_firstname":extra['firstname'],
    #         "from_lastname":extra['lastname'],
    #         "company_name":extra['company_name'],
    #         "url_join":extra['url_join']
    #         }
    #
    # if template == "pay_process":
    #     if lang == "en":
    #         subject = "Payment process"
    #     elif lang == "de":
    #         subject = "Zahlungsvorgang"
    #     elif lang == "fr":
    #         subject = "Processus de paiement"
    #     elif lang == "it":
    #         subject = "Processo di pagamento"
    #     else:
    #         subject = "Proceso de Pago"
    #     tempid = 24
    #     params = {
    #         "firstname":firstname,
    #         "lastname":lastname,
    #         "email":email,
    #         "plan_name":extra["plan_name"],
    #         "default_credits":extra["default_credits"],
    #         "company":extra["company"],
    #         "language":lang,
    #         "default_price":extra["default_price"]
    #         }
    #     to = [{"email":"info@indagia.com","name":"admin"}]
    #
    # if template == "pay_process_temporal":
    #     if lang == "en":
    #         subject = "First confirmation of payment"
    #     elif lang == "de":
    #         subject = "Erste Bestätigung der Zahlung"
    #     elif lang == "fr":
    #         subject = "Première confirmation de paiement"
    #     elif lang == "it":
    #         subject = "Prima conferma del pagamento"
    #     else:
    #         subject = "Primera confirmación de pago"
    #     tempid = 43
    #     params = {
    #         "firstname":firstname,
    #         "lastname":lastname,
    #         "email":email,
    #         "plan_name":extra["plan_name"],
    #         "default_credits":extra["default_credits"],
    #         "company":extra["company"],
    #         "language":lang,
    #         "default_price":extra["default_price"]
    #         }
    #     to = [{"email":"info@indagia.com","name":"admin"}]
    #
    #
    # if template == "pay_process_user":
    #     if lang == "en":
    #         subject = "Paid plan"
    #     elif lang == "de":
    #         subject = "Bezahlter Plan"
    #     elif lang == "fr":
    #         subject = "Plan rémunéré"
    #     elif lang == "it":
    #         subject = "Piano a pagamento"
    #     else:
    #         subject = "Plan pagado"
    #     tempid = 26
    #     params = {
    #         "firstname":firstname,
    #         "lastname":lastname,
    #         "email":email,
    #         "plan_name":extra["plan_name"],
    #         "default_credits":extra["default_credits"],
    #         "company":extra["company"],
    #         "language":lang,
    #         "default_price":extra["default_price"]
    #         }
    #
    # if template == "pay_process_user_temporal":
    #     if lang == "en":
    #         subject = "First confirmation of payment"
    #     elif lang == "de":
    #         subject = "Erste Bestätigung der Zahlung"
    #     elif lang == "fr":
    #         subject = "Première confirmation de paiement"
    #     elif lang == "it":
    #         subject = "Prima conferma del pagamento"
    #     else:
    #         subject = "Primera confirmación de pago"
    #     tempid = 44
    #     params = {
    #         "firstname":firstname,
    #         "lastname":lastname,
    #         "email":email,
    #         "plan_name":extra["plan_name"],
    #         "default_credits":extra["default_credits"],
    #         "company":extra["company"],
    #         "language":lang,
    #         "default_price":extra["default_price"]
    #         }
    #
    # if template == "newuserbexiocompany":
    #     if lang == "en":
    #         subject = "New company"
    #     elif lang == "de":
    #         subject = "Neue Firma"
    #     elif lang == "fr":
    #         subject = "Nouvelle société"
    #     elif lang == "it":
    #         subject = "Nuova azienda"
    #     else:
    #         subject = "Nueva compañia"
    #     tempid = 37
    #     params = {
    #         "locale":lang,"email":email,"firstname":firstname,
    #         "lastname":lastname,
    #         "name_company":company,
    #         "plan_name":extra["plan_name"],
    #         "default_credits":extra["default_credits"]
    #         }

    transaction = {
        "to":to,
        # "subject": subject,
        "templateId":tempid,
        "params":params
        }
    response = requests.request("POST",STRANS,json=transaction,headers=headers)
    return response.text


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
