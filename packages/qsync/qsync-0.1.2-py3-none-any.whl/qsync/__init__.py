from os import path, walk, mkdir, remove
from multiprocessing import Process
from json import dumps, loads
from distutils.dir_util import remove_tree
from time import sleep, ctime
from datetime import datetime
from shutil import copy2
from random import randint

# all errors
class InvalidPathError(Exception):

    def __init__(self,path) -> None:
        self.message = "This path does not exists : " + path
        super().__init__(self.message)



# real shit 0_0
class SyncIniter():

    """
    this class contains all the necessary to start a one/twos ways sync
    """

    def __init__(self,sync_src,sync_dst, bi_directionnal=True):
        self.bi_directionnal = bi_directionnal
        self.sync_src = sync_src
        self.sync_dst = sync_dst
        self.tmp_file = f"{randint(10**9,10**12)}.conf"


    def __check_file_integrity(self):

        if (not path.exists(self.sync_src)):
            raise InvalidPathError(self.sync_src)
        elif (not path.exists(self.sync_dst)):
            raise InvalidPathError(self.sync_dst)

    def start_sync(self):
        """
        basically start the sync processes
        """

        self.__check_file_integrity()
        # first sync way
        self.s1 = Process(target=SyncProcess(
            self.sync_src, self.sync_dst, self.tmp_file).start)
        self.s1.start()


        if self.bi_directionnal:
            # second sync way
            self.s2 = Process(target=SyncProcess(
                self.sync_dst, self.sync_src, self.tmp_file).start)

            self.s2.start()

    def stop_sync(self)->None:
        """
        stop the two sync processes (or the one if the sync is one way)
        """
        self.s1.kill()
        if self.bi_directionnal:
            self.s2.kill()

        remove(self.tmp_file)


class SyncProcess():

    """

    This class contains all the necessary to init a watchdog and process to sync two folders in one way

    """

    def __init__(self, sync_src: str, sync_dst: str,tmp_file:str):
        self.sync_src = sync_src
        self.sync_dst = sync_dst
        self.tmp_file = tmp_file
        self.map = []
        self.old_map = []
        self.loop_time = 5

    def __sync_process(self)->None:
        """

        the main function of the sync process

        """

        # first directory map
        self.__recursive(self.sync_src)
        self.old_map = self.map
        self.__write_last_op()

        while True:

            self.map = []
            self.__recursive(self.sync_src)
            mod_files = self.__get_files_to_update()

            # loop and compare maps of directories architecture
            if str(self.old_map) != str(self.map):

                if self.__is_sync_safe():

                    print(f"sync map from {self.sync_src} to {self.sync_dst}")

                    for ele in self.map:

                        # build the future path of element
                        tmp = ele.replace(self.sync_src, self.sync_dst)

                        # add non existing folder
                        if path.isdir(ele) and (not path.exists(tmp)):
                            mkdir(tmp) if not path.exists(tmp) else None

                        # add non existing file
                        elif path.isfile(ele) and (not path.exists(tmp)):
                            copy2(ele, tmp)


                    deleted_elements = [
                        ele for ele in self.old_map if ele not in self.map]

                    for ele in deleted_elements:
                        # build the future path of element
                        tmp = ele.replace(self.sync_src, self.sync_dst)

                        # delete existing folder in the other sync that has been deleted here
                        if path.isdir(tmp):
                            remove_tree(tmp)

                        # delete existing file in the other sync that has been deleted here
                        elif path.isfile(tmp):
                            print(f"deleting file : ", tmp)
                            remove(tmp)

                    self.__write_last_op()

                self.old_map = self.map

            # loop throught files that have been modified
            elif (mod_files != []) and self.__is_sync_safe():
                if self.__is_sync_safe():
                    for file in mod_files:

                        # build the future path of element
                        tmp = file.replace(self.sync_src, self.sync_dst)
                        print(
                            f"sync modif from : {self.sync_src} to : {self.sync_dst}")
                        copy2(file, tmp)

                    self.__write_last_op()

            sleep(self.loop_time)

    

    def __get_files_to_update(self) -> list:
        """
            loop throught the map and check if the file modification 
            date is from less than a loop time

        Returns:
            list: the list of files modified that need to be updated on the other end
        """

        files = []
        for ele in self.map:
            if path.isfile(ele):

                now = datetime.now()

                mdate = datetime.strptime(ctime(path.getmtime(ele)),
                                          "%a %b %d %H:%M:%S %Y")

                delta = now - mdate

                if delta.seconds <= self.loop_time:
                    files.append(ele)

        return files

    def __recursive(self, rootdir: str):
        """
        map a directory and his own subdirs, updates self.map
        """

        for root, subdirs, files in walk(rootdir):
            for dir in subdirs:
                sub_root = path.join(rootdir, dir)
                self.map.append(sub_root)
                self.__recursive(sub_root)

            for file in files:
                self.map.append(path.join(rootdir, file))

    def __write_last_op(self):
        try:
            with open(self.tmp_file, "w") as f:
                f.write(
                    dumps({"sync_src": self.sync_src, "sync_dst": self.sync_dst, "old_sync_map": self.old_map, "sync_map": self.map, "date": datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")}))
                f.close()
        except Exception as e:
            # busy file ??
            sleep(self.loop_time)
            self.__write_last_op()


    def __is_sync_safe(self)->bool:
        """
        return True only if last op was from the same sync side or the weight/map has changed
        """

        # make sure no erros are in map (often when a file is moved to the upper folder)
        for i in range(len(self.map)):
            if not path.exists(self.map[i]):

                # make sure the bug/file is removed in both ways
                tmp = self.map[i].replace(self.sync_src, self.sync_dst)

                if path.isdir(tmp):
                    remove_tree(tmp)
                elif path.isfile(tmp):
                    remove(tmp)
                
                # skip a loop time as the folder seems to be in a huge load 
                sleep(self.loop_time)
                
                # refresh the folders mapping
                self.map = []
                self.__recursive(self.sync_src)
                self.__write_last_op()

                return True


        # as it could be edited by the second process at the same time
        # it is necessary to put this block into a try/catch 
        try:
            json = {}
            with open(self.tmp_file, "r") as f:
                json = loads(f.read())
                f.close()
        except Exception as e:
            return False

        f_now = datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")
        now = datetime.strptime(f_now, "%Y-%m-%d-%H-%M-%S")
        last_sync_time = datetime.strptime(
            json['date'], "%Y-%m-%d-%H-%M-%S")
        delta = now - last_sync_time

        return True if (not json['old_sync_map'] == str(self.map)) and delta.seconds >= self.loop_time*2 else False

    def start(self)->None:
        """
        function to start a sync loop (you may want to pass this method as target of a process)
        """
        self.__sync_process()
