from ..extensions import db

class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(200), nullable=False, index=True)

    def __repr__(self):
        return f"<TokenBlocklist jti={self.jti}>"
