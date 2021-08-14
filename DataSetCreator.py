import json
import re

#text lower case and remove all special characters only but leave the spaces
regex = '[^a-z\s]'
def textPreProcessing(text):
    textTemp = text.lower()
    textTemp = re.sub(regex,"",textTemp)
    textTemp = textTemp.replace('\n','')
    return textTemp


def readTxtFileAndCountWords(fileInput):
    filePath = fileInput
    file = open(filePath,'r',encoding="utf8")
    dict = {}
    # reading each line    
    for line in file:
        # reading each word        
        words =  line.split()
        for word in words:
            word = textPreProcessing(word)
            if (word != ""):
                if(word in dict):
                    dict[word] += 1
                else:
                    dict[word] = 1

    sorted_keys = sorted(dict, key=dict.get,reverse=True)
    sorted_dict = {}
    totalFrequency = sum(dict.values())

    for w in sorted_keys:
        sorted_dict[w] = dict[w]/totalFrequency

    
    # Serializing json 
    json_object = json.dumps(sorted_dict, indent = 4)
    
    # Writing to sample.json
    with open(fileInput.split(".txt")[0]+".json", "w") as outfile:
        outfile.write(json_object)

    print("Dataset is created")

def main():
    userInput = -1
    while(True):
        print("****************To create dataset from multiple files please put them in one text file****************")
        fileInput = input("Please enter txt file name (e.g. prisoner-of-zenda.txt) and -1 to exit: ")
        if(fileInput == '-1'):break
        try:
            readTxtFileAndCountWords(fileInput)
        except:
            print("Please enter correct file name!!")

if __name__ == "__main__":
    main()
