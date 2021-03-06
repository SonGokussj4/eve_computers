""" Available keys:
    check_mk                           ... Hostname (cuddy.konstru.evektor.cz)
    df                                 ...
    df_2                               ...
    nfsmounts                          ... connected mounts with space available etc
    cifsmounts                         ...
    mounts                             ...
    ps                                 ... all running processes
    mem                                ... all info about memory in columns
    cpu                                ... cpu usage (0.09 0.07 0.12 1/581 25295 8)
    uptime                             ... uptime (820637.18 6489510.66)
    lnx_if                             ... something with network, iplink?
    lnx_if:sep(58)                     ... something with network too, speed, adresses, ...
    tcp_conn_stats                     ... (01 3 \n 0A 19)
    diskstat                           ... (8      16 sdb 226124 212 17686679 982982 12665240 145901 213040630 1491786882 0 22245661 1492790767)
    kernel                             ... very much numbers (1498752495 \nnr_free_pages 19155871)
    md                                 ...
    vbox_guest                         ...
    ntp:cached(1498752290,30)          ...
    chrony:cached(1498752290,30)       ... some IP adress and something...
    nvidia                             ... (GPUErrors: 0 \nGPUCoreTemp: 64 \nGPUCoreTemp: 64)
    cups_queues:cached(1498752204,300) ... connected printers? (printer hp4650dn is idle. enabled since Thu Jun 29 11:48:22 2017 \nprinter Xerox is idle. enabled since Mon Nov 14 07:23:30 2016)
    postfix_mailq                      ...
    job                                ...
    local                              ...
    logins                             ...
    user                               ...
    dmi_bios                           ... bios release date, rom size, characteristics, version
    dmi_system                         ... (Product Name: Precision WorkStation T7500, Serial Number: 472BX4J, UUID, ...)
    dmi_baseboard                      ... (Product Name: 06FW8P, Version, Serial Number, Manufacturer)
    dmi_processor                      ... Processor info: (Flags, Max Speed, Upgrade, )
    memory                             ... Memory size: (94G)
    memory_2                           ... Physical memory installed: (96GiB System Memory) and slots (8GiB DIMM DDR3 1333 MHz (0.8 ns))
    dmi_memory_max                     ... Max memory that can be installed: (Maximum Capacity: 192 GB)
    dmi_memory                         ... Info about individual modules (Size, Speed, Manufacturer, Serial Number, Part Number, ...)
    dmi_memory_array                   ... Range size of currently installed memory: (Range Size: 96 GB)
    drives                             ... (KNAME TYPE SIZE REV SERIAL MODEL \nsdb   disk 278.9G 1028 600508e0000000006ca7fe2e6684410f VIRTUAL DISK)
    monitor_info                       ... Info about monitors, EDID, ...
    monitor_names                      ... Monitor Names with connectors (DELL U2410 (DFP-3) \nDELL U2410 (DFP-4))
    monitor_resolutions                ... Monitor Resolutions with connectors (DP-2 1920x1200 1920 \nDP-3 primary 1920x1200)
    lscpu                              ... All the info about cpu: sockets, cpus, ht, (Intel(R) Xeon(R) CPU        X5677  @ 3.47GHz)
    gpu_name                           ... Name of GPU: (NVIDIA Corporation GF100GL [Quadro 4000] (rev a3))
    gpu_driver                         ... (375.39)
    uptime_all                         ...
    os_distributor                     ... (CentOS)
    os_release                         ... (7.3.1611)
    os_kernel                          ... (3.10.0-514.6.1.el7.x86_64)
    os_codename                        ... (Core)
    local_ip                           ... (10.0.23.35)
    public_ip                          ... (194.212.223.78)
    location                           ... (KUNOVICE)
    screeninfo                         ... DUPLICITE  #TODO: Odstranit, duplicitni

    ['local', 'cpu', 'mounts', 'cifsmounts', 'os_kernel', 'monitor_info', 'os_release', 'md', 'vbox_guest',
    'dmi_memory_max', 'diskstat', 'job', 'gpu_name', 'gpu_driver', 'dmi_system', 'mem',
    'ntp:cached(1499695070,30)', 'nfsmounts', 'logins', 'uptime_all', 'lscpu', 'memory_2', 'kernel', 'user',
    'memory', 'df_2', 'lnx_if:sep(58)', 'check_mk', 'monitor_names', 'dmi_memory_array', 'postfix_mailq',
    'drives', 'lnx_if', 'dmi_baseboard', 'cups_queues:cached(1499694841,300)', 'ps', 'uptime', 'os_distributor',
    'nvidia', 'local_ip', 'chrony:cached(1499695070,30)', 'os_codename', 'df', 'dmi_bios', 'monitor_resolutions',
    'dmi_processor', 'public_ip', 'tcp_conn_stats', 'location', 'dmi_memory']
"""

import os
from os.path import join, curdir, abspath
import re
import datetime
import subprocess
import collections

# DELL WARRANTY
# https://gist.github.com/teroka/0720274b87b77fe7171f

timeout = 5  # timeout for ncat in sec


