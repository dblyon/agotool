"""Define some fixtures to use in the project."""
import sys, os

if __name__ == "__main__":
    print(os.path.join("../../..", os.path.dirname(os.path.abspath(os.path.realpath(__file__)))))
    print(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")))
