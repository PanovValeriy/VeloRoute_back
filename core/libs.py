def ip2int(ip_str):
    ip_int = 0
    ip_arr = list(map(int, ip_str.split('.')))
    for i in range(4):
        ip_int += 256 ** i * ip_arr[3 - i]
    return ip_int


def int2ip(ip_int):
    ip_arr = [0, 0, 0, 0]
    for i in range(4):
        ip_arr[3 - i] = ip_int % 256
        ip_int = ip_int // 256
    return '.'.join(map(str, ip_arr))

def calcCodeTrue(pk, type):
    return str(((pk + 108) * 6 - 77) // 4 + type)[::-1]
