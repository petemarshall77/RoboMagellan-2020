#
# Identify USB Devices
#
import subprocess, re

installed_devices = {
    'key': 'value'
    }

port_families = ['/dev/ttyACM', '/dev/ttyUSB']


def probe():
    ports = {}
    for port_family in port_families:
        for index in range(10):
            port = '%s%s' % (port_family, index)
            command = 'udevadm info -a -n %s' % port
            try:
                out = subprocess.check_output(command.split(),
                                            stderr=subprocess.STDOUT)

                regex = re.compile("{serial}==\"([\w\.:]+)\"")
                match = regex.search(out)
                if match:
                    serial_num = match.group(1)
                    if serial_num in installed_devices:
                        ports[installed_devices[serial_num]] = port
            except:
                pass

    return ports
