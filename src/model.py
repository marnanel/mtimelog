from PySide.QtCore import *
import sys
import os.path

class Timelog(QObject):
    def __init__(self, filename=None):
        QObject.__init__(self)

        if filename:
            self.filename = filename
        else:
            self.filename = '/home/user/.gtimelog/mtimelog.txt'

    def save(self, place, date, message):
        i = 1
        f = self._tempfile()
        m = self._mainfile()
        s = self._makestring(date, message) + '\n'

        for line in m.readlines():
            if place==i:
                f.write(s)
            else:
                f.write(line)
            i += 1

        if place==-1:
            f.write(s)

        f.close()

        self._storefile()

    def load(self):
        self.emit(SIGNAL('clear()'))

        i = 0

        for line in self._mainfile().readlines():

            i += 1

            if line[22:24]!=': ':
                continue

            try:
                year = int(line[0:4])
                month = int(line[5:7])
                day = int(line[8:10])
                hour = int(line[11:13])
                minute = int(line[14:16])
                second = 0
                #timezone = int(line[17:22])
                message = line[24:-1]

                date = QDate(year, month, day)
                time = QTime(hour, minute, second)
                datetime = QDateTime(date, time)

                self.emit(SIGNAL('found(int, QDateTime, QString)'),
                          i,
                          datetime,
                          message)
            except:
                pass

    def _tempfile(self):
        return file(self.filename + '.0', 'w')

    def _mainfile(self):
        return file(self.filename, 'r')

    def _storefile(self):
        os.rename(self.filename+'.0',
                  self.filename)

    def _makestring(self, date, message):
        # FIXME: need to make timezones saner
        return '%s %s: %s' % (date.toString('yyyy-MM-dd hh:mm'),
                             '-0400', # FIXME!
                             message)

class Quicks(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.filename = '/home/user/.gtimelog/quicks.txt'

        if not os.path.exists(self.filename):
            f = file(self.filename, 'w')
            f.write('sleep **\n')
            f.write('work\n')
            f.write('eat **\n')
            f.close()

    def contents(self):
        return sorted([x[:-1] for x in file(self.filename, 'r').readlines()])

if __name__=='__main__':

    import tempfile

    filename = tempfile.mkdtemp('model')+'/model.txt'

    print filename

    class Replayer(QObject):
        def __init__(self):
            QObject.__init__(self)
            self.contents = ''

        def receiveClear(self):
            self.contents += 'CLEAR\n'

        def receive(self, place, date, message):
            self.contents += '(%d) %s %s\n' % (place,
                                               date.toString(),
                                               message)

        def content(self):
            return self.contents

    def create_test_file():
        f = file(filename, 'w')

        events = ['get cape', 'wear cape', 'fly']

        for i in range(0, len(events)):
            f.write('2010-09-%02d 16:32 -0400: %s\n' % (10+i,
                                                        events[i]))

        f.close()

        return Timelog(filename)

    def run_test_by_id(testid):
        tl = create_test_file()
        if testid==1:
            return ['2010-09-10 16:32 -0400: get cape',
                    '2010-09-11 16:32 -0400: wear cape',
                    '2010-09-12 16:32 -0400: fly']
        elif testid==2:
            tl.save(-1,
                     QDateTime(QDate(2010, 10, 31)),
                     'Halloween')
            return ['2010-09-10 16:32 -0400: get cape',
                    '2010-09-11 16:32 -0400: wear cape',
                    '2010-09-12 16:32 -0400: fly',
                    '2010-10-31 00:00 -0400: Halloween']
        elif testid==3:
            tl.save(2,
                     QDateTime(QDate(2010, 9, 12)),
                     'go north')
            return ['2010-09-10 16:32 -0400: get cape',
                    '2010-09-12 00:00 -0400: go north',
                    '2010-09-12 16:32 -0400: fly']
        elif testid==4:
            rp = Replayer()
            rp.connect(tl, SIGNAL('clear()'), rp, SLOT('receiveClear()'))
            rp.connect(tl, SIGNAL('found(int, QDateTime, QString)'),
                       rp, SLOT('receive(int, QDateTime, QString)'))

            tl.load()

            file(filename, 'w').write(rp.content())
            return ['CLEAR',
                    '(1) Fri Sep 10 16:32:00 2010 get cape',
                    '(2) Sat Sep 11 16:32:00 2010 wear cape',
                    '(3) Sun Sep 12 16:32:00 2010 fly',
                    ]

        else:
            return None

    def run_tests():

        testid = 1

        while True:
            contents = run_test_by_id (testid)

            if contents==None:
                print "All tests finished."
                os.unlink(filename)
                return

            want = '\n'.join(contents)+'\n'
            found = file(filename, 'r').read()

            if want != found:
                print 'Test %d: FAIL.' % (testid,)
                print 'Want:\n%s\nFound:\n%s' % (want,
                                                 found)
            else:
                print 'Test %d: pass.' % (testid,)

            os.unlink(filename)
        
            testid += 1


    run_tests()
    os.rmdir(filename[:filename.rindex('/')])
