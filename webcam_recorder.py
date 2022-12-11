import os


class WebcamRecorder:
    def __init__(self, users):
        self.users = users

        module_dir = os.path.dirname(__file__)
        self.download_dir = module_dir + "/downloads"

        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        executable_file = os.path.join(module_dir, "sc_recorder")
        os.system(f"chmod +x {executable_file}")

        os.system(f"{executable_file} settings download-dir {self.download_dir}")

        for user in users:
            os.system(f"{executable_file} add stripchat {user} --autodownload")

        os.system(f"{executable_file} download &")

    def get_files(self):
        files = []

        for file_name in os.listdir(self.download_dir):
            if os.path.isfile(os.path.join(self.download_dir, file_name)):
                files.append({
                    "name": file_name,
                    "path": os.path.join(self.download_dir, file_name),
                    "dir": self.download_dir,
                    "size": os.path.getsize(os.path.join(self.download_dir, file_name))
                })

        return files

    def get_users(self):
        return self.users

    @staticmethod
    def delete_file(path):
        if os.path.exists(path):
            os.remove(path)

            if not os.path.exists(path):
                print("delete success")
            else:
                print("delete fail")
        else:
            print(f"File {path} doesn't exists.")
