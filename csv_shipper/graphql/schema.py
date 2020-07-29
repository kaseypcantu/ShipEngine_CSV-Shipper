import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from csv_shipper.models import User, ShippingAddress


class User(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )


class ShippingAddress(SQLAlchemyObjectType):
    class Meta:
        model = ShippingAddress
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(User.connection)
    all_shipping_addresses = SQLAlchemyConnectionField(
            ShippingAddress.connection,
            sort=None
    )


schema = graphene.Schema(query=Query)
