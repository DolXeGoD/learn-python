#
# Fluent Python 18 챕터 (asyncio)의 18-1 번 예제입니다.
# 쓰레드와 코루틴을 비교하기 위한 코드로, spinner_asyncio.py 파일과 대조하여 보는 것이 좋습니다.
#

import threading
import itertools
import time
import sys

class Signal:
    go = True

def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        time.sleep(.1)

        if not signal.go:
            break
    
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():
    time.sleep(1)
    return 42

def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=('thinking!', signal))

    print('spinner object:', spinner)
    spinner.start()

    result = slow_function()
    signal.go = False
    spinner.join()
    return result

def main():
    result = supervisor()
    print('Answer:', result)

if __name__ == '__main__':
    main()
