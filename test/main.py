import pandas as pd 

from functions import insert_row_and_update, show_stats

poblation_list = [
    './dataPruebaDataEngineer/2012-1.csv',
    './dataPruebaDataEngineer/2012-2.csv',
    './dataPruebaDataEngineer/2012-3.csv',
    './dataPruebaDataEngineer/2012-4.csv',
    './dataPruebaDataEngineer/2012-5.csv'
]

validation_list = ['./dataPruebaDataEngineer/validation.csv']

def poblation_stage():
    for file in poblation_list:
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            insert_row_and_update(row)
        print(f"Archivo procesado: {file}")
        print("Estadisticas actuales del archivo:")
        show_stats()

def validation_stage():
    for file in validation_list:
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            insert_row_and_update(row)
        print(f"Archivo de validacion procesado: {file}")
        print("Estadisticas actuales del archivo de validacion:")
        show_stats()

def main():
    # Carga de datos inicial
    poblation_stage()

    # Etapa de validacion
    validation_stage()
    

if __name__ == "__main__":
    main()




