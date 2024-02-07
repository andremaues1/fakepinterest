#Cria rotas do site
from flask import  render_template, url_for, redirect
from FakePinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from FakePinterest.templates.forms import FormLogin, FormCriarConta, FormFoto
from FakePinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename

@app.route("/",methods=["GET","POST"]) # isso serve pra dizer se é homepage ou um caminho dentro da homepage

def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha,formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html",form=formlogin) # O nome do diretório dos arquivos html sempre deve se chamar templates

@app.route("/criar-conta",methods=["GET","POST"])
def criar_conta():
    formcriarconta = FormCriarConta()

    if formcriarconta.validate_on_submit(): # validate_on_submite serve pra quando clicar no botão

        senha = bcrypt.generate_password_hash(
            formcriarconta.senha.data,10)  # aplica criptografia na senha e assim se o hacker tiver acesso ao banco de dados ele não roubará a senha, mas só a criptografia
        usuario = Usuario(username=formcriarconta.username.data,senha=senha,email=formcriarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario,remember=True)# remember serve pra gravar a o login do usuario armazenando nos cookies do navegador
        return redirect(url_for("perfil",id_usuario=usuario.id))
    return render_template("criar_conta.html",form=formcriarconta)




@app.route("/perfil/<id_usuario>",methods=["GET","POST"]) # <usuario> é qualquer coisa que voce escreva na url
@login_required
def perfil(id_usuario): # usuario é a variavel da url
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():  # validate_on_submite serve pra quando clicar no botão
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo dentro da pasta certa
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/fotos_posts",nome_seguro)
            arquivo.save(caminho)
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user,form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html",usuario=usuario,form=None) # a variavel usuario no html é a variavel usuario no python


@app.route("/logout")
@login_required
def logout():
    formlogin = FormLogin()
    logout_user()
    return render_template("homepage.html",form=formlogin)



@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()[:]
    return render_template("feed_test.html",fotos=fotos)