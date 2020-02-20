# Caching Network with LRU

 - Requirements:
 
- [x] Simplicity. Integration needs to be dead simple

      Integration is really simple as shown on this readme
- [x] Resilient to network failures or crashes

      Socket network created for resilience and consistence. If a node drops the node Network will survide. If a node connection is cut off, the node will be standalone until connection is recovered and reconnect to nodeNetwork.
- [x] Near real time replication of data across Geolocation. Writes need to be in real time.

      Socket handle the real time replication
- [x] Data consistency across regions

      If the cache changes in A it will be reflected in B,C,D... on network
- [x] Locality of reference, data should almost always be available from the closest region

      Probably the half implementation of this module, the cache will update as fast as the connection, if conection A->B is closer than A->C but the connection is way better on A->C probably this network will be synced faster
- [x] Flexible Schema

      The Schema is dead simple and flexible, (key,Value) the value can be anything the user want to be     
- [x] Cache can expire

      The Cache Tail will expire default 60 seconds, can be set on network.CacheNetwork(expire_after=seconds), it will be the same expire time across the network
   
   
   I opted for creating a interconected cache network, only using basic and built-in packages.
   
   Note that if you wanna try this code, either you will need to run as a program (this method is good for creating server, for safe heaven) or install the package and import it, if you import the file directly it will raise an import error. Please follow the 'usage as module' down bellow.
   
   Usage connection method:
    
      To start a network, only need to run as a program, or if you like import and run without any imputs.
      
      To conect a node to an existing network, provide the input join='ip' ip => any network's node IP, the network will auto sync the data and existing nodes.
      
      Default Args:
      
            CacheNetwork(
              port=5000 << Socket Port
              join=None << IP for network connection 'None' to start a new, IP to connect to a existing network
              max_size=1000 << max size for lru cache
              expire_after=60 << expire time for lru cache
            )
   Usage as a module:
    
      - install method
      
            cd question_c folder
            python setup.py install or develop
      
      - usage method
        - start a network
        
              import lru_networking
              network = lru_networking.CacheNetwork()
        
        - connect to a network
        
              import lru_networking
              network = lru_networking.CacheNetwork(join='ip')
        
      - usage API
       
              network.get_key(key) << get key on cache
              network.set_key(key, value) << save/update (key,value) on cache
              network.spy() << get entire cache without touching it
              
              @network.cache_io << decorator for caching function/method I/O
              function_foo
