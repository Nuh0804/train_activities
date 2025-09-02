import graphene
from tanrail_service.views import Mutation
from tanrail_service.schema import AllQuery
from tanrail_accounts.schema import Query as AccountsQuery
from tanrail_accounts.views import Mutation as AccountsMutation
from tanrail_uaa.schema import Query as UaaQuery
from tanrail_uaa.views import Mutation as UaaMutation

class Query(AllQuery, AccountsQuery, UaaQuery, graphene.ObjectType):
    pass

class Mutation(Mutation, AccountsMutation, UaaMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)