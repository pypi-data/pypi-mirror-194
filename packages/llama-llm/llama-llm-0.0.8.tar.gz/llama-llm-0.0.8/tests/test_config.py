from llama import LLM, setup_config
import unittest

from llama.program.util.config import get_config


class TestConfig(unittest.TestCase):
    def test_config(self):
        llm = LLM(name="test_random", config={"production.key": "hiii"})
        config = get_config()

    def test_manual(self):
        setup_config({"production.key": "hiii"})
        config = get_config()
