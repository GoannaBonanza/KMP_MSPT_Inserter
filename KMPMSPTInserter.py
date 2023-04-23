def FindMSPT(KMPFile):
    #MSPT Offset location
    KMPFile.seek(0x44)
    MSPToffset=0
    #For loop for finding combined byte value of offset
    for k in range(0, 4):
        if k > 0:
            MSPToffset = MSPToffset << 8
        byte = KMPFile.read(1)
        MSPToffset = MSPToffset + ord(byte)
    return MSPToffset + 0x4c
def FindStageInfo(KMPFile):
    #MSPT Offset location
    KMPFile.seek(0x48)
    STGIoffset=0
    #For loop for finding combined byte value of offset
    for k in range(0, 4):
        if k > 0:
            STGIoffset = STGIoffset << 8
        byte = KMPFile.read(1)
        STGIoffset = STGIoffset + ord(byte)
    return STGIoffset
def FindStartPos(KMPFile):
    #MSPT Offset location
    KMPFile.seek(0x10)
    STRToffset=0
    #For loop for finding combined byte value of offset
    for k in range(0, 4):
        if k > 0:
            STRToffset =STRToffset << 8
        byte = KMPFile.read(1)
        STRToffset = STRToffset + ord(byte)
    return STRToffset + 0x4c
def CheckForMSPT(MSPToffset, KMPFile):
    KMPFile.seek(MSPToffset+5)
    byte = KMPFile.read(1)
    print("There are", ord(byte), "MSPTS in this Course")
    return ord(byte)
def FindRemainLength(AmoOfMSPT, MSPToffset, KMPFile):
    restBytes = 0
    KMPFile.seek(MSPToffset + 13 + (AmoOfMSPT * 0x1c))
    byte = KMPFile.read(1)
    print("There are", ord(byte), "STGI Entries")
    restBytes = (ord(byte)*0xc) + 10
    return restBytes
def GetStartPos(KMPFile, STARTPOSoffset):
    KMPFile.seek(STARTPOSoffset + 6)
    StartPos = KMPFile.read(0x1c)
    return StartPos
#MAIN PROGRAM
filestr = input("Input name (no kmp): ")
msptOff=0
strmakeMSPT=""
makeMSPT=False
BufferList = []
MSPTAmount = 0
RestOfFile = 0
startPosOff = 0
StartPosData = 0
STGIOff = 0
MSPTChange = 0
try:
    KMPFile = open(filestr + ".kmp", "br")
except FileNotFoundError:
    print("File does not exist")
    raise SystemExit
msptOff = FindMSPT(KMPFile)
MSPTAmount = CheckForMSPT(msptOff, KMPFile)
RestOfFile = FindRemainLength(MSPTAmount, msptOff, KMPFile)
strmakeMSPT = input("(1) make MSPT or (2) don't: ")
if strmakeMSPT == "1":
    MSPTChange = 1 - MSPTAmount
    STGIOff = FindStageInfo(KMPFile) + (0x1c * MSPTChange)
    startPosOff = FindStartPos(KMPFile)
    StartPosData = GetStartPos(KMPFile, startPosOff)
    KMPFile.seek(0)
    BufferList.append(KMPFile.read(0x48))
    KMPFile.seek(0x4c)
    BufferList.append(KMPFile.read(msptOff - 0x4c))
    KMPFile.seek(msptOff + 6 + (0x1c * MSPTAmount))
    BufferList.append(KMPFile.read(RestOfFile))
    KMPFile.close()
    KMPFile = open(filestr + ".kmp", "bw")
    KMPFile.write(BufferList[0])
    KMPFile.write(STGIOff.to_bytes(4, 'big'))
    KMPFile.write(BufferList[1])
    KMPFile.write((1297305684).to_bytes(4, 'big'))
    KMPFile.write((1).to_bytes(2, 'big'))
    KMPFile.write(StartPosData)
    KMPFile.write(BufferList[2])
    KMPFile.close()
    print("Rewritten file one MSPT with the first start position's data")
else:
    raise SystemExit
