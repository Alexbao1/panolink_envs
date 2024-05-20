from traceutils2.ixps.peeringdb_base import AbstractPeeringDB
from traceutils2.ixps import peeringdb, peeringdb_v1
from traceutils2.ixps.peeringdb import PeeringDB
from traceutils2.ixps.caida import CaidaIXPs


def create_peeringdb(filename):
    if filename.endswith('.json'):
        return peeringdb.PeeringDB(filename)
    try:
        return peeringdb.PeeringDB(filename)
    except:
        return peeringdb_v1.PeeringDB(filename)
