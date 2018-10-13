from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, ValidationError

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少输入两个字符，最多10个字符')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该电子邮箱已经被注册')


class ForgetForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])


class LoginForm(ForgetForm):
    password = PasswordField(validators=[DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32)])
