from django import forms

class GrafoForm(forms.Form):
  digrafo = forms.BooleanField(label="Digrafo", required=False)
  digrafo.widget_attrs(widget={
    "class": "form-check-input appearance-none h-4 w-4 border border-gray-300 rounded-sm bg-white checked:bg-blue-600 checked:border-blue-600 focus:outline-none transition duration-200 mt-1 align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-pointer",
  })
  grafo_text = forms.CharField(widget=forms.Textarea(attrs={
      "class": " form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white  focus:border-blue-600 focus:outline-none",
      "rows" : "10",
      "placeholder" : "Insira o grafo aqui",
      "cols":20,
      }),
      label="", required=False)
  vertice_grau = forms.CharField(required=False)
  vertice_grau.widget_attrs(widget={
    "class": "form-check-input appearance-none h-4 w-4 border border-gray-300 rounded-sm bg-white checked:bg-blue-600 checked:border-blue-600 focus:outline-none transition duration-200 mt-1 align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-pointer",
    "placeholder" : "Insira o nome",
  })
  vertice_adj = forms.CharField(required=False)
  vertice_adj.widget_attrs(widget={
    "class": "form-check-input appearance-none h-4 w-4 border border-gray-300 rounded-sm bg-white checked:bg-blue-600 checked:border-blue-600 focus:outline-none transition duration-200 mt-1 align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-pointer",
    "placeholder" : "Insira o nome do verice",
  })
  short_path = forms.CharField(required=False)
  short_path.widget_attrs(widget={
    "class": "form-check-input appearance-none h-4 w-4 border border-gray-300 rounded-sm bg-white checked:bg-blue-600 checked:border-blue-600 focus:outline-none transition duration-200 mt-1 align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-pointer",
    "placeholder" : "Insira o nome do verice",
  })
