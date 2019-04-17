import os


def delete_content(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


if __name__== '__main__':
    delete_content('tmp/rules/')
    delete_content('tmp/stls/')
    delete_content('tmp/scads/')