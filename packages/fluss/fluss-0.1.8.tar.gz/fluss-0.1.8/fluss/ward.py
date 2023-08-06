
from herre.wards.query import TypedQuery
from herre.access.object import GraphQLObject
from herre.herre import get_current_herre
from herre.wards.graphql import GraphQLWardConfig, ParsedQuery, GraphQLWard


class FlussConfig(GraphQLWardConfig):
    _group = "fluss"
    host: str
    port: int
    secure: bool

    class Config:
       group = "fluss"



class FlussWard(GraphQLWard):
    configClass: FlussConfig

    class Meta:
        key = "fluss"



async def open_playground():
    raise NotImplementedError("SSS")







class gql(TypedQuery):
    ward_key = "fluss"
    


