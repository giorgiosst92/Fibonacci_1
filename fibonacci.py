import time
import matplotlib.pyplot as plt
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

# read the digit param from the config file
digits = config.get('processing', 'digits')

# initialize variables
axis_x_mem = []
axis_y_mem = []

cache = {}
stopFib = False


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        delta = (time2 - time1) * 1000.0
        axis_y_mem.append(delta)
        # print('{:s} function took {:.3f} ms'.format(f.__name__, delta))

        return ret

    return wrap


def fibonacci(n):
    # if the value is stored into the cache, use that value
    if n in cache:
        return cache[n]

    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n > 2:
        value = fibonacci(n - 1) + fibonacci(n - 2)

        if len(str(value)) == int(digits):
            global stopFib
            stopFib = True
            print("index: ",n," - digits: ",len(str(value)))

    # Cache the value and return it
    cache[n] = value

    return value


@timing
def execute_fibonacci(i):
    for n in range(1, i + 1):

        fibonacci(n)


if __name__ == "__main__":

    time1 = time.time()
    n = 0
    while True:
        n += 1
        axis_x_mem.append(n)

        execute_fibonacci(n)
        if stopFib:
            break

    plt.plot(axis_x_mem, axis_y_mem, 'ro', label='+ memorization')

    plt.ylabel('time [ms]')
    plt.xlabel('iterations')
    plt.title("Fibonacci sequence")
    plt.legend()

    time2 = time.time()
    delta = (time2 - time1) * 1000.0
    print('Fibonacci index search took {:.3f} ms'.format(delta))

    plt.show()
