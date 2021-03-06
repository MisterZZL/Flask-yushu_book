from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少输入两个字符，最多10个字符')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该电子邮箱已经被注册')


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])


class LoginForm(EmailForm):
    password = PasswordField(validators=[DataRequired(message='密码不能为空，请输入你的密码'),
                                         Length(6, 32)])


class ResetPasswordForm(Form):
    password1 = PasswordField(
        validators=[DataRequired(message='密码不能为空'),
                    Length(6, 32, message='密码长度至少为6到32个字符之间'),
                    EqualTo('password2', message='两次输入的密码不相同')])

    password2 = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired()])
    new_password1 = PasswordField(validators=[
        DataRequired(message='密码不能为空'),
        Length(6, 32, message='密码长度至少为6到32个字符之间'),
        EqualTo('new_password2', message='两次输入的密码不相同')])

    new_password2 = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])
