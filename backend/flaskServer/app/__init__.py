import os
from flask import Flask



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #ROUTES
    #/api/user/ is the authentication route (and user interaction)
        #/api/user/getWallet is the route to get the user's wallet info
        #/api/user/sendTrade is the route to send a trade request (bid or ask market orders)
    #/api/stockData is the route to get info on stock tickers (relies on two APIs - SIX (pricing data) and Twelve(financial stements))

    @app.route('/api')
    def base_endpoint():
        return 'Default API endpoint'


    #DATABASE
    from . import db
    db.init_app(app)

    #BLUEPRINT (AUTH)
    from . import auth
    app.register_blueprint(auth.bp)

    #BLUEPRINT (STOCKDATA)
    from . import marketRoutes
    app.register_blueprint(marketRoutes.bp)

    #BLUEPRINT (PLAYGROUND)
    from . import playground
    app.register_blueprint(playground.bp)


    return app


app = create_app()