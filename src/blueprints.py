from flask.blueprints import Blueprint

from views import IndexView


core = Blueprint('core', __name__)
core.add_url_rule('/', view_func=IndexView.as_view(name='index'), methods=('GET', 'POST'))
