import random
import threading
import time

from werkzeug.local import LocalStack

thread_data_stack = LocalStack()

#Thread로 실행할 함수
def long_running_function(thread_index):

    thread_data_stack.push({'index': thread_index, 'thread_id' : threading.get_native_id()})
    print(f'Starting thread #{thread_index} ... {thread_data_stack}')
    
    time.sleep(random.randrange(1,11))

    print(f'LocalStack contains : {thread_data_stack.top}')
    print(f'Finished thread #{thread_index}')
    thread_data_stack.pop()

def thread_test(thread_index):
    for i in range(10):
        print(i)
        time.sleep(1)

if __name__ == "__main__":
    threads = []


    #Thread 3개 추가
    for index in range(3):
        thread = threading.Thread(target=long_running_function, args=(index,))
        thread2 = threading.Thread(target=thread_test, args=(index,))
        threads.append(thread)
        threads.append(thread2)
        thread.start()
        thread2.start()

    for thread in threads:
        thread.join()

    print('Done!')