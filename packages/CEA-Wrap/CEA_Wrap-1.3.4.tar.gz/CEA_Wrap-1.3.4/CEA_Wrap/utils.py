import importlib.resources, os.path

def _get_location(file):
  # The reason the manager is used is because our package may be zipped and the manager extracts it
  #   However, this package is not zip-safe so we just return the location
  with importlib.resources.path(__package__, file) as manager:
    return str(manager)

def open_thermo_lib():
  return os.system(_get_location("thermo_spg.inp"))

def open_pdfs():
  os.system('"'+os.path.join("..", _get_location("CEAMathematicalAnalysis.pdf"))+'"')
  #os.system(os.path.join("..", _get_location("CEA Mathematical Analysis.pdf")))
  #os.system(os.path.join("..", _get_location("CEA Users Manual and Program Description.pdf")))