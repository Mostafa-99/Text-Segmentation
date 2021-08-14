import json

#Note dataset input must be word:Frequency to calculate the probability correctly
def convertTxtToJson(fileInput):
    
    filePath = fileInput+'.txt'
    file = open(filePath,'r',encoding="utf8")
    dict = {}
    # reading each line    
    for line in file:
        # reading each word        
        words =  line.split()
        dict[words[0]] = int(words[1])


    totalFrequency = sum(dict.values())
    
    #calc probability (freq/totalFreq)
    for word in dict:      
        dict[word] = float(dict[word]/totalFrequency)

    # Serializing json 
    json_object = json.dumps(dict, indent = 4)
    
    # Writing to sample.json
    with open(fileInput+".json", "w") as outfile:
        outfile.write(json_object)

    print("Converted to json")

   


def main():
    fileName = input("Please enter Text name e.g. count_1w: ")
    convertTxtToJson(fileName)
    
    
if __name__ == "__main__":
    main()
