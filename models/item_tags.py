from db import db

class ItemTags(db.Model):
    __tablename__ = "items_tags"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")