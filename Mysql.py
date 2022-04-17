import PySimpleGUI as sg
import mysql.connector as mysql

sg.theme('DarkGrey11')
layout = [[sg.Text('Usuario:', size=(8, 1)), sg.InputText(expand_x=True)],
          [sg.Text('Senha:', size=(8, 1)), sg.InputText(password_char='*', expand_x=True)],
          [sg.Button('Cancelar'), sg.Button('OK')]]
window = sg.Window('Conectar', layout)
event, values = window.read()
window.close()

if event == sg.WIN_CLOSED or event == 'Cancelar':
    exit
elif event == 'OK':
    mydb = mysql.connect(
      host='168.138.140.85',
      port='3306',
      user=values[0],
      password=values[1],
      database='PRODUTOS'
    )
    mycursor = mydb.cursor()
    while True:
        sql = "SELECT * FROM PRODUTO"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        itens = []
        c = 0
        for row in myresult:
            itens.append([])
            itens[c].append(row[0])
            itens[c].append(row[1])
            itens[c].append(row[2])
            itens[c].append(row[3])
            itens[c].append(row[4])
            itens[c].append(row[5])
            itens[c].append(row[6])
            itens[c].append(row[7])
            itens[c].append(row[8])
            itens[c].append(row[9])
            itens[c].append(row[10])
            itens[c].append(row[11])
            itens[c].append(row[12])
            c += 1

        cabecario = ['Nome', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        layout = [[sg.Table(values=itens, headings=cabecario, max_col_width=25,
                            background_color='#313641',
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='center',
                            num_rows=20,
                            alternating_row_color='#1c1f22',
                            key='-TABLE-',
                            row_height=20)],
                  [sg.Button('Adicionar', expand_x=True), sg.Button('Remover', expand_x=True)],
                  [sg.Button('Cancelar', expand_x=True)]]
        window = sg.Window('Menu', layout)
        event, values = window.read()
        window.close()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        elif event == 'Adicionar':
            while True:
                layout = [[sg.Text('Adicionar Item')],
                          [sg.Text('Nome:', size=(9, 1)), sg.InputText(expand_x=True)],
                          [sg.Text('Janeiro:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Fevereiro:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Março:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Abril:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Maio:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Junho:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Julho:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Agosto:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Setembro:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Outubro:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Novembro:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Text('Dezembro:', size=(9, 1)), sg.InputText(0, expand_x=True)],
                          [sg.Button('Cancelar'), sg.Button('OK')]]
                window = sg.Window('Adicionar', layout)
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancelar':
                    window.close()
                    break
                elif event == 'OK':
                    mycursor.execute(
                        f'INSERT INTO PRODUTO VALUES ("{values[0]}", {values[1]}, {values[2]}, {values[3]}, {values[4]}, {values[5]}, {values[6]}, {values[7]}, {values[8]}, {values[9]}, {values[10]}, {values[11]}, {values[12]});')
                    mydb.commit()
                    window.close()

                    layout = [[sg.Text('Item adicionado com sucesso')],
                              [sg.Button('OK', expand_x=True)]]
                    window = sg.Window('Sucesso', layout)
                    event, values = window.read()
                    if event == sg.WIN_CLOSED or event == 'OK':
                        window.close()
        elif event == 'Remover':
            while True:
                layout = [[sg.Text('Nome do item: '), sg.InputText(expand_x=True)],
                          [sg.Button('Remover Item', expand_x=True), sg.Button('Remover Todos', expand_x=True)],
                          [sg.Button('Cancelar', expand_x=True)]]
                window = sg.Window('Remover Item', layout)
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancelar':
                    window.close()
                    break
                elif event == 'Remover Item':
                    mycursor.execute(f'DELETE FROM PRODUTO WHERE Nome = "{values[0]}"')
                    mydb.commit()
                    window.close()

                    layout = [[sg.Text('Item removido com sucesso')],
                              [sg.Button('OK', expand_x=True)]]
                    window = sg.Window('Sucesso', layout)
                    event, values = window.read()
                    if event == sg.WIN_CLOSED or event == 'OK':
                        window.close()
                elif event == 'Remover Todos':
                    window.close()
                    layout = [[sg.Text('Tem certeza ?')],
                              [sg.Button('Sim'), sg.Button('Não')]]
                    window = sg.Window('Remover', layout)
                    event, values = window.read()
                if event == 'Sim':
                    mycursor.execute('TRUNCATE TABLE PRODUTO;')
                    window.close()
                    break
                elif event == 'Não':
                    window.close()
window.close()
