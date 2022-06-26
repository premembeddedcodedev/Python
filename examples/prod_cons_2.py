#!/usr/bin/env python

from collections import deque
from threading import Thread,Condition

QUEUE = deque()

def an_item_is_available():
    return bool(QUEUE)

def get_an_available_item():
    return QUEUE.popleft()

def make_an_item_available(item):
    QUEUE.append(item)

def consume(cv):
    cv.acquire()
    while not an_item_is_available():
        cv.wait()
    print('We got an available item', get_an_available_item())
    cv.release()

def produce(cv):
    cv.acquire()
    make_an_item_available('an item to be processed')
    cv.notify()
    cv.release()

def main():
    cv = Condition()
    Thread(target=consume, args=(cv,)).start()    
    Thread(target=produce, args=(cv,)).start()

if __name__ == '__main__':
    main()
