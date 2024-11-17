#import unittest
#from utils.utility import fetch_from_llama

#class TestUtilities(unittest.TestCase):
 #   def test_fetch_from_llama_success(self):
  #      prompt = "Suggest technical skills for a Data Scientist"
   #     result = fetch_from_llama(prompt)
    #    self.assertIsInstance(result, list)

#    def test_fetch_from_llama_error(self):
 #       # Simulate incorrect API call
  #      result = fetch_from_llama("", model="non-existent-model")
   #     self.assertIn("Error:", result[0])

#if __name__ == "__main__":
 #   unittest.main()

#RunTestWith: python -m unittest discover tests/
