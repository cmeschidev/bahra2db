import pandas as pd
import os


path_to_csv = os.path.join("data", "base_total.csv")

# Importa CSV BAHRA
df = pd.read_csv(path_to_csv, dtype=str)

df["lat_gs_long_gs"] = df["lat_gs"] + " / " + df["long_gs"]
df["lat_gd"] = pd.to_numeric(df["lat_gd"], errors="coerce")
df["long_gd"] = pd.to_numeric(df["long_gd"], errors="coerce")
df['cod_loc'] = df['cod_ase'].apply( lambda s: s[:8])

# === Provincias ===
provincias = df[["cod_pcia", "nom_pcia", "lat_gd", "long_gd", "lat_gs_long_gs"]] \
    .drop_duplicates(subset=["cod_pcia"]) \
    .sort_values("cod_pcia") \
    .reset_index(drop=True)

# === Departamentos ===
departamentos = df[["cod_pcia", "cod_depto", "nom_depto", "lat_gd", "long_gd", "lat_gs", "long_gs"]] \
    .drop_duplicates(subset=["cod_pcia", "cod_depto"]) \
    .sort_values("cod_depto") \
    .reset_index(drop=True)

# === Departamentos de aglomerados ===
depar_aglo = df[["cod_aglo", "cod_depto"]] \
    .dropna(subset=["cod_depto", "cod_aglo"]) \
    .drop_duplicates(subset=["cod_aglo", "cod_depto"]) \
    .sort_values(["cod_aglo", "cod_depto"]) \
    .reset_index(drop=True)

# === Entidades ===
entidades = df[df["tipo"].str.startswith("Entidad")]    
entidades = entidades[[ "cod_pcia", "cod_depto", "cod_aglo", "cod_agl", "cod_loc", "cod_ase", "nombre", "lat_gd", "long_gd", "lat_gs", "long_gs"]] \
    .dropna(subset=["cod_ase", "nombre"]) \
    .drop_duplicates(subset=["cod_ase"]) \
    .sort_values(["cod_pcia", "cod_depto", "nombre"]) \
    .reset_index(drop=True)

# === Bases antarticas ===
bases = df[df["tipo"].str.startswith("Base")]    
bases = bases[[ "cod_pcia", "cod_depto",  "cod_ase", "nombre", "lat_gd", "long_gd", "lat_gs", "long_gs"]] \
    .dropna(subset=["cod_ase", "nombre"]) \
    .drop_duplicates(subset=["cod_ase"]) \
    .sort_values(["cod_pcia", "cod_depto", "nombre"]) \
    .reset_index(drop=True)

# === Parajes ===
parajes = df[df["tipo"].str.startswith("Paraje")]
parajes = parajes[[ "cod_pcia", "cod_depto", "cod_aglo", "cod_agl" ,"cod_ase", "nombre", "lat_gd", "long_gd", "lat_gs", "long_gs"]] \
    .dropna(subset=["cod_ase", "nombre"]) \
    .drop_duplicates(subset=["cod_ase"]) \
    .sort_values(["cod_pcia", "cod_depto", "nombre"]) \
    .reset_index(drop=True)

# === Localidades ===
localidades = df[df["tipo"].str.startswith("Localidad") | df["tipo"].str.startswith("Componente") ]
localidades = localidades[[ "cod_pcia", "cod_depto", "cod_aglo", "cod_agl", "cod_ase", "tipo", "nombre", "lat_gd", "long_gd", "lat_gs", "long_gs"]] \
    .dropna(subset=["cod_ase", "nombre"]) \
    .drop_duplicates(subset=["cod_ase"]) \
    .sort_values(["cod_pcia", "cod_depto", "nombre"]) \
    .reset_index(drop=True)
localidades["tipo"] = localidades["tipo"].apply( lambda t: t[:1])

# === Aglomerados ===
aglomerados = df[[ "cod_aglo", "cod_pcia" , "nom_aglo"]] \
    .dropna(subset=["cod_aglo", "nom_aglo"]) \
    .drop_duplicates(subset=["cod_aglo"]) \
    .sort_values(["cod_aglo", "cod_pcia"]) \
    .reset_index(drop=True)

# === Gobiernos locales ===
gob_locales = df[[ "cod_pcia", "cod_depto", "cod_aglo", "cod_agl", "nom_agl"  ]] \
    .sort_values( ["cod_pcia", "cod_agl"] ) \
    .dropna(subset=["cod_agl", "nom_agl", "cod_depto" ]) \
    .drop_duplicates(subset=["cod_agl", "cod_depto"]) \
    .reset_index(drop=True)

control = pd.DataFrame( columns=["tabla", "archivo", "filas", "columnas"]);
print( control )


# === Helpers ===
def sql_str(s):
    if pd.isna(s): return "NULL"
    return "'" + str(s).replace("'", "''") + "'"

# === Genera comandos INSERT IGNORE ===

def generar_csv(df, tabla, info=True):
    os.makedirs("out", exist_ok=True)
    archivo_out = f"out/{tabla}.csv"

    info = [  tabla, archivo_out, len(df), len(df.columns)  ]
    global control
    control.loc[len(control)] = info
    
    with open(archivo_out, "w", encoding="utf-8") as f:
        # Escribir encabezado
        columnas = df.columns.tolist()
        f.write("\t".join(columnas) + "\n")

        # Escribir cada fila
        for _, row in df.iterrows():
            valores = [
                str(val) if pd.notna(val) else ""
                for val in row
            ]
            f.write("\t".join(valores) + "\n")
    print( archivo_out )
        

def generar_inserts(df, tabla):
    os.makedirs("sql", exist_ok=True)
    archivo_out = f"sql/insert_{tabla}.sql"

    with open(archivo_out, "w", encoding="utf-8") as f:
        columnas = df.columns.tolist()
        for _, row in df.iterrows():
            values = []
            for val in row:
                if isinstance(val, str):
                    values.append(sql_str(val))
                elif pd.isna(val):
                    values.append("NULL")
                else:
                    values.append(str(val))
            stmt = f"INSERT IGNORE INTO {tabla} ({', '.join(columnas)})\nVALUES ({', '.join(values)});"
            f.write(stmt + "\n")

def bahra2db( sql = False ) :
    generar_csv(provincias, "provincias")
    generar_csv(departamentos, "departamentos")
    generar_csv(depar_aglo, "depar_de_aglo")
    generar_csv(aglomerados, "aglomerados")
    generar_csv(gob_locales, "gob_locales")
    generar_csv(localidades, "localidades")
    generar_csv(entidades, "entidades")
    generar_csv(bases, "bases")
    generar_csv(parajes, "parajes")  
    
    generar_csv(control, "control_bahra")  
    print("✅ Archivos csv generados!")

    if( sql) :
        generar_inserts(provincias, "provincias")
        generar_inserts(departamentos, "departamentos")
        generar_inserts(aglomerados, "aglomerados")
        generar_inserts(depar_aglo, "depar_de_aglo")
        generar_inserts(gob_locales, "gob_locales")
        generar_inserts(localidades, "localidades")
        generar_inserts(entidades, "entidades")
        generar_inserts(bases, "bases")
        generar_inserts(parajes, "parajes")
        generar_inserts(control, "control_bahra")
        print("✅ Archivos sql generados!")   

bahra2db()

