import os
import unittest

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    suite = unittest.TestLoader().discover('.', pattern="*_test.py")
    tests = unittest.TextTestRunner()
    tests.run(suite)
