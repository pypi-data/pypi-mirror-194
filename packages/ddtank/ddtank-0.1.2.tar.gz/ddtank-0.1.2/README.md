# DDTank

A package used for writing ddtank game scripts.

Contact the author: jugking6688@gmail.com 

Video tutorial in bilibili: https://space.bilibili.com/3493127383943735

Examples are as follows：
```python
from ddtank import Status, get_game

class ScriptStatus(Status):
    def task(self):
        while True:
            self.press('B')

if __name__ == '__main__':
    handle_list = get_game()
    handle = handle_list[0]
    my_status = ScriptStatus(handle)
    my_status.start()
    my_status.stop()
```

Note: ver 0.1 is incompatible with previous version! But the general idea is the same.