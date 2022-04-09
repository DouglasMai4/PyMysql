import PySimpleGUI as sg
import mysql.connector as mysql

sg.theme('DarkGrey11')
layout = [[sg.Text('Usuario'), sg.InputText()],
          [sg.Text('Senha  '), sg.InputText(password_char='*')],
          [sg.Button('Cancelar'), sg.Button('OK')]]
window = sg.Window('Conectar', layout)
event, values = window.read()
window.close()

if event == sg.WIN_CLOSED or event == 'Cancelar':
    exit
elif event == 'OK':
    mydb = mysql.connect(
      host='144.22.239.20',
      port='3307',
      user=values[0],
      password=values[1],
      database='PRODUTOS'
    )
    mycursor = mydb.cursor()
    while True:
        sql = "SELECT Nome, ValorAnt, ValorAtu FROM PRODUTO"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        itens = []
        data = []
        c = 0
        for row in myresult:
            data.append([])
            data[c].append(row[0])
            data[c].append(row[1])
            data[c].append(row[2])
            c += 1

        cabecario = ['Nome', 'Valor Anterior', 'Valor Atual']
        layout = [[sg.Table(values=data, headings=cabecario, max_col_width=25,
                            background_color='#313641',
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='center',
                            num_rows=20,
                            alternating_row_color='#1c1f22',
                            key='-TABLE-',
                            row_height=20)],
                  [sg.Button('Adicionar', size=(21, 1)), sg.Button('Remover', size=(20, 1))],
                  [sg.Button('Cancelar', size=(47, 1))]]
        window = sg.Window('Menu', layout)
        event, values = window.read()
        window.close()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        elif event == 'Adicionar':
            while True:
                layout = [[sg.Text('Adicionar Item')],
                          [sg.Text('Nome:           '), sg.InputText()],
                          [sg.Text('Valor Anterior:'), sg.InputText()],
                          [sg.Text('Valor Atual:    '), sg.InputText()],
                          [sg.Button('Cancelar'), sg.Button('OK')]]
                window = sg.Window('Adicionar', layout)
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancelar':
                    window.close()
                    break
                elif event == 'OK':
                    mycursor.execute(
                        f'INSERT INTO PRODUTO (Nome, ValorAnt, ValorAtu) VALUES ("{values[0]}", {values[1]}, {values[2]});')
                    mydb.commit()
                    window.close()

                    layout = [[sg.Text('Item adicionado com sucesso')],
                              [sg.Button('OK', size=(22, 1))]]
                    window = sg.Window('Sucesso', layout)
                    event, values = window.read()
                    if event == sg.WIN_CLOSED or event == 'OK':
                        window.close()
        elif event == 'Remover':
            while True:
                layout = [[sg.Text('Nome do item: '), sg.InputText()],
                          [sg.Button('Remover Item', size=(26, 1)), sg.Button('Remover Todos', size=(25, 1))],
                          [sg.Button('Cancelar', size=(57, 1))]]
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
                              [sg.Button('OK', size=(22, 1))]]
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
