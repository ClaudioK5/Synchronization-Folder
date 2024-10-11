# Synchronization-Folder

The script allows one-way synchronization between Source folder and the replica folder as required. It ensures that every action (File creation/copying/removal) is mirrored in the replica folder. It uses
only built-in Python libraries in order to run effectively. Every action is logged inside the log folder and into the console in order to ensure clarity.


## How to run
Command prompt should be opened in order to navigate to the folder where the script is stored, in order to run the following command:
python main.py "path_to_source_folder" "path_to_replica_folder" "path_to_log_folder" "interval" 
