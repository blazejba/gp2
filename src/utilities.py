import time

def get_date_in_string():
    date = time.localtime()
    return str(date.tm_year) + '_' + str(date.tm_mon) + '_' + \
           str(date.tm_mday) + '_' + str(date.tm_hour) + '_' + \
           str(date.tm_min) + '_' + str(date.tm_sec)


def decode_stdout(stdout):
    stdout = stdout.decode('ascii')
    index, fitness = [x for x in stdout.split(',')]
    return index, fitness