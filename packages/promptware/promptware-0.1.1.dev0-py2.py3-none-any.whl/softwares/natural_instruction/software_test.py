import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import NaturalInstructionPromptware  # noqa


class TestNaturalInstructionPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = NaturalInstructionPromptware(
            config_name="air_dialogue_sentence_generation"
        )
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute_default(self):
    #     software = NaturalInstructionPromptware(
    #         config_name="air_dialogue_sentence_generation"
    #     )
    #     input = {
    #         "definition": "In this task, you're given a dialogue between"
    #         " a customer and a flight booking agent with a gap"
    #         " in the conversation. Your job is to find the answer"
    #         " of the previous dialogue. Avoid using irrelevant"
    #         " extra information while creating the answer."
    #         " The answer should be relevant to the question"
    #         " before the blank. If you fill the blank with"
    #         " a question, it should have an answer from the agent"
    #         " in the given dialogue. Fill the gap marked"
    #         " with underline.",
    #         "inputs": "customer: Hello. \n agent: Hello, how may I"
    #         " help you today? \n customer: I am Rebecca Parker"
    #         " here. I want to travel from AUS to DCA. Can you"
    #         " please help me with booking a flight ticket? \n "
    #         "agent: Sure, please share me your planned journey "
    #         "dates? \n customer: My planned Journey  "
    #         "dates are from Apr 13 to Apr 15. \n agent: May I know your"
    #         " connection limit? \n customer: I need a connecting"
    #         " flight in between my journey. \n agent: Please wait"
    #         " for a moment. \n customer: Sure, I will wait."
    #         " \n __ \n customer: That's perfect, please proceed"
    #         " with that booking. \n agent: Shall I proceed with"
    #         " booking? Your flight ticket has been booked. \n "
    #         "customer: Thank you for helping me . \n agent: Thank"
    #         " you for visiting us, have a nice journey.",
    #         "targets": "agent: Thank you for waiting ,"
    #         "I found a connecting flight 1003 of airline Frontier,"
    #         " fare is 100 and class is economy.",
    #     }
    #     result = software.execute(input)
    #     print(result)
    #     self.assertGreater(len(result), 0)
