import requests
import json
import os
import sys
import urllib.parse
import six
import riotgames_api

lolcapi = riotgames_api.LeagueOfLegendsClientAPI()

def createlobby():
    lolcapi.post('/lol-lobby/v2/lobby', {"queueId": 700})
    
def userinfo(username):
    summoner = lolcapi.get('/lol-summoner/v1/summoners?name=%s' % username)
    accountid = summoner.get("summonerId")
    return accountid
        
def menu():
    print('+--------------------------------------------------------------+')
    print("@TravaLOL - 1. Utilizar 'nickname' do usuario para travar.")
    print("@TravaLOL - 2. Utilizar o 'SummonerID' do usuario para travar.")
    print("@TravaLOL - 3. Verificar o 'SummonerID' do usuario utilizando o 'nickname'.")
    print("@TravaLOL - 4. Criar um lobby. (Clash)")
    print("@TravaLOL - 5. Creditos.")
    print('+--------------------------------------------------------------+')
    selection = int(input('Escola uma opção: '))
    global accountid
    if selection == 1:  
        user = input('Username: ')
        userformated = urllib.parse.quote(user)
        accountid = userinfo(userformated)
    if selection == 2:
        accountid = input('SummonerID: ')
    if selection == 3:  
        user = input('Username: ')
        userformated = urllib.parse.quote(user)
        accountid = userinfo(userformated)
        print('+--------------------------------------------------------------+')
        print('@TravaLOL - SummonerID: %s' % accountid)
        menu()
    if selection == 4:
        createlobby()
        menu()
    if selection == 5:
        print('+--------------------------------------------------------------+')
        print("@TravaLOL - Feito por: @TravaLoL")
        menu()    
    ## // Antigo sistema de whitelist //
    #try:
        #with six.moves.urllib.request.urlopen('Lista de usuários na whitelist') as f:
            #test2 = f.read().decode('utf-8')
            #teste3 = json.loads(test2)
            #for i in teste3['whitelist']:
                #if accountid == i['id']:
                    #anykey = input('@TravaLOL - Whitelisted User. \nPress ENTER to continue...')
                    #menu()
    #except urllib.error.URLError as e:
        #print(e.reason)        
    while True:
        print('+-----+')
        r = lolcapi.post('/lol-lobby/v2/lobby/invitations', [{"toSummonerId":accountid}])
        print('@TravaLOL - Convite Enviado: %s (%s)' % (r.status_code, accountid))
        print('+-----+')
        r2 = lolcapi.post('/lol-lobby/v2/lobby/members/%s/kick' % accountid)
        print(r2.json())
        print('@TravaLOL - Convite Removido: %s (%s)' % (r2.status_code, accountid))
        print('+-----+')
    
try:
    menu()
except KeyboardInterrupt:
    sys.exit(0)