
import ModuleType
import firestore as fs
import time

current_quota = 50

def go():
    ModuleType.init_module()
    while True:
        time.sleep(30)
        count = fs.check_count()
        if count >= 5000:
            print("That's all for now!")
            break
        if count >= current_quota:
            try: 
                data = fs.batched_read()
                ModuleType.run(count, data[0], data[1]) ##one epoch for every data point for now
                current_quota = current_quota*2

            except Exception as e:
                print(e)
                current_quota = int(current_quota / 2)
                continue
