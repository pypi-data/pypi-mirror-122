
from house_model.house.common import (HouseLocation, HouseProperty,
                                      TransactionProperty)
from house_model.util.mongo_mixin import MongoMixin
from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (DateTimeField, DecimalField, DictField,
                                EmbeddedDocumentField, FloatField, IntField,
                                ListField, StringField, URLField)


class HousePrice(Document, MongoMixin):
    meta = {
        "strict": False,
        "indexes": [
            {"fields": ("platform", "platform_house_id"), "unique": True},
            ("estate_name", "area"),
            ("built_datetime"),
            ("location.city", "location.district")
        ]
    }

    platform = StringField(required=True)
    platform_house_id = StringField(required=True)
    platform_title = StringField(required=True)
    platform_description = StringField(required=True)
    total_price = DecimalField(required=True)
    unit_price = DecimalField(required=True)
    area = FloatField()
    estate_name = StringField()
    built_datetime = DateTimeField()
    images = ListField(StringField())
    scrape_datetime = DateTimeField()
    url = URLField()
    house_property = EmbeddedDocumentField(HouseProperty)
    transaction_property = EmbeddedDocumentField(TransactionProperty)
    location = EmbeddedDocumentField(HouseLocation)

    created_datetime = DateTimeField()
    updated_datetime = DateTimeField(required=True)

    @classmethod
    def bulk_update(cls, requests, ordered=True, bypass_document_validation=False, session=None):
        collection = cls._get_collection()
        collection.bulk_write(
            requests, ordered, bypass_document_validation, session)

    @classmethod
    def from_dict(cls, dict_data, created=False):
        return super()._from_son(dict_data, created=created)

    def to_dict(self):
        return self.to_dict_default("%Y-%m-%d %H:%M:%S")


class HousePriceHistory(Document, MongoMixin):
    meta = {
        "strict": False,
        "indexes": [
            {"fields": ("platform", "platform_house_id",
                        "snapshot_date"), "unique": True},
            ("calendar_year", "calendar_weeknumber", "calendar_weekday"),
            ("total_price"),
            ("unit_price")
        ]
    }

    platform = StringField(required=True)
    platform_house_id = StringField(required=True)
    snapshot_date = DateTimeField(required=True)
    calendar_year = IntField()
    calendar_weeknumber = IntField()
    calendar_weekday = IntField()
    total_price = FloatField(required=True)
    unit_price = FloatField(required=True)
    area = FloatField()
    estate_name = StringField()
    status = IntField()
    updated_datetime = DateTimeField(required=True)

    def to_dict(self):
        return self.to_dict_default("%Y-%m-%d %H:%M:%S")