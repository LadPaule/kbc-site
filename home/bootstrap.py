class CommonLayout(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(
            MultiField("User data",
                'username',
                'lastname',
                'age'
            )
        )