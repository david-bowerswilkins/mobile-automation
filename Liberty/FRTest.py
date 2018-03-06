from __future__ import division
import time
import serial

def readSerial():
    try:
        line = usbSerial.readline()
        dec = line.decode('utf-8')
        l = str(dec)
        logFile.write(l)
        logFile.flush()
        return l
    except:
        logFile.write('\nOne line of output had some invalid UTF-8. Why? He screams, for he does not know.\n\n')

if __name__ == '__main__':

    usbSerial = serial.Serial(port='/dev/tty.SLAB_USBtoUART', baudrate='115200', timeout=15)

    #t = time.strftime("%m\%d %H-%M-%S", time.localtime())

    #  Change to your target directory. Use t above to label it with the date/time.
    fileName = "/Users/david/Automation/Results/FRTestLog.txt"

    logFile = open(fileName,'w')
    logFile.close()
    logFile = open(fileName, 'a')

    logFile.write('\n\nStarting up test now\n\n')
    logFile.write('Serial open? ' + str(usbSerial.is_open))
    logFile.flush()

    forever = True
    failCount = 0
    iterationTotal = 1
    failPercent = '0.00%'
    toFind = 'Setting current audio index to 0'

    while forever:

        go = True
        iterationN = 1

        while go:
            logFile.write('\nDoing meshctl now.\n\n')
            logFile.flush()

            usbSerial.write('\x03'.encode('utf-8'))
            usbSerial.write('\n\n'.encode('utf-8'))
            usbSerial.write('meshctl info\n'.encode('utf-8'))
            slice = ''
            time.sleep(2)

            while True:
                try:
                    line = usbSerial.readline()
                    dec = line.decode('utf-8')
                    l = str(dec)
                    logFile.write(l)
                    logFile.flush()

                    if not l.find('Node ID: ') == -1:
                        nodeID = l[9:]
                        slice = nodeID[:6]
                        break
                except:
                    logFile.write('\nOne line had bad UTF encoding.\n\n')

            logFile.write('\nFACTORY RESETTING NOW.\n\n')
            logFile.flush()
            time.sleep(1)
            serIn = 'statectl factory-reset -id %s\n' % slice
            usbSerial.write(serIn.encode('utf-8'))

            time.sleep(50)

            timeLimit = 10  # Max time to look for the issue after reboot.
            startTime = time.time()

            usbSerial.write('\x03'.encode('utf-8'))
            time.sleep(1)
            usbSerial.write('\noobectl liberty\n'.encode('utf-8'))
            time.sleep(3)
            usbSerial.write('tail -f /var/log/messages\n'.encode('utf-8'))

            while (time.time() < (timeLimit + startTime)):

                try:
                    line = usbSerial.readline()
                    dec = line.decode('utf-8')
                    l = str(dec)
                    logFile.write(l)
                    logFile.flush()
                except:
                    logFile.write('\nOne line of output had some invalid UTF-8. Why? He screams, for he does not know.\n\n')
                    continue

                if not l.find(toFind) == -1:

                    failCount = failCount + 1
                    failPercent = "{0:.2f}".format((failCount / iterationTotal) * 100) + '%'

                    logFile.write('\n\n\n!!!ISSUE HAS BEEN HIT!!!\nCURRENT ITERATION: %s\nTOTAL ITERATIONS: %s\nTOTAL FAILURES: %s\nFAILURE PERCENTAGE: %s\n\n' % (iterationN, iterationTotal, failCount, failPercent))
                    go = False
                    forever = True  # Change this to forever = False to stop after one failure.
                    break

            if go:
                logFile.write('\n\n\nDID NOT HIT ISSUE.\nCURRENT ITERATION: %s\nTOTAL ITERATIONS: %s\nTOTAL FAILURES: %s\nFAILURE PERCENTAGE: %s\n\n' % (iterationN, iterationTotal, failCount, failPercent))

            iterationN = iterationN + 1
            iterationTotal = iterationTotal + 1
            logFile.flush()
