import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

metadata = db.MetaData()

"""usage = db.Table(
    "usage",
    metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("usage_ident", db.String),
    db.Column("traffic", db.Integer),
    db.Column("last_int", db.DateTime),
)
"""

class Usage(base):
    __tablename__ = "usage"

    id = db.Column(db.Integer, primary_key=True)
    usage_ident = db.Column(db.String)
    traffic = db.Column(db.Integer)
    last_int = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Usage(usage_ident={self.usage_ident}, traffic={self.traffic}, last_int={self.last_int})>"