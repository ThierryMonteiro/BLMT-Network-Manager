
import tkinter as tk
from tkinter import ttk
import pandas as pd

root = tk.Tk()
root.title("")
screen_width = root.winfo_screenwidth()  
screen_height = root.winfo_screenheight()  
root.geometry(f"{screen_width}x{screen_height}")
root.config(bg="#D3D3D3") 
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

dados1 = {'Coluna 1': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
          'Coluna 2': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
dados2 = {'Coluna X': ['W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F'],
          'Coluna Y': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
dados3 = {'Coluna 1': ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1'],
          'Coluna 2': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}
dados4 = {'Coluna X': ['W1', 'X1', 'Y1', 'Z1', 'A1', 'B1', 'C1', 'D1', 'E1', 'F1'],
          'Coluna Y': [110, 120, 130, 140, 150, 160, 170, 180, 190, 200]}

df1 = pd.DataFrame(dados1)
df2 = pd.DataFrame(dados2)
df3 = pd.DataFrame(dados3)
df4 = pd.DataFrame(dados4)

dataframes_lista = [df1, df2, df3, df4]
dataframe = df1
indice_tabela1 = 0

def exibir_tabelas():
    
    # tabela 1
    frame1 = tk.Frame(root)
    frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    tree1 = ttk.Treeview(frame1, columns=list(dataframes_lista[indice_tabela1].columns), show="headings", height=10)
    for col in dataframes_lista[indice_tabela1].columns:
        tree1.heading(col, text=col)
        tree1.column(col, anchor="center", width=100) 

    for _, row in dataframes_lista[indice_tabela1].iterrows():
        tree1.insert("", "end", values=list(row))

    scrollbar_y1 = tk.Scrollbar(frame1, orient="vertical", command=tree1.yview)
    scrollbar_x1 = tk.Scrollbar(frame1, orient="horizontal", command=tree1.xview)
    tree1.configure(yscrollcommand=scrollbar_y1.set, xscrollcommand=scrollbar_x1.set)
    scrollbar_y1.pack(side="right", fill="y")
    scrollbar_x1.pack(side="bottom", fill="x")
    tree1.pack(fill=tk.BOTH, expand=True)

    # tabela 2
    frame2 = tk.Frame(root)
    frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    tree2 = ttk.Treeview(frame2, columns=list(dataframe.columns), show="headings", height=10)
    for col in dataframe.columns:
        tree2.heading(col, text=col)
        tree2.column(col, anchor="center", width=100)  

    for _, row in dataframe.iterrows():
        tree2.insert("", "end", values=list(row))
    
    scrollbar_y2 = tk.Scrollbar(frame2, orient="vertical", command=tree2.yview)
    scrollbar_x2 = tk.Scrollbar(frame2, orient="horizontal", command=tree2.xview)
    tree2.configure(yscrollcommand=scrollbar_y2.set, xscrollcommand=scrollbar_x2.set)
    scrollbar_y2.pack(side="right", fill="y")
    scrollbar_x2.pack(side="bottom", fill="x")
    tree2.pack(fill=tk.BOTH, expand=True)


def atualizar_dados():
    global indice_tabela1

    indice_tabela1 = (indice_tabela1 + 1) % len(dataframes_lista)

    exibir_tabelas()

# aqui colocar os dataframes recebidos pelo "back"
def descobrir_dados():
    #colocar nessa variável a lista de dataframes 
    #global dataframes_lista

    #colocar nessa variável o dataframe dos dispositivos conhecidos 
    #global #colocar nessa variável a lista de dataframes 
    #global dataframe

    atualizar_dados()


btn_descobrir = tk.Button(root, text='Descobrir Dados', command=descobrir_dados, padx=20, pady=20, font=('Arial', 16), bg="#ADD8E6", fg="#282c35")
btn_descobrir.grid(row=1, column=1, padx=10, pady=20, sticky="nsew")

btn_proximo_df = tk.Button(root, text='Próxima Interface', command=atualizar_dados, padx=20, pady=20, font=('Arial', 16), bg="#ADD8E6", fg="#282c35")
btn_proximo_df.grid(row=1, column=0, padx=10, pady=20, sticky="nsew")

descobrir_dados()
#exibir_tabelas()
root.mainloop()


