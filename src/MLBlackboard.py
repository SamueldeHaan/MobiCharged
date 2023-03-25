
import ModuleType
import firestore as fs
import time

current_quota = 5000 #changed from 50

def go():
    global current_quota
    ModuleType.init_module()
    while True:
        count = fs.check_count()
        if count >= 5000:
            print("That's all for now!")
            break
        if count >= current_quota:
            try: 
                # print("accessing data")
                data = fs.batched_read()
                # print("data read")
                ModuleType.run(count, data[0], data[1]) ##one epoch for every data point for now
                current_quota = count*2

            except Exception as e:
                print(e)
                current_quota = int(current_quota / 2)
                continue
        else:
            print("Waiting for data. Current count is: " + str(count))
        time.sleep(20)


go()