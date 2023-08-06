from sys import argv

from yaml2xbel import convert


if __name__ == '__main__':
    with open('output.xbel', 'w') as output:
        output.write(convert(argv[1]))
