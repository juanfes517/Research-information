from CvLAC.projects import CvLAC_projects
import pandas as pd
from docentes import docentes

proyectos_df = pd.DataFrame(columns=["Docente", "Tipo_de_proyecto", "Nombre_del_proyecto", "Inicio", "Fin", "Resumen"])

for docente in docentes:
  CvLAC_projects(proyectos_df, docente)

proyectos_df.to_csv('proyectos.csv', index=False)
