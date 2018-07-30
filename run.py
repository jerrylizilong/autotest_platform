#!flask/bin/python
from app import app
def main():
    app.run(host='0.0.0.0',port=5000,debug=True)
main()


