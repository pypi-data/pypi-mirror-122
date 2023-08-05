# SYNC_MODULE

## introduction
> sync_module is the simplest way to set-up a one/two ways syncronisations between folders from a python script ! just use it like so :

```python
# import the module
from qsync import SyncIniter

from sys import argv # here to get command lines args

if __name__ == "__main__":
    
    # define your 2 folders path (here the command line arguments)
    sync_src = argv[0].replace("\\","/")
    sync_dst = argv[1].replace("\\","/")

    # create a SyncIniter object with the two sync source and destination (commutative if bi directionnal)
    s = SyncIniter(sync_src,sync_dst,bi_directionnal=True)

    # do I really need to explain the rest ?  
    s.start_sync()
    print("started to sync")
    s.stop_sync()
    print("stopped to sync")

    
```

## A cli is also available with this module :

#### Start to sync two folders in one way :
> qsync "src_dir" "dst_dir" false

#### start to sync two folders in two ways :

> qsync "dir1" "dir2" true
 

## Errors :

#### InvalidPathError
> raised in start_sync() when a path don't exists