#!/expSW/SOFTWARE/bin/python3.7eve

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

from multiprocessing import Pool, cpu_count
from Host import Host

# DELL WARRANTY
# https://gist.github.com/teroka/0720274b87b77fe7171f

#=========================================
# C2
#=========================================
hosts = [
    'winder',
    'ogg', 'koch', 'tigerfly',
    'klatch', 'nina', 'moist', 'sarita',
    'nindra', 'morpork', 'sybil',
    'cohen', 'winvoe', 'gapa', 'dorfl',
    'modo', 'sally',
    'cuddy', 'havelock', 'tacticus',
    'coin',
]

#=========================================
# C6
#=========================================
# hosts = [
#     'samuel', 'detritus', 'buckleby',
#     'hrun', 'shelly', 'fate',
#     'bucket', 'ego', 'shawn',
#     'quirm', 'quoth', 'klotz', 'morkie'
# ]

#=========================================
# Dalsi
#=========================================
# hosts = [
#     'esme', 'gemma', 'esk', 'sarina', 'myron', 'eskymak'
# ]

# timeout = 5  # timeout for ncat in sec


def main():
    pool = Pool(cpu_count())
    results = pool.map(Host, hosts)
    pool.close()
    pool.join()

    # print("Done!")
    # print('{: <10}{: <15}{: <8}{: <12}{: <9}{: <5}'.format(
    #       'Host', 'CPU details', 'Memory', 'Built Date', 'Warranty', 'Age'))

    print(f'{"Host":<15}{"Memory":<15}{"Computer Age":<20}{"User":<20}{"Monitor Serials":<20}')

    for item in results:
        item: Host
        if not item.received:
            # print()
            print(f'{item.hostname: <15}cannot connect...')
            continue

        # TESTS
        #==============================================================
        # print()
        # print('{host: <10}{cpu_details: <15}{memory: <8}'
        #       '{built_date: <12}{warranty: <9}{age: <5}'.format(
        #           host=item.hostname, cpu_details=item.cpu_details, memory=item.memory,
        #           built_date=item.computer_age, warranty=str(item.warranty_status[1]),
        #           age=item.warranty_status[0]))
        # print("[{size}] - {name}".format(size=item.drives[0].size, name=item.drives[0].name))
        # except Exception as e:
        #     print('Exception: {}'.format(e))
        #     continue

        # ALL INFORMATION
        #==============================================================
        # print("")
        # print("DEBUG: item.hostname:", item.hostname)
        # print("DEBUG: item.location:", item.location)
        # print("DEBUG: item.cpu_name:", item.cpu_name)
        # print("DEBUG: item.cpu_details:", item.cpu_details)
        # print("DEBUG: item.cpu_ghz:", item.cpu_ghz)
        # print("DEBUG: item.gpu_name:", item.gpu_name)
        # print("DEBUG: item.gpu_driver:", item.gpu_driver)
        # print("DEBUG: item.os:", item.os)
        # print("DEBUG: item.kernel:", item.kernel)
        # print("DEBUG: item.monitor:", item.monitor)
        # print("DEBUG: item.local_ip:", item.local_ip)
        # print("DEBUG: item.public_ip:", item.public_ip)
        # print("DEBUG: item.uptime:", item.uptime)
        # print("DEBUG: item.drives:", item.drives)
        # print("DEBUG: item.memory:", item.memory)
        # print("DEBUG: item.computer_age:", item.computer_age)
        # print("DEBUG: item.warranty_status:", item.warranty_status)
        # print("DEBUG: item.system_name:", item.system_name)
        # print("DEBUG: item.system_user:", item.system_user)

        # EXCEL format
        #==============================================================
        print()
        print(item.system_user)
        print(item.hostname, item.memory)
        print(item.cpu_details)
        print(item.os)
        print(item.system_name, item.cpu_ghz)
        print(item.gpu_driver)

        # EXCEL Table
        #==============================================================
        # try:
        #     monitor_serials = ', '.join([val.serial for val in item.monitor])
        #     print(f'{item.hostname:<15}{item.memory.split()[0]:<15}{item.computer_age:<20}{item.system_user:<20}{monitor_serials:20}')
        # except Exception:
        #     print(f'{item.hostname:<15}failed... for some reason.')


if __name__ == '__main__':
    main()





# import concurrent.futures
# import urllib.request

# URLS = ['http://www.foxnews.com/',
#         'http://www.cnn.com/',
#         'http://europe.wsj.com/',
#         'http://www.bbc.co.uk/',
#         'http://some-made-up-domain.com/']

# # Retrieve a single page and report the URL and contents
# def load_url(url, timeout):
#     with urllib.request.urlopen(url, timeout=timeout) as conn:
#         return conn.read()

# # We can use a with statement to ensure threads are cleaned up promptly
# with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#     # Start the load operations and mark each future with its URL
#     future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
#     for future in concurrent.futures.as_completed(future_to_url):
#         url = future_to_url[future]
#         try:
#             data = future.result()
#         except Exception as exc:
#             print('%r generated an exception: %s' % (url, exc))
#         else:
#             print('%r page is %d bytes' % (url, len(data)))






# import concurrent.futures
# ls = []
# with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
#     for host, data in zip(hosts, executor.map(receive_data, hosts)):
#         ls.append(host)
#         print(host)

# print(len(ls))

