from DriveAnalizer import DriveAnalyzer
from Drawer import Drawer


def main():
    worker = DriveAnalyzer()
    try:
        data = worker.get_files()
    except ValueError as e:
        print(e.args)
        return

    if data is None:
        print('No files found')
        return

    drawer = Drawer(data)
    drawer.run()


if __name__ == '__main__':
    main()
