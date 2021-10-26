import psutil

print(psutil.cpu_percent(interval=1, percpu=False)) # CPU Percentage
print(psutil.cpu_freq().max) # CPU Frequency
print(psutil.cpu_count()) # CPU Thread Count
print(psutil.virtual_memory()[2]) # Virtual Memory Percentage
print(psutil.net_if_addrs()['Ethernet'][1][1]) # IP Address