#!/usr/bin/env python3

from swagger_server import create_app


def main():
    create_app().run(port=8080)


if __name__ == '__main__':
    main()
