"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una camp de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clients para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios files csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los files comprimidos (sin
    descomprimirlos). Se desea partir la data en tres files csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada file debe tener las columnas indicadas.

    Los tres files generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    import os
    import zipfile
    import pandas as pd
    from glob import glob

    dir_in = os.path.join("files", "input")
    
    dir_out = os.path.join("files", "output")
    
    os.makedirs(dir_out, exist_ok=True)

    data = []

    files_zip = glob(os.path.join(dir_in, "*.zip"))
    for file_zip in files_zip:
    
        with zipfile.ZipFile(file_zip, 'r') as zip_abierto:
    
            for file in zip_abierto.namelist():
                if file.endswith(".csv"):
    
                    with zip_abierto.open(file) as contenido:
                        df = pd.read_csv(contenido)
                        data.append(df)

    if not data:
        return

    datos = pd.concat(data, ignore_index=True)

    # Datos del cliente
    clients = pd.DataFrame({
        "client_id": datos["client_id"],
        "age": datos["age"],
        "job": datos["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False),
        "marital": datos["marital"],
        "education": datos["education"].str.replace(".", "_", regex=False)
    })
    
    clients["education"].replace("unknown", pd.NA, inplace=True)
    
    clients["credit_default"] = datos["credit_default"].str.lower().eq("yes").astype(int)
    
    clients["mortgage"] = datos["mortgage"].str.lower().eq("yes").astype(int)
    
    clients.to_csv(os.path.join(dir_out, "client.csv"), index=False)

    # Datos de la camp
    camp = pd.DataFrame({
        "client_id": datos["client_id"],
        "number_contacts": datos["number_contacts"],
        "contact_duration": datos["contact_duration"],
        "previous_campaign_contacts": datos["previous_campaign_contacts"],
        "previous_outcome": datos["previous_outcome"].str.lower().eq("success").astype(int),
        "campaign_outcome": datos["campaign_outcome"].str.lower().eq("yes").astype(int),
    })

    meses = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    
    dias = datos["day"].astype(str).str.zfill(2)
    
    mes_numerico = datos["month"].str.lower().map(meses)
    
    camp["last_contact_date"] = "2022-" + mes_numerico + "-" + dias
    
    camp.to_csv(os.path.join(dir_out, "campaign.csv"), index=False)

    # Información económica
    
    eco = datos[["client_id", "cons_price_idx", "euribor_three_months"]]
    
    eco.to_csv(os.path.join(dir_out, "economics.csv"), index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()