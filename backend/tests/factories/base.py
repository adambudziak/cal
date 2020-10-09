import factory


class PeeweeModelFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        instance = super().create(**kwargs)
        instance.save()
        return instance
