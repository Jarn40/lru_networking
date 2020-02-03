'''lru module created by hand with timeout'''
# import json
import time
from threading import Thread

class LRUNode():
    '''actual lru node for linked list creation'''
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
        self.time_alocated = None

    def update_timer(self):
        '''method responsable for updating node expiration time'''
        self.time_alocated = time.time()

    def manual_timer(self, expire):
        '''method for sync purpose'''
        self.time_alocated = float(expire)

    def __str__(self):
        '''built-in method for printing value if object is printed'''
        return f'{self.key}, {self.value}, {self.time_alocated}'

class LRUCache():
    '''LRU class for caching'''
    def __init__(self, max_size=1000, expire_after=60):
        """
        LRU Cache with default size of 10 and tail expire time of 1 min.
        """
        if max_size <= 0:
            raise ValueError("max_size > 0")
        self.cache_map = {}

        self.head = None
        self.end = None

        self.max_size = max_size
        self.current_size = 0
        self.time_limit = expire_after
        self.stop_check = False

        self.check_expire_thread = Thread(target=self.check_expire, name='Check Expire')
        self.check_expire_thread.setDaemon(True)
        self.check_expire_thread.start()

    def check_expire(self):
        '''threading method for check if node expiration time was reached'''
        while 1:
            if self.stop_check:
                break
            if not self.end:
                continue
            tail = self.end
            if time.time() - tail.time_alocated >= self.time_limit:
                print(f"TAIL {tail} => Expired")
                del self.cache_map[tail.key]
                next_tail = tail.next
                self._remove(tail)
                self.end = next_tail

    def spy(self):
        '''Method to see entire LRU cache without touching it'''
        current = self.head
        ref_pos = 0
        lru_map = {}

        while current:
            if ref_pos == 0:
                lru_map['[head]'] = {
                    'key':current.key,
                    'value': current.value,
                    'expire': current.time_alocated
                }
            elif ref_pos == self.current_size -1:
                lru_map['[tail]'] = {
                    'key':current.key,
                    'value': current.value,
                    'expire': current.time_alocated
                }
            else:
                lru_map[f'[node-{ref_pos}]'] = {
                    'key':current.key,
                    'value': current.value,
                    'expire': current.time_alocated
                }
            ref_pos += 1
            current = current.prev
        # print(json.dumps(lru_map, indent=4, separators=("  ↓", " -> ")))
        return lru_map


    def get_key(self, key):
        """
        Method for get and update LRU key
        """
        if key not in self.cache_map.keys():
            return -1

        node = self.cache_map[key]

        if self.head == node:
            return node.value
        self._remove(node)
        self._set_head(node)
        return node.value

    def set_key(self, key, value):
        """
        Method for write or update a LRU key
        """
        if key in self.cache_map.keys():
            node = self.cache_map[key]
            node.value = value

            if self.head != node:
                self._remove(node)
                self._set_head(node)
        else:
            new_node = LRUNode(key, value)
            if self.current_size == self.max_size:
                del self.cache_map[self.end.key]
                self._remove(self.end)
            self._set_head(new_node)
            self.cache_map[key] = new_node


    def _set_head(self, node, sync=False):
        '''Private methode for setting the head of LRU'''
        if not self.head:
            self.head = node
            self.end = node
        else:
            node.prev = self.head
            node.next = None
            self.head.next = node
            self.head = node
        if not sync:
            node.update_timer()
        self.current_size += 1


    def _remove(self, node):
        '''Private methode for removing a LRU node'''
        if not self.head:
            return -1

        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

        if not node.next and not node.prev:
            self.head = None
            self.end = None

        if self.end == node:
            self.end = node.next
            self.end.prev = None
        self.current_size -= 1
        return node

    def sync_key(self, node):
        """
        Method for sync LRU key
        """
        new_node = LRUNode(node.key, node.value)
        new_node.manual_timer(node.expire)
        self._set_head(new_node, True)
        self.cache_map[node.key] = new_node
