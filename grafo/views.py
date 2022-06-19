from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
from .forms import GrafoForm
from grafo.structs.Grafo import Grafo
from base64 import b64encode

grafo = Grafo()


def index(request):
  global grafo
  form = GrafoForm()
  context = {}
  if request.method == 'POST':
    print(request.POST)
    if "botao_cria_grafo" in request.POST:
      grafo = Grafo()
      if request.POST.get('digrafo') == "on":
        grafo.digrafo = True
      if request.POST.get('digrafo') == "False":
        grafo.digrafo = False
      grafo.createDataFrame(request.POST.get("grafo_text"))
      grafo.createImg()
    if "botao_verifica_aresta" in request.POST:
      entrada = request.POST.get('vertice_aresta').split()
      if (request.POST.get('vertice_aresta') == ""):
        grafo.log.append(f"Há arestas no grafo: {grafo.containsAresta()}")
      elif (len(entrada) == 1):
        grafo.log.append(f"Há aresta no vertice {entrada[0]}: {grafo.containsAresta(entrada[0])}")
      else:
        grafo.log.append(f"Há aresta entre os vertices {entrada[0]} e {entrada[1]}: {grafo.containsAresta(entrada[0],entrada[1])}")
    if "botao_verifica_grau" in request.POST:
      grafo.log.append(f"O Grau do Vertice {request.POST.get('vertice_grau')} é: {grafo.calcGrau(request.POST.get('vertice_grau'))}")
    if "botao_verifica_adj" in request.POST:
      grafo.log.append(f"Os vertices adjacentes são: {grafo.calcAdjacencia(request.POST.get('vertice_adj'))}")
    if "botao_grafo_nori_conexo" in request.POST:
      grafo.log.append(f"O grafo não orientado é conexo?: {grafo.conexidadeGrafo()}")
    if "botao_veri_digra_frac_conexo" in request.POST:
      pass
    if "botao_veri_digra_uni_conexo" in request.POST:
      pass
    if "botao_di_fort_conex" in request.POST:
      pass
    if "botao_graf_ciclo?" in request.POST:
      grafo.log.append(f"O grafo possui ciclo?: {grafo.hasCiclo()}")
    if "botao_dig_aci_cone_ord_top" in request.POST:
      grafo.ordenacaoTopologica()
    if "botao_veri_planar_2-con_eule" in request.POST:
      pass
    if "botao_caminho_curto_custo" in request.POST:
      pass
    if "botao_arv_min" in request.POST:
      pass
    if grafo.imagem_bin != None:
      context["image"] = b64encode(grafo.imagem_bin).decode()
    form.fields["grafo_text"].initial = request.POST.get('grafo_text')
    form.fields["digrafo"].initial = request.POST.get('digrafo')
    context['form'] = form
    context['grafo'] = grafo
  else:
    context = {
        'form': form,
    }

  return render(request, "index.html", context)