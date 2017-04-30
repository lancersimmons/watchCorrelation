import os
import sys

def main():
    # if (len(sys.argv) != 2):
    #     print("Bad args. Pass in input, output file.")
    #     exit()

    # 0th arg is python filename
    print(sys.argv)

    # fileHandler = open(sys.argv[1], 'r')
    # fileHandlerWrite = open("outputNumbers.txt", 'w')

    # for line in fileHandler:
    #     lineTokens = line.split(' ')
    #     if lineTokens[0] in ["<START_FILE>", "<END_FILE>"]:
    #         continue

    #     loss = lineTokens[0]
    #     loss = loss[1:-1]


    #     fileHandlerWrite.write(str(loss))
    #     fileHandlerWrite.write("\n")
    #     # for token in lineTokens:
    #     #   print("TOKEN: " + token)




if __name__ == "__main__":
    main()