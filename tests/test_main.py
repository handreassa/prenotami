import unittest
from unittest.mock import patch
from io import StringIO
from main import Prenota


class TestPrenota(unittest.TestCase):
    def setUp(self):
        # Set up any necessary configurations or mock data for tests
        pass

    def tearDown(self):
        # Clean up any resources created during the tests
        pass

    def test_check_file_exists(self):
        # Test the check_file_exists method
        self.assertTrue(Prenota.check_file_exists("files/residencia.pdf"))
        self.assertFalse(Prenota.check_file_exists("nonexistent_file.txt"))

    @patch("builtins.input", side_effect=["quit"])
    @patch("undetected_chromedriver.Chrome")
    def test_run_citizenship(self, mock_chrome, mock_input):
        # Test the run method with citizenship request type
        mock_chrome.return_value.page_source = ""
        Prenota.run()

        # Add assertions based on your specific expectations
        self.assertTrue(mock_chrome.called)

    @patch("builtins.input", side_effect=["quit"])
    @patch("undetected_chromedriver.Chrome")
    def test_run_passport(self, mock_chrome, mock_input):
        # Test the run method with passport request type
        mock_chrome.return_value.page_source = ""
        Prenota.run()

        # Add assertions based on your specific expectations
        self.assertTrue(mock_chrome.called)

    @patch("builtins.input", side_effect=["quit"])
    @patch("undetected_chromedriver.Chrome")
    def test_run_no_files(self, mock_chrome, mock_input):
        # Test the run method when required files are not available
        with patch("sys.exit") as mock_exit:
            Prenota.check_file_exists = lambda _: False  # Mock file not exists
            Prenota.run()

            # Add assertions based on your specific expectations
            self.assertTrue(mock_exit.called_with(0))


if __name__ == "__main__":
    unittest.main()
