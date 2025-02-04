import requests
import json
import random
import os
import time

api_key = "<insert your api key here>" #Your API-Key
baseurl = "https://api.rustmaps.com"
limit_ep = "/v4/maps/limits"
gen_ep = "/v4/maps"
seed_history = "seeds.txt" #The file that keeps track of seeds that already have been generated
retry_interval = 20 #Time in seconds before retrying to generate a map
size = <insert map size here> #The map size
staging = True #Will generate staging maps if True
headers = {"X-API-Key": api_key}




def generateRandomSeed():
    mode = 'r' if os.path.exists(seed_history) else 'a+'
    with open(seed_history, mode) as seeds:
        prev_seeds = seeds.readlines()
        seed = random.randint(1, 2147483647)

        if seed not in prev_seeds:
            return seed
        
        else: 
            generateRandomSeed()


def generateMap(size, seed, staging):
    
    genr = requests.post(baseurl + gen_ep, headers=headers, json={
        "size": size,
        "seed": seed,
        "staging": staging
    })
    
    
    genr_json = genr.json

    if genr.status_code in [200,201]:
        with open(seed_history, "a") as seeds:
            seeds.write(str(seed) + "\n")
        
        if genr.status_code == 201:
            print("Map generation successfully started for seed " + str(seed) + "!")
            print(genr.text)

        elif genr.status_code == 200:
            print("The map for seed " + str(seed) + " was already generated. Starting new generation!")
            generateMap(size, generateRandomSeed(), staging)
        

    else:
        print("Error-Code: " + str(genr.status_code))

##end of functions##

def attemptMapGeneration():
    r = requests.get(baseurl + limit_ep, headers=headers)
    resp_json = json.loads(r.text)
    resp_meta = resp_json['meta']

    if resp_meta['statusCode'] != 200:
        print (resp_meta['status'] + ": " + str(resp_meta['statusCode']))

    else:
        gen_limit_conc = [resp_json['data']['concurrent']['current'], resp_json['data']['concurrent']['allowed']]
        gen_limit_mtl = [resp_json['data']['monthly']['current'], resp_json['data']['monthly']['allowed']]
        
        if gen_limit_mtl[0] != gen_limit_mtl[1]:
            #routine here
            if gen_limit_conc[0] != gen_limit_conc[1]:
                avail = gen_limit_conc[1] - gen_limit_conc[0]

                for i in range(avail):
                    generateMap(size, generateRandomSeed(), staging)
                print("Hit generation limit for now, refreshing in " + str(retry_interval) + " seconds")
            else:
                print("Concurrent limit reached! Retrying in " + str(retry_interval) + " seconds")

        else:
            print("Monthly limit reached, good luck next mont =)")
            return False
while True:
    if attemptMapGeneration() == False:
        break
    time.sleep(retry_interval)