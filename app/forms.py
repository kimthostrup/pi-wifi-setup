from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class WifiForm(Form):
    ssid = StringField("SSID", validators = [DataRequired()])
    key = StringField("key", validators = [DataRequired()])
