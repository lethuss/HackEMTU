import os
import zipfile


paths = [os.path.join(dp, f)
         for dp, dn, fn in os.walk(os.path.expanduser("2017"))
            for f in fn]
clean_paths = [path for path in paths if r'.zip' in paths]
for file in clean_paths:
    try:
        zip_file = zipfile.ZipFile(file)
        zip_file.extractall(file)
        zip_file.close()
    except:
        pass
