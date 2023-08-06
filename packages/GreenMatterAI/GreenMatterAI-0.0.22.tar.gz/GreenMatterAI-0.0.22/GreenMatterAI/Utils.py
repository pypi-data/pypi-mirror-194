import pathlib
import matplotlib.pyplot as plt
import math

class Utils:
    def __init__(self, s3_client, bucket, s3_folder):
        self._s3_client = s3_client
        self._bucket = bucket
        self._s3_folder = s3_folder

    def display_images_in_grid(self, imgs_to_display, imgs_in_row):
        imgs_to_display = list(map(lambda x: plt.imread(x), imgs_to_display))
        rows = math.ceil(len(imgs_to_display) / imgs_in_row)
        columns = min(imgs_in_row, len(imgs_to_display))

        fig, axes = plt.subplots(rows, columns, sharex=True, sharey=True, figsize=(5 * columns, 5 * rows))
        fig.subplots_adjust(wspace=0, hspace=0)

        for img, ax in zip(imgs_to_display, axes.flat):
            ax.imshow(img)
            ax.axis('off')

        for ax in axes.flat[len(imgs_to_display):len(axes.flat)]:
            fig.delaxes(ax)
        plt.show()

    def upload_file_to_s3(self, local_file_path, folder, file_path_on_s3=None):
        if file_path_on_s3 is None:
            file_name = pathlib.PurePath(local_file_path).name
        else:
            file_name = file_path_on_s3

        #s3_folder_path = self._s3_folder + '/' + folder
        s3_folder_path = folder
        s3_path = s3_folder_path + file_name
        print(f"Uploading {file_name}")
        self._s3_client.upload_file(local_file_path, self._bucket, s3_path)

        return self._bucket, s3_folder_path, file_name

    def upload_folder_to_s3(self, local_folder_path, folder):
        path = pathlib.Path(local_folder_path)
        files_to_upload = [item for item in path.rglob("*") if not item.is_dir()]
        for file in files_to_upload:
            relative_file_path = str(file.relative_to(path.parent).as_posix())
            self.upload_file_to_s3(str(file), folder, relative_file_path)
