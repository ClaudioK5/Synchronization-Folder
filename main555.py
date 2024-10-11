from pathlib import Path
from datetime import datetime
import shutil
import hashlib
import time
import argparse


class FolderSynchronization:

    def __init__ (self, source_folder, replica_folder, log_folder, interval):

        self.source_folder = source_folder;
        self.replica_folder = replica_folder;
        self.log_folder = log_folder;
        self.interval = interval;
        
        Path(self.log_folder).mkdir(parents=True, exist_ok=True)
        
        self.log_file = Path(self.log_folder) / "sync_log.txt"

    
    #log_action will report every action will happen during the synchronization,
    #whether a file has been copied, deleted or updated.
    
    def log_action(self, message):
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.log_file, 'a') as f: f.write(f"{current_time}: {message}\n")
    

    #calculator of md5 associated to a file.
    
    def md5(self, fname):
        
        hash_md5 = hashlib.md5()
        
        with open(fname, "rb") as f:
            
            for chunk in iter(lambda: f.read(4096), b""):
                
                hash_md5.update(chunk)
                
            return hash_md5.hexdigest()

    
    #the method down below assures that if a file or directory is deleted inside the source folder, 
    #the same will happen inside the replica folder, assuring synchronization.
    
    def sync_delete_replica(self, source_folder = None, replica_folder = None):
        source_folder = Path(source_folder or self.source_folder)
        replica_folder = Path(replica_folder or self.replica_folder)
        
        for item in replica_folder.iterdir():
            
            corresponding_item = source_folder / item.name
            
            if not corresponding_item.exists():
                
                if item.is_file():
                    
                    item.unlink()
                    
                    self.log_action(f"File '{item.name}' has been deleted from {self.replica_folder}")
                    
                    print(f"File '{item.name}' has been deleted from {self.replica_folder}.")
                
                elif item.is_dir():
                    
                    shutil.rmtree(item)
                    
                    self.log_action(f"Directory '{item.name}' has been deleted from {self.replica_folder}")
                    
                    print(f"Directory '{item.name}' has been deleted from {self.replica_folder}.")
         
            elif corresponding_item.exists() and item.is_dir():
                
                self.sync_delete_replica(corresponding_item,item)
    
    #the method down below assures that if a file or a directory assures
    #that if a file or a directory is added in the source folder, it will be copied in the
    #replica folder, assuring synchronization.
    
    def sync_add_replica(self, source_folder = None, replica_folder = None):
        
        source_folder = Path(source_folder or self.source_folder)
        replica_folder = Path(replica_folder or self.replica_folder)
        
        for item in source_folder.iterdir():
            
            corresponding_item = replica_folder / item.name
            
            if not corresponding_item.exists():
                
                if item.is_file():
                    
                    shutil.copy2(item, corresponding_item)
                    self.log_action(f"File '{item.name}' has been copied from {self.source_folder} to {self.replica_folder}.")
                    print(f"File '{item.name}' has been copied from {self.source_folder} to {self.replica_folder}")
                
                elif item.is_dir():
                    
                    #shutil.copytree(item, corresponding_item)
                    corresponding_item.mkdir(parents=True, exist_ok=True)
                    self.log_action(f"Directory '{item.name}' has been copied from {self.source_folder} to {self.replica_folder}")
                    print(f"Directory '{item.name}' has been copied from {self.source_folder} to {self.replica_folder}")
                    self.sync_add_replica(item,corresponding_item)
            
            
            elif corresponding_item.exists() and item.is_dir():
                
                self.sync_add_replica(item,corresponding_item)


    #the method below synchronizes the two folder assuring an updated file
    #in the src folder will be updated in the replica folder as well, assuring synchronization.

    def sync_update_replica(self, source_folder = None, replica_folder = None):
        
        source_folder = Path(source_folder or self.source_folder)
        replica_folder = Path(replica_folder or self.replica_folder)
        
        for item in source_folder.iterdir():
            
            corresponding_item = replica_folder / item.name
            
            if item.is_file():
                
                if self.md5(item) != self.md5(corresponding_item):
                    
                    shutil.copy2(item,corresponding_item)
                    self.log_action(f"File '{item.name}' has been updated in {self.replica_folder}.")
                    print(f"File '{item.name}' has been updated in {self.replica_folder}.")
             
            elif item.is_dir():
                
                self.sync_update_replica(item,corresponding_item)



    def sync(self):


        self.sync_add_replica()
        self.sync_delete_replica()
        self.sync_update_replica()
        

    def run(self):

        while True:

            self.sync()
            time.sleep(self.interval)

def parse_arguments():

    parser = argparse.ArgumentParser(description = "Folder Synchronization Tool")

    parser.add_argument("source_folder", type = str, help = "Path to the source folder")

    parser.add_argument("replica_folder", type = str, help = "Path to the replica folder")

    parser.add_argument("log_folder", type = str, help = "Path to the log folder")

    parser.add_argument("interval", type = int, help = "Synchronization interval in seconds")

    return parser.parse_args()


if __name__ == "__main__":
    
    args = parse_arguments()

    synchronization = FolderSynchronization(args.source_folder, args.replica_folder, args.log_folder, args.interval)

    synchronization.run()
    
               
