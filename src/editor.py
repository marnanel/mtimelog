import dbus

def edit(filename):
   bus = dbus.SessionBus()
   proxy = bus.get_object('com.nokia.osso_notes',
                          '/com/nokia/osso_notes')
   proxy. mime_open('file://'+filename,
                    dbus_interface='com.nokia.osso_notes')

if __name__ == '__main__':
   edit('/etc/hosts')

