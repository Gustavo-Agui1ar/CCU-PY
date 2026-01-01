import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, BASE_DIR)

from utils.cripto_utils import CriptoUtils

class CryptoLibrary:
    def decrypt(self, value):
        return CriptoUtils.decrypt(value)

    def encrypt(self, value):
        return CriptoUtils.encrypt(value)
