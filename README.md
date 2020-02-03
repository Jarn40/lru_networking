# ormuco
Tests requested for position.


- Question A

    A program that checks if there is intersection between 2 lines.

    Usage:
    
      python program.py x1 x2 x3 x4
      
    Module Usage:
      import question_a.program as program
      program.has_intersection(x1, x2, x3, x4)

- Question B

    A program/module that compare 2 version values, and return a string with the relationship between them.
    Usage as a program:
    
      python version_compare_module.py v1 v2
      
    Usage as a module:
    
      - install method
      
        cd question_b folder
        python setup.py install or develop
      
      - usage method
      
        import version_compare
        version_compare.version_compare(v1,v2)
        
 - Question C
 
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
        
              import lru_ormuco
              network = lru_ormuco.CacheNetwork()
        
        - connect to a network
        
              import lru_ormuco
              network = lru_ormuco.CacheNetwork(join='ip')
        
      - usage API
       
              network.get_key(key) << get key on cache
              network.set_key(key, value) << save/update (key,value) on cache
              network.spy() << get entire cache without touching it
              
              @network.cache_io << decorator for caching function/method I/O
              function_foo
  
 
![](https://lh3.googleusercontent.com/hMJp3-Y1D_3pXzgjoKOrXT5PSbev_oghFu4NzQQ9DKppRFPzJPxYPl-tK9SVWDEOMBgWhbkPC23V72Mo-XnyyHlk5IgnzEyzIZEikxqJhchW3neOd91crbQNOF01u4LUSF2D_Ev5eY0ouKNZ9VQ7k_2zfPwXQhavDKMvXMd1zjfAca50p-3hapuKH2cGAs2K34A1e9n-orw35pyu78onNgQY45SRpso-66bRgZsYzPW7PixOkSFZRl4Ahf8BWttMaGzzPeyfXKedUu1cI0dcw9nespbHWabl-wmhPw8wUlJEpQEIdLHeEmEiQ-HABscTAf6f9QjtYohNIFSkPYqUTlezrEsF0r_AwwgAgE3X7gmiA_2ilU-gQAq0M4iRUDkeeqyrPeDUPuhSlQekcuSksr99flcUbWOHPKjYTNZr3ttEEResilXFxBYetpYDfrKWtIkzB3HlP7Q-CX7fnl7XqQ0ZexOs5FMBMfqtEBpve9axLXKrW6SRSh9etEZi9wbDsJdH-_2xQBP7oqnGsqJe8FCD3VZ1wWDkmWrhwwi0i8emh6Pe1fM1AGmfC1vhTs4UFUpNnsxZpv571K6am8ZMFpfew_OcSP2QmmJB-3EibcNvfNLijcaGQDp5uB3VkfmK0ELIqjTUtqZhrSaDm2ueWnJ3OdXK_G5yWq3_cnfA-Yfsn53cq4ELmHZW=w874-h657-no)
   
   All test on question c was made using localmachine plus 2+ remote connected with putty, Windows and linux, tested network consistence, read, write operations and cache syncing. Demostrated on video below.
