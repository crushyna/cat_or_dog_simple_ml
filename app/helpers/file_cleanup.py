import os, time, sys


class FileCleanup:

    @staticmethod
    def file_cleanup(path: str) -> bool:
        """
        Deletes temporary files in upload folder.
        :param path: str
        :return: bool
        """
        now = time.time()
        try:
            for file in os.listdir(path):
                if os.stat(os.path.join(path, file)).st_mtime < now - 15 * 60:
                    if os.path.isfile(os.path.join(path, file)):
                        os.remove(os.path.join(path, file))

            return True

        except Exception:
            return False
