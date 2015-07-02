from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class WifiForm(Form):
    ssid = StringField("SSID", validators = [DataRequired()])
    key = PasswordField("key", validators = [DataRequired()])
