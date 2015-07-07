from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class WifiForm(Form):
    ssid = StringField("SSID", validators = [DataRequired(), Length(min = 0, max = 32])
    key = PasswordField("key", validators = [DataRequired(), Length(min = 8, max = 63])
