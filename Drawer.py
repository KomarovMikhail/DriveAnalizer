import matplotlib.pyplot as plt


class Drawer:
    def __init__(self, data):
        self._data = data
        self._size = len(data)

    def _draw_common_data(self):
        labels = [item + '(' + str(self._data[item]['totalSize']) + ' Кб)' for item in self._data.keys()]
        x = [item['totalSize'] for item in self._data.values()]

        plt.figure(figsize=(14, 7 * (self._size / 2 + 1)))
        plt.subplot(self._size / 2 + 1, 2, 1)
        plt.pie(x=x, labels=labels)
        plt.title('Распределение памяти по типам файлов')
        plt.legend()

    def _draw_each_format(self):
        count = 2
        for key in self._data.keys():
            x = [item['size'] for item in self._data[key]['objects']]
            labels = [item['name'] + '(' + str(item['size']) + ' Кб)' for item in self._data[key]['objects']]
            plt.subplot(self._size / 2 + 1, 2, count)
            plt.pie(x=x, labels=labels)
            plt.title('Распределение для формата ' + key)
            plt.legend()
            count += 1

    def run(self):
        self._draw_common_data()
        self._draw_each_format()
        plt.show()

