import unittest
from Controllers.HomeMediatingController import HomeMediatingController


from langchain.schema import HumanMessage
from Workflow import APP
from States import *
from ToolKit import Tools
from AppCoordinator import *
import timeit
'''

    app = APP
    state: State = {"messages": []}
    tools = Tools()
    backend = AppCoordinator(APP=app, state=state, tools=tools)
    controller = HomeMediatingController(backend=backend)


'''
# TODO: We're going to have to alter this whole code base, to get tests working cleanly.

class HomeMediatingControllerTests(unittest.TestCase):
    def setUp(self):
        self.APP = APP
        self.state = {"messages": []}
        self.tools = Tools(), 
        self.mock_backend = AppCoordinator(APP=self.APP, state=self.state, tools=self.tools)
        self.controller = HomeMediatingController(backend=self.mock_backend)

    def test_process_text_input_valid(self):
        sut = self.controller.process_text_input("Hello!")
        self.assertIsInstance(sut, str)
        self.assertNotEqual(sut, "")  # Ensure the result is not empty

    
    # def test_process_text_input_invalid(self):
    #     """
    #     Test process_text_input with invalid input (e.g., empty string).
    #     """
    #     result = self.controller.process_text_input("")
    #     self.assertEqual(result, "Error: Invalid input")  # Replace with expected error message

    # def test_process_audio_input_valid(self):
    #     """
    #     Test process_audio_input with a valid file path.
    #     """
    #     valid_file_path = "/path/to/audio/file.wav"  # Replace with a valid test file path
    #     result = self.controller.process_audio_input(valid_file_path)
    #     self.assertIsInstance(result, str)
    #     self.assertNotEqual(result, "")  # Ensure the result is not empty

    # def test_process_audio_input_invalid(self):
    #     """
    #     Test process_audio_input with an invalid file path.
    #     """
    #     invalid_file_path = "/invalid/path/to/audio/file.wav"
    #     result = self.controller.process_audio_input(invalid_file_path)
    #     self.assertEqual(result, "Error: No valid audio file provided")  # Replace with expected error message

if __name__ == "__main__":
    print("😀 ******************** Welcome to HomeMediatingController | Tests Running ********************")
    unittest.main()

    a = '''page, number = 3, 5'''
    b = """page = 3
    number = 5
    """

    b = '''
page = 3
number = 5

'''
    # why is this not creating an object?
    testA = timeit.timeit(stmt=a, number = 100000)
    testB = timeit.timeit(stmt=b, number = 100000)

    print(testA)
    print(testB)
    testA = float(round(testA,10))
    testB = float(round(testB,10))
    print("TEST RESULTS")
    # Calculate percentage difference
    if testA < testB:
        percentage = ((testB - testA) / testB) * 100
        print(f"testA was {percentage:.2f}% faster than testB")
    elif testB < testA:
        percentage = ((testA - testB) / testA) * 100
        print(f"testB was {percentage:.2f}% faster than testA")
    else:
        print("testA and testB had the same execution time")

    # Print the raw results for reference
    print("Execution time for testA:", testA*1000)
    print("Execution time for testB:", testB*1000)
