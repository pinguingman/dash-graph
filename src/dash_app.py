import dash

from callbacks import register_callbacks
from database import engine, Base
from layout import init_layout


def create_app():
    app = dash.Dash(__name__)

    Base.metadata.create_all(bind=engine)

    init_layout(app)
    register_callbacks()

    return app


app = create_app()
app_server = app.server
