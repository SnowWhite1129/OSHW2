import threading

thread_array = []

def hello_thread():
    global tid_array
    tid = threading.get_ident()
    tid_array.append(tid)
    print("Hello ", tid)


def main():
    global thread_array
    for i in range(2):
        thread = threading.Thread(target = hello_thread)
        thread_array.append(thread)
        thread.start()
    for thread in thread_array:
        thread.join()
    print("End")

if __name__ == "__main__":
    main()    