from __future__ import division
import time
import serial



if __name__ == '__main__':

    usbSerial = serial.Serial(port='/dev/tty.SLAB_USBtoUART', baudrate='115200', timeout=15)

    #t = time.strftime("%m\%d %H-%M-%S", time.localtime())

    #  Change to your target directory. Use t above to label it with the date/time.
    fileName = "/Users/david/Automation/Results/LWM Reboot Test Log.txt"

    logFile = open(fileName,'w')
    logFile.close()
    logFile = open(fileName, 'a')

    logFile.write('\n\nStarting up test now\n\n')
    logFile.write('Serial open? ' + str(usbSerial.is_open))
    logFile.flush()

    # The error string to find
    toFind = 'connection failed; next connection attempt in 3s ;connecting to service:'

    forever = True
    failCount = 0
    iterationTotal = 1
    failPercent = '0.00%'

    while forever:

        go = True
        iterationN = 1

        while go:

            usbSerial.write('\x03')
            logFile.write('\n\nREBOOTING.\n\n')
            logFile.flush()
            time.sleep(1)
            usbSerial.write('\nreboot\n'.encode('utf-8'))
            time.sleep(45)
            usbSerial.write('tail -f /var/log/messages\n\r'.encode('utf-8'))

            timeLimit = 25  # Max time to look for the issue after reboot.
            startTime = time.time()

            while (time.time() < (timeLimit + startTime)):

                line = usbSerial.readline()
                logFile.write(line)
                logFile.flush()

                if not line.find(toFind) == -1:

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
