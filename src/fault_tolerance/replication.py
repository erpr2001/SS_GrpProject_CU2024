import shutil
import os

def replicate_data(src_file: str, dest_dir: str) -> None:
    """
    Replicates the source data file to the destination directory for redundancy.
    """
    try:
        shutil.copy(src_file, dest_dir)
        print(f"Replication successful: {src_file} -> {dest_dir}")
    except Exception as e:
        print(f"Error replicating data: {e}")
