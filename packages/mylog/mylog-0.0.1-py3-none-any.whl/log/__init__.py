
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def fail(msg):
    error(msg)

def error(msg):
    print(bcolors.FAIL + str(msg) + bcolors.ENDC)

def errorStr(msg):
    return bcolors.FAIL + str(msg) + bcolors.ENDC


def warn(msg):
    print(bcolors.WARNING + str(msg) + bcolors.ENDC)

def warnStr(msg):
    return bcolors.WARNING + str(msg) + bcolors.ENDC


def debug(msg):
    print(bcolors.OKBLUE + str(msg) + bcolors.ENDC)


def green(msg):
    print(bcolors.OKGREEN + str(msg) + bcolors.ENDC)