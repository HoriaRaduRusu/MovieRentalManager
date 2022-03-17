class IterableStructure:
    class Iterator:
        def __init__(self, collection):
            self.__collection = collection
            self.__poz = 0

        def __next__(self):
            if self.__poz == len(self.__collection.data):
                raise StopIteration()
            self.__poz += 1
            return self.__collection.data[self.__poz - 1]

    def __init__(self):
        self.__data = []

    @property
    def data(self):
        return self.__data

    def __iter__(self):
        return self.Iterator(self)

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __getitem__(self, item):
        return self.__data[item]

    def __delitem__(self, key):
        del self.__data[key]

    def __len__(self):
        return len(self.__data)

    def append(self, item):
        """
        Adds a new item to the end of the current list
        :param item: The item to be added to the list
        :return: nothing
        """
        self.__data.append(item)

    @staticmethod
    def sort(unordered_list, comparison_function):
        """
        Sorts an unordered list using comb sort based on a given function
        :param unordered_list: The list to be sorted
        :param comparison_function: The comparison function that takes two arguments and returns True if the first is
        supposed to be placed before the other in the list, otherwise False
        :return: nothing
        """
        shrink = 1.3
        gap = len(unordered_list)
        list_sorted = False
        while not list_sorted:
            gap = int(gap / shrink)
            if gap <= 1:
                list_sorted = True
                gap = 1
            for i in range(len(unordered_list) - gap):
                if comparison_function(unordered_list[i + gap], unordered_list[i]):
                    unordered_list[i + gap], unordered_list[i] = unordered_list[i], unordered_list[i + gap]
                    list_sorted = False

    @staticmethod
    def filter(unfiltered_list, acceptance_function):
        """
        Filters an unfiltered list using the given acceptance function
        :param unfiltered_list: The list to be filtered
        :param acceptance_function: The acceptance function that takes one argument and returns True if the argument
        respects the filtering condition, otherwise False
        :return: The filtered list
        """
        filtered_list = []
        for element in unfiltered_list:
            if acceptance_function(element):
                filtered_list.append(element)
        return filtered_list
