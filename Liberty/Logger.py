import time
import shutil

severities = ['FATAL', 'ERROR', 'WARN', 'INFO']


class Logger:

    def __init__(self):
        self.running = 1

    def start(self):
        self.fileName = "Appium Log %s.txt" % self.getFilesafeTime()
        self.summaryName = "Test Summary %s.txt" %self.getFilesafeTime()
        new = open(self.fileName, "w")
        newSum = open(self.summaryName, "w")
        new.write("Appium Logging is beginning now at:\n%s" % self.getTime())
        newSum.write("Test Summary for tests at:\n%s" % self.getTime())
        new.close()
        newSum.close()

        self.lineCount = 1
        self.failureLine = 0

        self.f = open(self.fileName, "a")
        self.s = open(self.summaryName, "a")

    def finish(self):
        shutil.move(self.fileName, "/Users/david/Automation/Results/%s" % self.fileName)
        shutil.move(self.summaryName, "/Users/david/Automation/Results/%s" % self.summaryName)


    def getTime(self):
        t = time.strftime("%m/%d %H:%M:%S", time.localtime())
        return t

    def getFilesafeTime(self):
        t = time.strftime("%m\%d %H-%M-%S", time.localtime())
        return t

    def addLine(self, line, sev):
        message = '\n%d || %s [%s]: %s' % (self.lineCount, self.getTime(), severities[sev], line)
        print(message)
        self.f.write(message)
        self.lineCount = self.lineCount + 1

    def reportResults(self, testName, result):
        summary = '\n%s TEST %s at %s\n' % (testName, result, self.getTime())
        self.s.write(summary)

        if result == 'FAILED':
            self.s.write('\n!!! See log at line %d' % self.failureLine)

        self.s.write('\n')

    def markLine(self):
        self.failureLine = self.lineCount

    def logOptions(self, options):
        self.addLine('\n', 3)
        self.addLine('Starting OOBE with the following options:', 3)
        self.addLine('%s: %s' % ('Accept Data:', str(options['acceptData'])), 3)
        self.addLine('%s: %s' % ('Check Help:', str(options['checkHelp'])), 3)
        self.addLine('%s: %s' % ('Accept Eula:', str(options['acceptEULA'])), 3)
        self.addLine('%s: %s' % ('Use Current Network:', str(options['useCurrentNetwork'])), 3)
        self.addLine('%s: %s' % ('SSID:', str(options['ssid'])), 3)
        self.addLine('%s: %s' % ('Password:', str(options['password'])), 3)
        self.addLine('%s: %s\n' % ('Space Name:', str(options['spacename'])), 3)
