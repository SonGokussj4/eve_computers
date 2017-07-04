# from pssh.pssh_client import ParallelSSHClient, SSHClient
# from pssh.utils import load_private_key
# from pswd import pswd
# # pkey = load_private_key('/home/jverner/.ssh/known_hosts')

# hosts = ['ogg', 'esme', 'klatch', 'carrot']
# client = ParallelSSHClient(hosts, user='jverner', password=pswd)
# # client = ParallelSSHClient(hosts, user='jverner')

# cmd = 'cat /dev/shm/xrandrprops.info'
# output = client.run_command(cmd, stop_on_errors=False)

# # print(output)
# for key, val in output.items():
#     for item in val.stdout:
#         print(item)


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
"""


import re
import subprocess
import collections
from multiprocessing import Pool, cpu_count

# on hold: sarina, detritus, eskymak (old SUSE linux, waiting for CENTOS)
hosts = ['galaxy', 'klatch', 'ogg', 'nina', 'gapa', 'sarita', 'nindra', 'ook', 'swires',
         'carrot', 'tigerfly', 'sally', 'cuddy', 'havelock', 'tacticus', 'esme',
         'gemma', 'esk', 'myron',
         'morkie', 'klotz', 'quoth', 'quirm', 'shawn', 'ego', 'fate', 'irulan', 'hrun',
         'koch', 'shelly', 'modo', 'moist']


def receive_data(host):
    try:
        out = subprocess.check_output(['ncat', '--recv-only', host, '6556'], timeout=2)
        print('{host} .. OK'.format(host=host))
    except subprocess.TimeoutExpired as e:
        print('{host} .. '.format(host=host), end='')
        print('TIMEOUT EXPIRED: {e}'.format(e=e))
        out = ''
    except subprocess.CalledProcessError as e:
        print('{host} .. '.format(host=host), end='')
        print('CALLED PROCESS ERROR: {e}'.format(e=e))
        out = ''
    except Exception as e:
        print('{host} .. '.format(host=host), end='')
        print('UNKNOWN EXCEPTION: {e}'.format(e=e))

    return {host: out.decode('UTF-8') if out else str()}


def main():
    pool = Pool(cpu_count())
    # p = Pool(2)
    result = pool.map(receive_data, hosts)
    pool.close()
    pool.join()

    print("Done!")
    # print(len(result), [key.keys() for key in result])
    results = collections.defaultdict(list)
    for d in result:
        for key, val in d.items():
            results[key] = val

    print("Done again!")


    print("Divide check_mk_agent results into dictionaries")
    computers = collections.defaultdict(dict)
    for host, output in results.items():
        res = [item for item in re.split(r'(<<<.*?>>>)', output) if item]
        for idx in range(0, len(res), 2):
            new_key = res[idx].replace('<<<', '').replace('>>>', '')
            if new_key in computers[host].keys():
                computers[host].update({re.sub(new_key, '{}_2'.format(new_key), new_key): res[idx + 1].strip()})
            else:
                computers[host].update({new_key: res[idx + 1].strip()})

    computers = collections.OrderedDict(sorted(computers.items()))

    for key, val in computers.items():
        screen_info = val.get('monitor_info')
        # if screen_info:
        #     matches = re.findall(r'BorderDimensions.*$|(?:.*?EDID:)\s+([a-f\d\s]+)\s+', screen_info)
        #     matches = [''.join(match.split()) for match in matches]
        #     print(key, matches)
        local_ip = val.get('local_ip', '?')
        uptime = val.get('uptime_all', '?')
        gpu_driver = val.get('gpu_driver', '?')
        print('{host:<10} ... Local_IP = {ip:<12} Uptime = {uptime:<70} gpu_driver = {gpu_driver}'.format(
            host=key, ip=local_ip, uptime=uptime, gpu_driver=gpu_driver.replace('\n', '')))


    #
    #     print("uptime", key, uptime)



    # for pc, data in computers.items():
    #     print(data.keys())
    #     print()


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

