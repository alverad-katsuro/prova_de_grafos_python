from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
from .forms import GrafoForm
from grafo.strucs.Grafo import Grafo
from base64 import b64encode


def index(request):
  form = GrafoForm()
  grafo = Grafo()
  if request.method == 'POST':
    if request.POST.get('digrafo') == "on":
      grafo.digrafo = True
    if request.POST.get('digrafo') == "False":
      grafo.digrafo = False
    grafo.createDataFrame(request.POST.get("grafo_text"))
    img = grafo.createImg()
    form.fields["grafo_text"].initial = request.POST.get('grafo_text')
    form.fields["digrafo"].initial = request.POST.get('digrafo')
    context = {
          'form': form,
          'image': b64encode(img).decode()
      }
  else:
    context = {
        'form': form,
    }

  return render(request, "index.html", context)