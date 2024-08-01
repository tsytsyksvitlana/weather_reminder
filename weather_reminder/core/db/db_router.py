import typing as t

from django.db.models import Model


class AdministratorRouter:
    route_app_labels = {"administrator"}
    administrator_db = "administrator_db"

    def db_for_read(
        self, model: t.Type[Model], **hints: t.Any
    ) -> t.Optional[str]:
        if model._meta.app_label in self.route_app_labels:
            return self.administrator_db
        return None

    def db_for_write(
        self, model: t.Type[Model], **hints: t.Any
    ) -> t.Optional[str]:
        if model._meta.app_label in self.route_app_labels:
            return self.administrator_db
        return None

    def allow_relation(
        self, obj1: Model, obj2: Model, **hints: t.Any
    ) -> t.Optional[bool]:
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(
        self,
        db: str,
        app_label: str,
        model_name: t.Optional[str] = None,
        **hints: t.Any,
    ) -> t.Optional[bool]:
        if app_label in self.route_app_labels:
            return db == self.administrator_db
        return None
