from CvLAC.CvLAC import CvLAC_projects, scrape_CvLAC
import pandas as pd
from docentes import docentes

df_projects = pd.DataFrame(columns=["Docente", "Tipo_de_proyecto", "Nombre_del_proyecto", "Inicio", "Fin", "Resumen"])

scrape_CvLAC(df_projects, df_projects, df_projects, docentes=docentes)
df_projects.to_csv('test.csv', index=False)

# for docente in docentes:
#   CvLAC_projects(proyectos_df, docente)

