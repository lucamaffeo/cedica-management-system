from src.core.database import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True , nullable=False)
    #permissions = db.relationship('Permission', backref='roles')

    def __repr__(self):
        return f"<Role {self.name}>"
