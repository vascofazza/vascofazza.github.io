import serial
import string
import sys
import time
import serial
import os

sys.stdout.write('Arduino Parallel flash Programmer v1.2 - Federico Scozzafava\n')
sys.stdout.write('more information at --- http://insidecode.altervista.org\n')
sys.stdout.write('################################\n')

ser = serial.Serial('COM1', 57600)# Change COM2 to the port the Arduino is on
time.sleep(2) # Arduino gets reset when serial is started so we wait a bit

waitInput = 1


while (waitInput == 1):
        sys.stdout.write('Choose one of the following options:\n1. Dump game\n2. Read flash\n3. Program flash\n4. Erase flash\n5. Game info\n6. Arduino reset\n')
        sys.stdout.write('>')
        userInput = input()


        if (userInput == "3"):
            sys.stdout.write('\nName of source file...?')
            sys.stdout.write('\n>')
            userInput3 = input()
            fileExists = 1
            try:
                f = open(userInput3, 'rb')
            except IOError:
                sys.stdout.write('File not found, aborted.\n\n')
                fileExists = 0
            if (fileExists == 1):
                size = os.path.getsize(userInput3)
                b = str(size)
                sys.stdout.write('\nFile size: ' + b + 'bytes\n')
                sys.stdout.write('\n' + userInput3 + ' will be written on the flash\n' )
                sys.stdout.write('\n***Are you sure?***')
                sys.stdout.write('\nPress y to continue or n to abort.')
                sys.stdout.write('\n>')
                userInput2 = input()
                

                if (userInput2 == "y"):
                        ser.flushInput()
                        ser.flushOutput()
                        sys.stdout.write('\nProgramming... ')
                        doExit = 0
                        printHash = 0
                        Kbyteswrite = 0
                        try:
                            f = open(userInput3, 'rb')
                        except IOError:
                            sys.stdout.write('File not found, aborted.\n\n')
                            fileExists = 0
                        if (fileExists == 1):
                            if (b == '1024'):
                                ser.write('W17'.encode())
                            elif (b == '2048'):
                                ser.write('W27'.encode())
                            elif (b == '4096'):
                                ser.write('W37'.encode())
                            elif (b == '8192'):
                                ser.write('W47'.encode())
                            elif (b == '16384'):
                                ser.write('W57'.encode())
                            elif (b == '32768'):
                                ser.write('W67'.encode())
                            elif (b == '65536'):
                                ser.write('W77'.encode())
                            elif (b == '131072'):
                                ser.write('W87'.encode())
                            elif (b == '262144'):
                                ser.write('W97'.encode())
                            elif (b == '524288'):
                                ser.write('W07'.encode())
                            while 1:
                                waitArduino = 1
                                while waitArduino == 1:
                                    line = ser.readline()
                                    lineascii = ascii(line)
                                    if lineascii.find('NEXT') >= 0:
                                        waitArduino = 0
                                    if lineascii.find('END') >= 0:
                                        ser.flush()
                                        ser.flushInput()
                                        ser.flushOutput()
                                        doExit = 1
                                        break
                                if printHash % 4 == 0 and printHash != 0: # 256 / 64 = 4
                                    sys.stdout.write('#')
                                if printHash % 16 == 0 and printHash != 0:
                                    Kbyteswrite = Kbyteswrite + 1
                                    sys.stdout.write("%sK" % Kbyteswrite)
                                printHash += 1                                
                                if doExit == 1:
                                    break
                                line1 = f.read(64) # Read 64bytes of save file
                                if not line1:
                                    ser.flush()
                                    ser.flushInput()
                                    ser.flushOutput()
                                    break
                                ser.write(line1)

                            sys.stdout.write('\nOK!\n\n')
                        f.close()                        
            else:
                sys.stdout.write('Aborted.\n\n')

        if (userInput == "2"):

            sys.stdout.write('\nName of destination file...?')
            sys.stdout.write('\n>')
            userInput3 = input()
            sys.stdout.write('\nData size?\n' )
            sys.stdout.write('\n******')
            sys.stdout.write('\n1) 8kb\n2) 16kb\n3) 32kb\n4) 64kb\n5) 128kb\n6) 256kb\n7) 512kb')
            sys.stdout.write('\n******')
            sys.stdout.write('\n>')
            userInput4 = input()
            if (userInput4 == "1"):
                ser.write('R17'.encode())
            elif (userInput4 == "2"):
                ser.write('R27'.encode())
            elif (userInput4 == "3"):
                ser.write('R37'.encode())
            elif (userInput4 == "4"):
                ser.write('R47'.encode())
            elif (userInput4 == "5"):
                ser.write('R57'.encode())
            elif (userInput4 == "6"):
                ser.write('R67'.encode())
            elif (userInput4 == "7"):
                ser.write('R77'.encode())
            sys.stdout.write('\nDumping data on ' + userInput3 + ' ...\n')
            readBytes = 0
            inRead = 0
            Kbytesread = 0;
            f = open(userInput3 , 'wb')
            while 1:
                line = ser.readline()
                lineascii = ascii(line)
                if not line:
                    break
                if lineascii.find('END') >= 0:
                    break
                if inRead == 1:
                    writeLine = chr(int(line))
                    readBytes += 1
                    f.write(writeLine.encode('latin'))
                if lineascii.find('START') >= 0:
                    inRead = 1
                if readBytes % 1024 == 0 and readBytes != 0:
                    sys.stdout.write('#')
                if readBytes % 8192 == 0 and readBytes != 0:
                    Kbytesread = Kbytesread + 1
                    Kbytesprint = Kbytesread * 8
                    sys.stdout.write("%sK" % Kbytesprint)        
            sys.stdout.write('\nOK!\n\n')
            f.close()
                                
        elif (userInput == "1"):
            ser.flush()
            ser.flushInput()
            ser.flushOutput()
            ser.write('H07'.encode())
            sys.stdout.write('Game name...    ')
            gameTitle = ascii(ser.readline())
            gameTitle = gameTitle[2:(len(gameTitle)-5)]
            print (gameTitle)
            sys.stdout.write('ROM size... ')
            romSize = ascii(ser.readline())
            romSize = int(romSize[2:(len(romSize)-5)])
            if (romSize == 0):
                print ('32KByte')
            elif (romSize == 1):
                print ('64KByte')
            elif (romSize == 2):
                print ('128KByte')
            elif (romSize == 3):
                print ('256KByte')
            elif (romSize == 4):
                print ('512KByte')
            sys.stdout.write('Compability... ')
            compability = ascii(ser.readline())
            compability = int(compability[2:(len(compability)-5)])
            if (compability == 0):
                print ('GameBoy')
                estenzione = ('gb')
            elif (compability == 1):
                print ('GameBoy Color Compatible')
                estenzione = ('gb')
            elif (compability == 2):
                print ('GameBoy Color Only')
                estenzione = ('gbc')
            else:
                print ('Not identified')
                estenzione = ('gb')
            sys.stdout.write('\nDumping on ' + gameTitle +'.'+ estenzione + '...')
            readBytes = 0
            inRead = 0
            Kbytesread = 0;
            ser.write('D07'.encode())
            f = open(gameTitle + '.' + estenzione, 'wb')
            while 1:
                line = ser.readline()
                lineascii = ascii(line)
                if not line:
                    break
                if lineascii.find('END') >= 0:
                    break
                if inRead == 1:
                    writeLine = chr(int(line))
                    readBytes += 1
                    f.write(writeLine.encode('latin'))
                if lineascii.find('START') >= 0:
                    inRead = 1
                if readBytes % 1024 == 0 and readBytes != 0:
                    sys.stdout.write('#')
                if readBytes % 32768 == 0 and readBytes != 0:
                    Kbytesread = Kbytesread + 1
                    Kbytesprint = Kbytesread * 32
                    sys.stdout.write("%sK" % Kbytesprint)        
            sys.stdout.write('\nOK!\n\n')
            f.close()

        elif (userInput == "4"):
            ser.flushInput()
            ser.flushOutput()
            sys.stdout.write('\nI am going to ERASE the Flash...')
            sys.stdout.write('\n***Are you sure?***')
            sys.stdout.write('\nPress y to continue or n to abort.')
            sys.stdout.write('\n>')
            userInput2 = input()
            if (userInput2 == "y"):
                sys.stdout.write('Erasing...\n')
                ser.write('E07'.encode())
                line = ser.readline()
                lineascii = ascii(line)
                if lineascii.find('K') >= 0:
                   sys.stdout.write('\nOK!\n\n')
        elif (userInput == "5"):
            ser.flushInput()
            ser.flushOutput()
            ser.write('H07'.encode())
            sys.stdout.write('Game name...    ')
            gameTitle = ascii(ser.readline())
            gameTitle = gameTitle[2:(len(gameTitle)-5)]
            print (gameTitle)
            sys.stdout.write('ROM size... ')
            romSize = ascii(ser.readline())
            romSize = int(romSize[2:(len(romSize)-5)])
            if (romSize == 0):
                print ('32KByte')
            elif (romSize == 1):
                print ('64KByte')
            elif (romSize == 2):
                print ('128KByte')
            elif (romSize == 3):
                print ('256KByte')
            elif (romSize == 4):
                print ('512KByte')
            sys.stdout.write('Compability... ')
            compability = ascii(ser.readline())
            compability = int(compability[2:(len(compability)-5)])
            if (compability == 0):
                print ('GameBoy')
                estenzione = ('gb')
            elif (compability == 1):
                print ('GameBoy Color Compatible')
                estenzione = ('gb')
            elif (compability == 2):
                print ('GameBoy Color Only')
                estenzione = ('gbc')
            else:
                print ('Not identified')
                estenzione = ('gb')
        elif (userInput == "6"):
            ser.close()
            time.sleep(0.1)
            ser.open()
            time.sleep(2)
            waitInput = 1
            continue
            
        else:
            sys.stdout.write('\nCommand not recognised, please try again.\n\n')
ser.close()
