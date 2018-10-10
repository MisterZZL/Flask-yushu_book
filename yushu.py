from app import creat_app

app = creat_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=app.config['DEBUG'], port=5000)  # =======>>>@web.route('/book/search/<q>/<page>')


