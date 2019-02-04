class ExpectationQueue:
    def __init__(self):
        self.__queue = []

    def push(self, expectation):
        self.__queue.append(expectation)

    def pop(self):
        if self.get_size() > 0:
            return_value = self.__queue[0]
            del self.__queue[0]
            return return_value
        else:
            return None

    def get_size(self):
        return len(self.__queue)

    def get_next_element(self):
        if self.get_size() > 0:
            return self.__queue[0]
        else:
            return None


if __name__ == "__main__":
    test_queue = ExpectationQueue()
    print(test_queue.get_next_element())
    test_queue.push("first_pushed")
    print(test_queue.get_next_element())
    test_queue.push("second_pushed")
    print(test_queue.get_next_element())
    test_queue.pop()
    print(test_queue.get_next_element())
    test_queue.push("third_pushed")
    print(test_queue.get_next_element())
    test_queue.pop()
    print(test_queue.get_next_element())
    test_queue.pop()
    print(test_queue.get_next_element())
    test_queue.pop()
    print(test_queue.get_next_element())
