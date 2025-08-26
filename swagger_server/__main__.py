from swagger_server import create_app

def main():
    app = create_app()
    app.run(port=8080)


if __name__ == '__main__':
    main()
