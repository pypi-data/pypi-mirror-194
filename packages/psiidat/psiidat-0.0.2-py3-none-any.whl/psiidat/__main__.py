# __main__.py

import sys

def main():
 
    if len(sys.argv) > 1:
        print('hello, '+str(sys.argv[1]))
    else:
       print('Hello, world!')


if __name__ == "__main__":
    main()