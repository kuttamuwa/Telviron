from marshmallow import Schema, fields


class User(Schema):
    user_id = fields.Int(required=True, attribute='user_id')  # 11001100

    user_label = fields.Str(required=True)  # Ali Gul
    user_name = fields.Str(required=True)  # @avaligul

    follower_count = fields.Int(required=False)  # 50
    following_count = fields.Int(required=False)  # 100

    def __str__(self):
        return f"{self.user_name} | {self.user_label} \n" \
               f"{self.user_id}"
