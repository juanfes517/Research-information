from CvLAC.projects import CvLAC_projects
import pandas as pd

proyectos_df = pd.DataFrame(columns=["Docente", "Tipo_de_proyecto", "Nombre_del_proyecto", "Inicio", "Fin", "Resumen"])

CvLAC_projects(proyectos_df, 'MARIA BERNARDA SALAZAR SANCHEZ')

proyectos_df.to_csv('proyectos.csv', index=False)