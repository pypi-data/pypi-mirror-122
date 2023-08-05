from qsync import SyncIniter
from sys import argv

HELP_MSG = """

### START SYNC ONE WAY :

> sync_module "src_dir" "dst_dir" false

### START SYNC BIDIRECTIONNAL :

> sync_module "dir1" "dir2" true

"""


def main():
    if len(argv) == 4:
        sync_src = argv[1].replace("\\","/")
        sync_dst = argv[2].replace("\\","/")
        if argv[3] == "false" :
            bi_d = False
        elif argv[3] == "true":
            bi_d = True
        else:
            print(HELP_MSG)
            exit(0)
    else:
        print(HELP_MSG)
        exit(0)

    s = SyncIniter(sync_src,sync_dst,bi_directionnal=bi_d)
    s.start_sync()
    print(f"started to sync, bi directionnal mode : {bi_d}")


if __name__ == "__main__":
    
    main()