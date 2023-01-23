import random
import threading
import time

from werkzeug.local import LocalStack

thread_data_stack = LocalStack()

def long_running_function(thread_index):

    thread_data_stack.push({'index': thread_index, 'thread_id' : threading.get_native_id()})
    print(f'Starting thread #{thread_index} ... {thread_data_stack}')
    
    time.sleep(random.randrange(1,11))

    print(f'LocalStack contains : {thread_data_stack.top}')
    print(f'Finished thread #{thread_index}')
    thread_data_stack.pop()

if __name__ == "__main__":
    threads = []

    for index in range(3):
        thread = threading.Thread(target=long_running_function, args=(index,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print('Done!')