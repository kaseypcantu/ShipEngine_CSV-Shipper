import os
import logging

from flask_graphql import GraphQLView
from csv_shipper.graphql.schema import schema, User, ShippingAddress

from csv_shipper import create_app, load_dotenv, db

load_dotenv()

app = create_app()

if __name__ == "__main__":
    log: logging.Logger = app.logger
    log.setLevel(logging.DEBUG)
    db.create_all()
    app.add_url_rule(
            '/graphql',
            view_func=GraphQLView.as_view(
                    'graphql',
                    schema=schema,
                    graphiql=True
            )
    )
    app.run(host="127.0.0.1", port=os.getenv("APP_PORT"), debug=True)