class Host():
    """Class description."""

    def __init__(self, hostname, timeout=timeout):
        self.hostname = hostname
        self.received_list = []
        self.results = {}
        try:
            self.out = subprocess.check_output(
                ['ncat', '--recv-only', self.hostname, '6556'], timeout=timeout, stderr=subprocess.STDOUT)
            self.received_list = self.out.decode('UTF-8')
            self.received = True
            self.received_msg = '{hostname} .. OK'.format(hostname=hostname)
            self.results = self.__get_ncat_results()

        except subprocess.TimeoutExpired as e:
            self.received = False
            self.received_msg = 'TIMEOUT EXPIRED: {e}'.format(e=e)
        except subprocess.CalledProcessError as e:
            self.received = False
            self.received_msg = 'CALLED PROCESS ERROR: {e}'.format(e=e)
        except Exception as e:
            self.received = False
            self.received_msg = 'UNKNOWN EXCEPTION: {e}'.format(e=e)

    def __get_ncat_results(self):
        if not self.received:
            return None
        results = collections.defaultdict(dict)
        result_list = [item for item in re.split(r'(<<<.*?>>>)', self.received_list) if item]
        for idx in range(0, len(result_list), 2):
            new_key = result_list[idx].replace('<<<', '').replace('>>>', '')
            if new_key in results.keys():
                results.update({re.sub(new_key, '{}_2'.format(new_key), new_key): result_list[idx + 1].strip()})
            else:
                results.update({new_key: result_list[idx + 1].strip()})
        return results

    @property
    def location(self):
        """
        KUNOVICE
        ZLIN
        """
        return self.results.get('location')

    @property
    def cpu_name(self):
        """
        Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz
        Intel(R) Xeon(R) CPU E5-1680 v3 @ 3.20GHz
        """
        res = self.results.get('lscpu').split('\n')
        model_name = [item for item in res if item.startswith('Model name:')][0]
        return ' '.join(model_name.replace('Model name: ', '').split())

    @property
    def cpu_details(self):
        """
        2/4=8
        1/8=8 (16HT)
        1/6=6 (12HT)
        """
        try:
            res = self.results.get('lscpu').splitlines()
        except Exception:
            return '?/?=??'
        threads = int([item for item in res if item.startswith('Thread(s) per core:')][0].split()[-1])
        cores = int([item for item in res if item.startswith('Core(s) per socket')][0].split()[-1])
        sockets = int([item for item in res if item.startswith('Socket(s):')][0].split()[-1])
        cores_sum = sockets * cores
        return '{sockets}/{cores}={count}{if_HT}'.format(
            sockets=sockets, cores=cores, count=cores_sum,
            if_HT=' ({}HT)'.format(cores_sum * 2) if threads >= 2 else '')

    @property
    def cpu_ghz(self):
        """
        @ 3.20GHz
        @ 3.50GHz
        """
        num = self.cpu_name.split("@")[-1]
        return f'@{num}'

    @property
    def gpu_name(self):
        """
        NVIDIA Corporation GM204GL [Quadro M4000] (rev a1)
        NVIDIA Corporation GK106GL [Quadro K4000] (rev a1)
        NVIDIA Corporation GP104GL [Quadro P4000] (rev a1)
        """
        return self.results.get('gpu_name').split('\n')[0]

    @property
    def gpu_driver(self):
        """
        390.116
        340.107
        """
        return self.results.get('gpu_driver').split('\n')[0]

    @property
    def os(self):
        """
        Centos 7.3
        CentOS 7.6
        """
        distrib = self.results.get('os_distributor').split('\n')[0]
        release = '.'.join(self.results.get('os_release').split('\n')[0].split('.')[0:2])
        return '{distrib} {release}'.format(distrib=distrib, release=release)

    @property
    def kernel(self):
        """
        3.10.0-957.5.1.el7.x86_64
        """
        return self.results.get('os_kernel')

    @property
    def monitor(self):
        """
        [monitor(connector='DP-4', name='DELL-U2518D',
                 resolution='2560x1440', serial='3C4YP93D875L',
                 build='20190324', age=0.28),
         monitor(connector='DP-6', name='DELL-U2518D',
                 resolution='2560x1440', serial='3C4YP93D929L',
                 build='20190324', age=0.28)]
        """
        mon_res = self.results.get('monitor_resolutions')
        # mon_names = self.results.get('monitor_names')
        mon_info = self.results.get('monitor_info')

        resolutions = re.findall(r'\d*x\d*', mon_res)
        connectors = re.findall(r'^.*-[\d.]*', mon_res, flags=re.MULTILINE)

        # names = [name.split('(')[0].strip() for name in mon_names.split('\n') if name]
        # mon_names = dict(zip(connectors, names))
        # print(names)

        matches = re.findall(r'BorderDimensions.*$|(?:.*?EDID:)\s+([a-f\d\s]+)\s+', mon_info)
        edids_encoded = [''.join(match.split()) for match in matches]

        out = subprocess.check_output(['./monitor-names.sh', mon_info]).decode('UTF-8').splitlines()
        names = [name.replace(' ', '-') for name in out]

        monitor = collections.namedtuple('monitor', ['connector', 'name', 'resolution', 'serial', 'build', 'age'])
        monitors = []
        edids_decoded = []
        serial_numbers = []
        for conn, edid, name, resol in zip(connectors, edids_encoded, names, resolutions):
            filename = join(abspath(curdir), 'EDID__{host}__{connector}'.format(host=self.hostname, connector=conn))
            with open(filename, 'w') as f:
                f.writelines(edid)
            proc = subprocess.Popen(['edid-decode', filename],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out, err = proc.communicate()
            os.remove(filename)
            edid_decoded = out.decode('UTF-8').splitlines()
            edids_decoded.append(edid_decoded)

            serial_number = [item.split(': ')[1] for item in edid_decoded if item.startswith('Serial number:')][0]
            serial_numbers.append(serial_number)

            build_date_splitted = [item for item in edid_decoded if item.startswith('Made week')][0].split()
            week, year = build_date_splitted[2], build_date_splitted[4]

            # dtm = datetime.datetime.strptime('{}W{} MON'.format(year, week), '%YW%U %a')
            dtm = datetime.datetime.strptime('{}-W{}'.format(year, week) + '-0', "%Y-W%W-%w").date()
            build_date = datetime.datetime.strftime(dtm, "%Y%m%d")

            # How many years (2 float) is the monitor old
            age_years = round((datetime.date.today() - dtm) / datetime.timedelta(days=365.2425), 2)

            monitors.append(monitor(
                connector=conn, name=name, resolution=resol, serial=serial_number, build=build_date, age=age_years)
            )
            filename = join(abspath(curdir), 'EDID__{host}__{connector}__{name}__{resol}__{serial}__{build}'.format(
                host=self.hostname, connector=conn, name=name, resol=resol, serial=serial_number, build=build_date))
            with open(filename, 'w') as f:
                f.writelines(edid)
                f.write('\n')
                f.write('=' * 70)
                f.write('\n')
                f.writelines(['{line}\n'.format(line=line) for line in edid_decoded])
            # os.remove(filename)
        return monitors

    @property
    def local_ip(self):
        """
        10.0.23.78
        10.0.23.35
        """
        return self.results.get('local_ip')

    @property
    def public_ip(self):
        """
        194.212.223.78
        """
        return self.results.get('public_ip')

    @property
    def uptime(self):
        """
        8 days
        26 days
        """
        uptime_time = self.results.get('uptime_all').split(',')[0]
        return ' '.join(uptime_time.split()[2:])

    @property
    def drives(self):
        """
        [
            drive(size='238.5G', serial='TW03YYV3550854485046', name='LITEON_IT_LCS-25'),
            drive(size='465.8G', serial='WD-WCC2EXY87606', name='WDC_WD5000AAKX-7')
        ]
        [drive(size='477G', serial='S23SNXAH201288', name='SAMSUNG_SSD_PM87')]
        """
        ret = self.results.get('drives').splitlines()[1:]
        size = [drive.strip().split()[2] for drive in ret]
        serial = [drive.strip().split()[4] for drive in ret]
        name = ['_'.join(drive.strip().split()[5:]) for drive in ret]

        drive = collections.namedtuple('drive', ['size', 'serial', 'name'])
        drives = []
        for size, serial, name in zip(size, serial, name):
            drives.append(drive(size, serial, name))
        return drives

    @property
    def memory(self):
        """
        128 GB
        64 GB
        """
        ret = self.results.get('dmi_memory_array').splitlines()
        sizes = [int(line.split(':')[1].replace('GB', '').strip())
                 for line in ret if 'Range Size: ' in line]
        return f'{sum(sizes)} GB'

    @property
    def computer_age(self):
        """
        03/09/2016
        02/28/2014
        """
        ret = self.results.get('dmi_bios').splitlines()
        release = [line.split(':')[1].strip() for line in ret if 'Release Date: ' in line][0]
        return release

    @property
    def warranty_status(self):
        """
        (3.3, True)
        (5.3, '')
        (8.7, '')
        """
        # dtm = datetime.datetime.strptime('{}-W{}'.format(year, week) + '-0', "%Y-W%W-%w").date()
        # build_date = datetime.datetime.strftime(dtm, "%Y%m%d")

        # age_years = round((datetime.date.today() - dtm) / datetime.timedelta(days=365.2425), 2)
        year, day, month = [int(item) for item in self.computer_age.split('/')[::-1]]
        release_date = datetime.date(year, month, day)
        today = datetime.date.today()
        age_years = round((today - release_date) / datetime.timedelta(days=365.2425), 1)
        if age_years < 5:
            return (age_years, True)
        return (age_years, '')

    @property
    def system_name(self):
        """

        """
        name = [line.split(': ')[-1] for line in self.results.get('dmi_system').split('\n')
                if 'Product Name' in line]
        only_number = [word for word in name[0].split()
                       if any(char.isdigit() for char in word)]
        return only_number[0]

    @property
    def system_user(self):
        """

        """
        return self.results.get('user')
