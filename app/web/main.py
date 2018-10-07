from . import web


@web.route('/')
def index():
    return 'index'


@web.route('/personal')
def personal_center():
    pass
