__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"


class ExpectationQueue:
    def __init__(self):
        """Simple queue to represent a series of expected API requests and their responsesfor the tests."""
        self.__queue = []

    def push(self, expectation):
        """
        Adds a new element to the end of the expectation queue.

        :param expectation: the encapsulated expectation, containing the expected API request and the response to it.
        :type expectation: Expectation

        :return: None
        """

        self.__queue.append(expectation)

    def pop(self):
        """
        Returns the next element in the queue and deletes it from the queue.

        Returns None if the queue is empty.

        :return: the first element in the queue.
        :trype: Expectation
        """

        if self.get_size() > 0:
            return_value = self.__queue[0]
            del self.__queue[0]
            return return_value
        else:
            return None

    def get_size(self):
        """
        Returns the length of the expectation queue.

        :return: length of the queue (number of expected expectations.
        :trype: int
        """

        return len(self.__queue)

    def get_next_element(self):
        """
        Returns the next element in the queue without altering the queue itself.

        Returns None if the queue is empty.

        :return: the first element in the queue.
        :trype: Expectation
        """

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
