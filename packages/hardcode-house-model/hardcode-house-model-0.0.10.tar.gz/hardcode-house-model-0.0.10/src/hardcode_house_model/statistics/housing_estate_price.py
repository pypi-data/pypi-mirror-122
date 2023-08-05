from enum import Enum

from hardcode_house_model.house.common import HouseLocation, HouseQuotation
from hardcode_house_model.util.mongo_mixin import MongoMixin
from mongoengine import Document
from mongoengine.fields import (DateTimeField, DecimalField, DictField,
                                EmbeddedDocumentField, FloatField, IntField,
                                ListField, StringField, URLField)


class HouseEstateWeeklyReport(Document, MongoMixin):
    meta = {
        "strict": False,
        "indexes": [
            {"fields": ("city", "platform", "week_begin_date"), "unique": True},
        ]
    }

    city = StringField()
    platform = StringField(required=True)
    week_begin_date = DateTimeField()
    mean_price = DecimalField()
    price_percentile25 = DecimalField()
    price_percentile50 = DecimalField()
    price_percentile75 = DecimalField()
    price_percentile80 = DecimalField()
    price_percentile90 = DecimalField()
    price_percentile95 = DecimalField()
    house_count = IntField()
    price_increase_count = IntField()
    price_decrease_count = IntField()
    newlisting_count = IntField()
    delisting_count = IntField()
    unchanged_count = IntField()
    updated_datetime = DateTimeField()

class HouseEstateWeeklyPrice(Document, MongoMixin):
    meta = {
        "strict": False,
        "indexes": [
            {"fields": ("platform", "estate_name", "week_begin_date", "location.city", "location.district"), "unique": True},
            {"fields": ("report_id", "estate_name"), "unique": True}
            ("week_begin_date", "mean_price")
        ]
    }

    report_id = StringField(required=True)
    platform = StringField(required=True)
    estate_name = StringField()
    location = EmbeddedDocumentField(HouseLocation)
    week_begin_date = DateTimeField()
    mean_price = DecimalField()
    price_percentile25 = DecimalField()
    price_percentile50 = DecimalField()
    price_percentile75 = DecimalField()
    price_percentile80 = DecimalField()
    price_percentile90 = DecimalField()
    price_percentile95 = DecimalField()
    house_count = IntField()
    price_increase_count = IntField()
    price_decrease_count = IntField()
    newlisting_count = IntField()
    delisting_count = IntField()
    unchanged_count = IntField()
    updated_datetime = DateTimeField()


class HouseEstateWeeklyPriceChange(Document, MongoMixin):
    meta = {
        "strict": False,
        "indexes": [
            {"fields": ("platform_house_id", "week_begin_date", "location.city", "location.district"), "unique": True},
            {"fields": ("report_id", "platform_house_id"), "unique": True},
            ("location.city", "location.district", "week_begin_date"),
            ("direction", "delta.total_price"),
            ("direction", "delta.unit_price")
        ]
    }

    class ChangeDirection(Enum):
        Increase = 1
        Decrease = 2
        Newlisting = 3
        Delisting = 4

    report_id = StringField(required=True)
    estate_name = StringField()
    location = EmbeddedDocumentField(HouseLocation)
    week_begin_date = DateTimeField()
    platform = StringField()
    platform_house_id = StringField()
    last_week_snapshot_date = DateTimeField()
    last_week_quotation = EmbeddedDocumentField(HouseQuotation)
    current_week_snapshot_date = DateTimeField()
    current_week_quotation = EmbeddedDocumentField(HouseQuotation)
    direction = IntField()
    delta = EmbeddedDocumentField(HouseQuotation)
    updated_datetime = DateTimeField()


class HouseEstateMonthlyPrice(Document, MongoMixin):
    meta = {
        "strict": False,
        "indexes": [
            {"fields": ("estate_name", "month_begin_date", "location.city", "location.district"), "unique": True},
            ("location.city", "location.district", "month_begin_date"),
            ("month_begin_date", "mean_price")
        ]
    }

    platform = StringField(required=True)
    estate_name = StringField()
    location = EmbeddedDocumentField(HouseLocation)
    month_begin_date = DateTimeField()
    mean_price = DecimalField()
    price_percentile25 = DecimalField()
    price_percentile50 = DecimalField()
    price_percentile75 = DecimalField()
    price_percentile80 = DecimalField()
    price_percentile90 = DecimalField()
    price_percentile95 = DecimalField()
    house_count = IntField()
    updated_datetime = DateTimeField()


class HouseEstateMonthlyPriceChange(Document, MongoMixin):
    meta = {
        "strict": False,
        "indexes": [
            {"fields": ("platform_house_id", "month_begin_date", "location.city", "location.district"), "unique": True},
            ("location.city", "location.district", "month_begin_date"),
            ("direction", "delta.total_price"),
            ("direction", "delta.unit_price")
        ]
    }

    class ChangeDirection(Enum):
        Increase = 1
        Decrease = 2

    estate_name = StringField()
    location = EmbeddedDocumentField(HouseLocation)
    month_begin_date = DateTimeField()
    platform = StringField(required=True)
    platform_house_id = StringField(required=True)
    last_month_snapshot_date = DateTimeField(required=True)
    last_month_quotation = EmbeddedDocumentField(HouseQuotation)
    current_month_snapshot_date = DateTimeField(required=True)
    current_month_quotation = EmbeddedDocumentField(HouseQuotation)
    direction = IntField()
    delta = EmbeddedDocumentField(HouseQuotation)
    updated_datetime = DateTimeField()
