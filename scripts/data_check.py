#!/usr/bin/python3
import argparse
import os


def main():
    for root, dirs, files in os.walk('data'):
        print(root)


if __name__ == '__main__':
    main()
