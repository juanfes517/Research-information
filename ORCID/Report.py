import numpy as np

class Report:
  
  def __init__(self):
    self.docentes_no_encontrados = np.array([])
    self.tipos_de_trabajos = np.array([])
    self.trabajos_sin_citas = np.array([])
    self.citas_no_validas = np.array([])
    self.errores_en_cita = np.array([])

  def agregar_doncente_no_encontrado(self, docente):
    self.docentes_no_encontrados = np.append(self.docentes_no_encontrados, docente)

  def agregar_tipo_de_trabajo(self, tipo):
    self.tipos_de_trabajos = np.append(self.tipos_de_trabajos, tipo)
  
  def agregar_trabajo_sin_cita(self, nTrabajo, tipo_trabajo, año_trabajo, docente):
    trabajo_sin_cita = f'Trabajo {nTrabajo} del año {año_trabajo} de tipo {tipo_trabajo} de {docente}'
    self.trabajos_sin_citas = np.append(self.trabajos_sin_citas, trabajo_sin_cita)
  
  def agregar_cita_no_valida(self, nTrabajo, tipo_trabajo, año_trabajo, docente):
    cita_no_valida = f'Trabajo {nTrabajo} del año {año_trabajo} de tipo {tipo_trabajo} de {docente}'
    self.citas_no_validas = np.append(self.citas_no_validas, cita_no_valida)

  def agregar_error_en_cita(self, nTrabajo, tipo_trabajo, año_trabajo, docente):
    error_en_cita = f'Trabajo {nTrabajo} del año {año_trabajo} de tipo {tipo_trabajo} de {docente}'
    self.errores_en_cita = np.append(self.errores_en_cita, error_en_cita)

  def mostrar_resultados(self):
    # Reporte de doncentes no encontrados
    print('____________________________________________________________')
    print('Docentes no encontrados')
    print('Los siguientes docentes no fueron encontrados en la busqueda \no no tienen la Universidad de Antioquia como afiliación\n')
    for docente in self.docentes_no_encontrados:
      print('-',docente)
    print('____________________________________________________________\n\n')

    # Reporte de tipos de trabajo
    print('____________________________________________________________')
    print('Tipos de trabajo')
    for tipo in np.unique(self.tipos_de_trabajos):
      print('-', tipo)
    print('____________________________________________________________\n\n')

    # Reporte de citas no valida
    print('____________________________________________________________')
    print('Citas no validas')
    print('Lo siguientes trabajos no tienen el botón "Switch to expanded formatting"\nnecesario para obtener un XPATH valido')
    for cita_no_valida in self.citas_no_validas:
      print('-', cita_no_valida)
    print('____________________________________________________________\n\n')

    # Reporte de errores al obtener cita
    print('____________________________________________________________')
    print('Error al obtener la cita')
    print('Los siguientes trabajos no tienen un XPATH valido o en el rango indicado (1 a 5)')
    for error_en_cita in self.errores_en_cita:
      print('-', error_en_cita)
    print('____________________________________________________________\n\n')

    # Reporte de trabajos sin cita
    print('____________________________________________________________')
    print('Trabajos sin cita')
    print('Los siguientes trabajos no tienen cita')
    for trabajo_sin_citas in self.trabajos_sin_citas:
      print('-', trabajo_sin_citas)
    print('____________________________________________________________\n\n')
