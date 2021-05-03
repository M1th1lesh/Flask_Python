

from App import create_app
#importing from our App folder  from it using __init__.py ka create_app function

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)