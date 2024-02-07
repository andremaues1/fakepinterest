#Cria formularios do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from FakePinterest.models import Usuario
from FakePinterest import bcrypt



class FormLogin(FlaskForm):
    email = StringField("E-mail",validators=[DataRequired(),Email()])
    senha = PasswordField("Senha",validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer login")

    def validate_email(self,email):
        usuario1 = Usuario()
        usuario = usuario1.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("Email não encontrado, crie uma conta para continuar.")

    def validate_senha(self,senha):
        usuario1 = Usuario()
        checar = bcrypt.generate_password_hash(senha.data)
        usuario = usuario1.query.filter_by(senha=checar).first()

        if not usuario:
            raise ValidationError("Senha não encontrada, crie uma conta para continuar.")




class FormCriarConta(FlaskForm):
    email = StringField("E-mail",validators=[DataRequired(),Email()])
    username = StringField("Nome do usuário",validators=[DataRequired()])
    senha = PasswordField("Senha",validators=[DataRequired(),Length(6,20)])
    repetir_senha = PasswordField("Repetir senha",validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao =SubmitField("Confirmar senha")



    def validate_email(self,email):
        usuario1 = Usuario()
        usuario = usuario1.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError("Email já cadastrado, faça login para continuar") # o raise faz o erro subir para o formulario

    def validate_username(self,username):
        usuario1 = Usuario()
        usuario = usuario1.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError("O nome de usuário já existe.")




class FormFoto(FlaskForm):
    foto = FileField("Foto",validators=[DataRequired()])
    botao_confirmacao =SubmitField("Enviar")
