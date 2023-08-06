from .permission_manager import PermissionManager

import os
from . import config 


SYSTEMD_SYSTEM_DIR = r"/etc/systemd/system"

ADD_OTHERS_WRITE_PERMISSIONS = "o+w"
REMOVE_OTHERS_WRITE_PERMISSIONS = "o-w"
class FileManager:
    """Class contains methods to manage files in the /etc/systemd/system directory"""


    def __init__(self, filename: str, overwrite=False):
        self.logger = config.get_logger(__name__)
        self.logger.info("create instance of FileManager")

        self.filename = filename
        self.overwrite = overwrite
        self.permission_manager: PermissionManager = PermissionManager()

    @property
    def file_full_path(self):
        return f"{SYSTEMD_SYSTEM_DIR}/{self.filename}"

    def _save_origin_systemd_writable_permission(self):
        """save the origin directory permissions in origin_directory_permission"""
        if os.access(SYSTEMD_SYSTEM_DIR, os.W_OK):
            self.origin_systemd_writable_permission = ADD_OTHERS_WRITE_PERMISSIONS
        else:
            self.origin_systemd_writable_permission = (
                REMOVE_OTHERS_WRITE_PERMISSIONS
            )

    def create_file(self, content):
        """Create a file at /etc/systemd/system/ and add write permission to it

        Args:
            filename (string): filename with extension
            content (string): what to write at /etc/systemd/system/$filename
        """

        self.check_permissions()

        self._save_origin_systemd_writable_permission()

        # add write permission to /etc/systemd/system
        self.logger.debug(
            f"change permission to writable of {SYSTEMD_SYSTEM_DIR} "
        )
        self.permission_manager.change_path_permissions(
            SYSTEMD_SYSTEM_DIR, ADD_OTHERS_WRITE_PERMISSIONS
        )
        self.logger.debug(
            f"changed permission to writable of {SYSTEMD_SYSTEM_DIR} "
        )

        # create the file
        with open(f"{self.file_full_path}", "w") as service_file:
            service_file.write(content)
            self.logger.debug("create and fill file")
            # change permission of file to writable
            self.permission_manager.change_path_permissions(self.file_full_path, "o+w")

        # change /etc/systemd/system permission to it's origin
        self.logger.debug(f"change permission back of {SYSTEMD_SYSTEM_DIR}")
        self.permission_manager.change_path_permissions(
            SYSTEMD_SYSTEM_DIR, self.origin_systemd_writable_permission
        )
        self.logger.info(f"created {self.file_full_path} successfully")

    def is_file_exist(self):
        if os.path.exists(f"{SYSTEMD_SYSTEM_DIR}/{self.filename}"):
            return True
        else:
            return False

    def check_permissions(self):
        if self.is_file_exist():
            if not self.permission_manager.is_writable(self.file_full_path):
                self.logger.error(
                    f"{self.filename} is a system file. try another service name or title"
                )
                raise PermissionError(
                    f"{self.filename} is a system file. try another service name or title"
                )
            else:
                if not self.overwrite:
                    self.logger.error(
                        f"you can't overwrite {self.filename}. try another filename, or set overwrite to True"
                    )
                    raise FileExistsError(
                        f"You can't overwrite {self.filename}. Already existed. If you want to, you can set overwrite to True."
                    )


if __name__ == "__main__":
    file_manager = FileManager("ztest.txt")
    file_manager.create_file("hello world")
