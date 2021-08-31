#
# Fluent Python 18 챕터 (asyncio)의 18-2 번 예제입니다.
# 쓰레드와 코루틴을 비교하기 위한 코드로, spinner_thread.py 파일과 대조하여 보는 것이 좋습니다.
#
# + 책 내의 Line 34 코드는 asyncio.async() 로 되어있으나, 
# 해당 문법은 파이썬 3.4.4 부터 deprecated 되어 asyncio.ensure_future로 교체하였습니다.

import asyncio
import itertools
import sys

@asyncio.coroutine
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            yield from asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():
    yield from asyncio.sleep(3)
    return 42

@asyncio.coroutine
def supervisor():
    spinner = asyncio.ensure_future(spin('thinking!'))
    print('spinner object:', spinner)
    result = yield from slow_function()
    spinner.cancel()
    return result

def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()