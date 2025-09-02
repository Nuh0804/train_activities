import graphene
from tanrail_service.views import Mutation
from tanrail_service.schema import AllQuery

class Query(AllQuery, graphene.ObjectType):
    pass

class Mutation(Mutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)