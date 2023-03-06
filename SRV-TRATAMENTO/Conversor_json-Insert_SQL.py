import csv
import json


def transformador_json(csvFilePath, jsonFilePath):
     
    
    data = {}
     
    
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
       
      for rows in csvReader:
                   key = rows['No']
            data[key] = rows
 
    
    
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
         
 
csvFilePath = r'../SUBSCRIBER-e-CSV_ARQUIVO/topico.csv'#No campo tópico deverá ser alterado para o nome do arquivo que iremos converter
#O nome do arquivo, relembrando é ('tópico do publisher',QOS).csv
jsonFilePath = r'topico.json'
 
transformador_json(csvFilePath, jsonFilePath)

#Esse é um exemplo de como seria feito o  transformador.

