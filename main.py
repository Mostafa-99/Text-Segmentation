import json
import re
import seaborn as sns
import matplotlib.pyplot as plt
import time
from sklearn.metrics import f1_score


def readDataSetJSON(fileInput = 'count_1w'):
    filePath = './datasets/'+fileInput+'.json'
    f = open(filePath,'r')
    data=json.load(f)
    f.close()
    return data

def veterbiAlgorithm(text, p):
    words = [""]*(len(text)+1)
    best  = [0.0]*(len(text)+1)
    best[0] = 1.0

    for i in range(len(text)+1):
        for j in range(i):
            word = text[j:i]
            if(word in p):
                if (float(p[word])* best[i-len(word)] >= best[i]):
                    best[i] = float(p[word])* best[i-len(word)]
                    words[i] = word
            
    sequence = []
    i = len(text)
    while(i>0):
        sequence.append(words[i])
        i = i -len(words[i])
    sequence = sequence[::-1]
    return sequence,best[i]            

#text lower case and remove all special characters and spaces
regex = '[^a-z]'
def textPreProcessing(text):
    text = text.lower()
    text = re.sub(regex,"",text)
    return text

#text lower case and remove all special characters only but leave the spaces
regex2 = '[^a-z\s]'
def textPreProcessingForPerformance(text):
    textTemp = text.lower()
    textTemp = re.sub(regex2,"",textTemp)
    textTemp = textTemp.replace('\n','')
    return textTemp

#prepare the text for segmentation then run the algorithm
def segment(text,p): 
    text = textPreProcessing(text)
    seq, prob = veterbiAlgorithm(text, p)
    return seq

#calculate F1 score for the input in two ways (F1 score and modified one) explained in the document
def calculateF1Score(expectedOutput,programOutput):
    dictCount = {}
    for word in expectedOutput:
        dictCount[word]=programOutput.count(word)

    numberOfTrue = sum(dictCount.values())
    recall = numberOfTrue/len(expectedOutput)
    precision = numberOfTrue/len(programOutput)
    f1=0
    if(precision+recall != 0):
        f1 = 2*(recall*precision)/(precision+recall)
    
    f1Actual = 0
    if(len(expectedOutput) == len(programOutput)):
        f1Actual = f1_score(expectedOutput, programOutput, average='macro')

    return f1,f1Actual

#Calling of the algorithm and calculating F1 score
def measurePerformance(text, p):
    textInputForAlgo = textPreProcessing(text)
    if(textInputForAlgo==''):return -1,-1

    text = textPreProcessingForPerformance(text)
    expectedOutput = text.split(" ")

    programOutput, prob = veterbiAlgorithm(textInputForAlgo, p)
    f1ScoreModified,f1ScoreActual = calculateF1Score(expectedOutput,programOutput)
    return f1ScoreModified,f1ScoreActual

#User mode is just taking the input and write the output in an output file without any calculations    
def userMode(p,inFile,outFile):
    outFile.truncate(0) # need '0' when using r+
    # reading each line    
    for text in inFile:
        textOut = segment(text, p)
        textOut = ' '.join(textOut)
        outFile.write(textOut+'\n')

    print("Please check out.txt for the output segmented text")

#Performance mode is used for calculating F1 score and execution time
def performanceMode(p,inFile):
    start_time = time.time()

    # reading each line    
    totalAccuracy=0
    totalAccuracyAcctual=0
    testCasesCount = 0 
    for text in inFile:
        f1ScoreModified,f1ScoreActual = measurePerformance(text, p)
        if(f1ScoreModified!=-1):
            totalAccuracy+=f1ScoreModified
            totalAccuracyAcctual+=f1ScoreActual
            testCasesCount+=1
    end_time = time.time()

    #write the results in performance.txt file
    outFilePerformance = open("./output/performance.txt","w")
    outFilePerformance.write('Average F1 score Modified= '+str(totalAccuracy/testCasesCount)+'\n')
    outFilePerformance.write('Average F1 score Actual= '+str(totalAccuracyAcctual/testCasesCount)+'\n')
    outFilePerformance.write('Total execution time = '+str(end_time - start_time)+' seconds'+'\n')
    print("Please check performance.txt for the output")

#performance plotting is just calculating F1 score for a number of samples then plot the output
def performancePlottingMode(inFile,p):
    numberOfSamples = 600
    line_count = 0

    for line in inFile:
        line_count += 1
    #reset file pointer and init variables
    stepOfLines = line_count//numberOfSamples
    count = 0
    numberOfSamplesFinished = 0
    totalAccuracy=0
    totalAccuracyActual =0
    testCasesCount = 0 
    inFile.seek(0)
    outPutF1 = []
    outPutF1Actual = []
    countOfSamples = []
    #For each line in the file run the algorithm and measure the performance 
    for text in inFile:
        f1ScoreModified,f1ScoreActual = measurePerformance(text, p)
        if(f1ScoreModified!=-1):
            totalAccuracy+=f1ScoreModified
            totalAccuracyActual+=f1ScoreActual
            testCasesCount+=1
        count += 1
        #if number of lines in the sample reached then calculate the average and save it
        if(count == stepOfLines):
            count = 0
            numberOfSamplesFinished += 1
            f1 = totalAccuracy/testCasesCount
            f1Actual = totalAccuracyActual/testCasesCount
            outPutF1.append(f1)
            outPutF1Actual.append(f1Actual)
            countOfSamples.append(numberOfSamplesFinished*stepOfLines)
            
            #if finished number of samples end the loop
            if(numberOfSamplesFinished == numberOfSamples):
                break
    
    #plot F1 scores in two different graphs        
    grph= sns.lineplot(countOfSamples,outPutF1)
    plt.xlabel("Number of test cases")
    plt.ylabel("Average F1 score")
    grph.get_figure().savefig("./output/outputModified.png")
    plt.close()

    grph2= sns.lineplot(countOfSamples,outPutF1Actual)
    plt.xlabel("Number of test cases")
    plt.ylabel("Average F1 score")
    grph2.get_figure().savefig("./output/outputActual.png")
    
    print("Please check outputActual.png and outputModified.png for the output images")


def main():
    userInput = 0
    while(userInput != 4): 
        try:
            userInput = int(input("Which mode do you want to run? (1) User mode (2) Performance measurement (3) F1 Score plotting (4) Exit: "))
            p = readDataSetJSON('count_1w')
            inFilePath = './testcases/testcases.txt'
            outFilePath = './output/out.txt'
            inFile = open(inFilePath,'r',encoding="utf8")
            #do action depending on user input
            if(userInput == 1):
                outFile = open(outFilePath,"r+",encoding="utf8")
                #take from input file and put the output in the out file (without preformance measure)
                userMode(p,inFile,outFile)
                outFile.close()

            elif(userInput == 2):
                #Measure F1 Score, Run Time, Memory usage and print them in the terminal and in performance.txt file
                performanceMode(p,inFile)
                #Memory = 3MB
                
            elif(userInput == 3):
                #Measure F1 Score only and plot it in output.png
                performancePlottingMode(inFile,p)
            elif(userInput == 4):
                print("Program will close")
                inFile.close()
                break
        except:
            print("Error occured please check the input")
    

    
    
if __name__ == "__main__":
    main()
