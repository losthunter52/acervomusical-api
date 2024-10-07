from django.db import models

class Autor(models.Model):
    nome = models.CharField(max_length=100, blank=False)

class Genero(models.Model):
    descricao = models.CharField(max_length=100, blank=False)

class Formacao(models.Model):
    descricao = models.CharField(max_length=100, blank=False)

class Edicao(models.Model):
    descricao = models.CharField(max_length=100, blank=False)

class Imagem(models.Model):
    arquivo = models.ImageField(upload_to='images/')

class Partitura(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="partitura_autor")  
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name="partitura_genero")  
    titulo = models.CharField(max_length=220, blank=False)
    formacao = models.ForeignKey(Formacao, on_delete=models.CASCADE, related_name="partitura_formacao")  
    edicao = models.ForeignKey(Edicao, on_delete=models.CASCADE, related_name="partitura_edicao")  
    observacao = models.CharField(max_length=999, blank=True, null=True)
    imagem = models.OneToOneField(Imagem, on_delete=models.CASCADE, blank=True, null=True, related_name="partitura_imagem")
    sequencia = models.CharField(max_length=220, blank=True, null=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)  
