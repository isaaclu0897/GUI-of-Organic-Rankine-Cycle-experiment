import time
import threading


def fun():
    print("start fun")
    time.sleep(2)
    print("end fun")


print("main thread")
t1 = threading.Thread(target=fun,args=(), daemon=True)

# t1.setDaemon(True)
t1.start()
time.sleep(1)
print("main thread end")
