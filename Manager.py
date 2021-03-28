import mysql.connector
import csv
from csv import reader
from tabulate import tabulate

print("\n  *******************************************************\n    Benvingut a la base de dades del C.E. Diagonal Mar!\n  *******************************************************\n")

### IDENTIFICACIÓ ENTRENADOR I MOSTRA DELS EQUIPS #########

cnx = mysql.connector.connect(user='root', password='01Laura34', host='localhost', database='projecten1')
cursor = cnx.cursor()

state = 'inici'
while state != 'exit':    

    if state == 'inici':
        identrenador = input("Abans de res, identifica't amb el teu DNI (sense lletra)\n\nSi vols sortir, escriu 'S'\n\n")
        if identrenador == 'S':
            state = 'exit'
        
        else:

            query = ("SELECT Nom FROM ProjecteN1.Entrenadors WHERE idEntrenador = %s")
            cursor.execute(query, (identrenador,))

            for (nom) in cursor:
                nomentr = nom
    
            try:
                nomentr
                state = 'dnibo'
            except NameError:
                print('El DNI no és vàlid\n\n')
                state = 'inici'
        
    elif state == 'dnibo':
        
        query = ("SELECT idRelacioEquips, idCategoria, idNivell, Temporada FROM ProjecteN1.RelacioEquips WHERE idRelacioEquips IN (SELECT idEquip FROM ProjecteN1.EquipsEntrenadors WHERE idEntrenador = %s)")
        cursor.execute(query, (identrenador,))

        equips = []
        for (idequip, cat, niv, tempo) in cursor:
            newteam = [idequip, cat, niv, tempo]
            equips.append(newteam)
        i = 0
        for equip in equips:
            query = ("SELECT Nom FROM ProjecteN1.Categoria WHERE idCategoria = %s")
            cursor.execute(query, (equip[1],))
            for cat in cursor:
                equips[i].append(cat[0])
                i+=1
        i = 0
        for equip in equips:
            query = ("SELECT Nom, Sexe FROM ProjecteN1.Nivell WHERE idNivell = %s")
            cursor.execute(query, (equip[2],))
            for (niv, sexe) in cursor:
                equips[i].append(niv)
                equips[i].append(sexe)
                i+=1

        print("\nHola",nomentr[0],", s'han trobat",len(equips),"equips associats\n")

        equipstable = []
        i = 1
        sexe = {"F":"Femení", "M":"Masculí"}
        for equip in equips:
            temporada = str(equip[3])[0:2]+"-"+str(equip[3])[2:4]
            new = [i, temporada, equip[4], sexe[equip[6]], equip[5]]
            equipstable.append(new)
            i+=1

        state = 'equips'
    
    elif state == 'equips':
        print(tabulate(equipstable, headers=["idEquip", "Temporada", "Categoria", "Gènere", "Nivell"]))
        print("\n")

###########################################################

### TRIA D'EQUIP I MOSTRA DE JUGADORS #########

        idequip = input("A quin equip t'agradaria accedir? (Indica el número de la primera columna de la taula)\nSi vols sortir escriu 'S'\n")
        if idequip == 'S':
            state = 'exit'
        else:
            try:
                if int(idequip) < 1 or int(idequip) > len(equipstable):
                    print("'",idequip, "'", 'no és un número vàlid\n')
                    state = 'equips'
                else:
                    state = 'jugadors'
            except ValueError:
                print("'",idequip, "'", 'no és un número vàlid\n')
                state = 'equips'
            
    
    elif state == 'jugadors':

        refequip = equips[int(idequip)-1][0]
        print("\nAquests són els jugadors del teu equip:\n")
        query = ("SELECT idJugador, Nom, Cognom1, Cognom2, DataNaixement FROM ProjecteN1.Jugadors WHERE idJugador IN (SELECT idJugador FROM ProjecteN1.EquipsJugadors WHERE idEquip = %s)")
        cursor.execute(query, (refequip,))
        players = []
        for (idjugador, nom, cognom1, cognom2, data) in cursor:
            newplayer = [idjugador, nom, cognom1, cognom2, data]
            players.append(newplayer)

        i = 1
        playerstable = []
        for player in players:
            newp = [i, player[1], player[2], player[3], player[4]]
            playerstable.append(newp)
            i+=1
    
        print(tabulate(playerstable, headers=["idJugador", "Nom", "Cognom 1", "Cognom 2", "Data de Naixement"]))

###########################################################

### TRIA D'ACCIÓ #########

        action = input("\n\nSi vols consultar els valors d'un jugador en particular, indica el seu número identificador\nSi vols introduir un nou jugador a l'equip, escriu 'N'\nSi vols baixar els valors dels teus jugadors en un arxiu, escriu 'B'\nSi vols pujar un arxiu amb valors nous, escriu 'P'\nSi vols tornar a la llista d'equips, escriu 'E'\nSi vols sortir escriu 'S'\n\n")

###########################################################


### BAIXADA D'ARXIU #########

        if (action == 'B'):
            state = 'baixar'
        elif (action == 'P'):
            state = 'pujar'
        elif (action == 'E'):
            state = 'equips'
        elif (action == 'S'):
            state = 'exit'
        elif (action == 'N'):
            state = 'noujugador'
            
        else:
            try:
                if (isinstance(int(action), int) and int(action) > 0 and int(action) <= len(playerstable)):
                    state = 'skills'
                else:
                    print("'",action,"'","no és una opció vàlida\n")
                    state = 'jugadors'
            except ValueError:
                print("'",action,"'","no és una opció vàlida\n")
                state = 'jugadors'
            
        
                   
    elif state == 'baixar':
        
        query = ("SELECT idJugador, idHabilitat, Valor FROM ProjecteN1.RelacioHabilitats WHERE idRelacioEquips = %s")
        cursor.execute(query, (refequip,))
        skills = []
        idsskills = []
        for (idjug, idskill, valskill) in cursor:
            newskill = [idjug, idskill, valskill]
            skills.append(newskill)
            idsskills.append(idskill)
        idsplayers = []
        for player in players:
            idsplayers.append(player[0])
        bigtable = []
        for idplayer in idsplayers:
            newrow = [idplayer]
            for skill in skills:
                if(skill[0] == idplayer):
                    newrow.append(skill[2])
            bigtable.append(newrow)
    
        query = ("SELECT Nom FROM ProjecteN1.Habilitats WHERE idHabilitat = %s")
        nomsskills = []
        for i in idsskills:
            cursor.execute(query, (i,))
            for nom in cursor:
                nomsskills.append(nom[0])
    
    
        finaltable = [["DNI", "Nom", "Cognom 1", "Cognom 2"]+nomsskills[0:]]
        for row in bigtable:
            idplayer = row[0]
            for player in players:
                if player[0] == idplayer:
                    newrowfinal = player[:4]+row[1:]
                    finaltable.append(newrowfinal)


        with open('table.csv', 'w', newline ='') as f:
            wr = csv.writer(f)
            wr.writerows(finaltable)
    
        f.close()
    
        print(tabulate(finaltable[1:], headers = ["DNI", "Nom", "Cognom 1", "Cognom 2"]+nomsskills[0:3]))
        res = input("\nAquesta és la informació que s'escriurà a l'arxiu. Escriu 'ok' per continuar\nSi vols tornar a la taula de jugadors escriu 'J'\nSi vols sortir escriu 'S'\n")
        
        if res == 'ok':
            print("\nArxiu 'table.csv' creat\n")
            state = 'jugadors'
        elif res == 'S':
            state = 'exit'
        elif res == 'J':
            state = 'jugadors'
        else:
            print("'",res,"' no és una opció vàlida")
            state = 'jugadors'
    

###########################################################


### PUJADA D'ARXIU #########

    elif (state == 'pujar'):
        filename = input("Indica el nom de l'arxiu\nSi vols tornar a la taula de jugadors escriu 'J'\nSi vols sortir escriu 'S'\n")
        
        if filename == 'J':
            state = 'jugadors'
        
        elif filename == 'S':
            state = 'exit'
        
        else:
            try:
                with open(filename, 'r') as read_obj:
                    csv_reader = reader(read_obj)
                    listrows = list(csv_reader)
                read_obj.close()
    
                print(tabulate(listrows[1:], headers = listrows[0]))
                actualitzar = input("\nAquesta és la informació que has pujat. Vols actualitzar la base de dades? (s/n)\n")
                if actualitzar == 's':
                    skillsrelacio = {}
                    query = ("SELECT idHabilitat, Nom FROM ProjecteN1.Habilitats WHERE Nom = %s")
                    for skill in listrows[0][4:]:
                        cursor.execute(query, (skill,))
                        for (idskill, nomskill) in cursor:
                            skillsrelacio[nomskill] = idskill
        
                    tuplelist = []
                    k = 0
                    for i in range(1,len(listrows)):
                        for j in range(4,len(listrows[0])):
                            newentry = ()
                            query = ("SELECT idRelacioHabilitats FROM ProjecteN1.RelacioHabilitats WHERE (idJugador = %s AND idRelacioEquips = %s AND idHabilitat = %s)")
                            cursor.execute(query, (listrows[i][0], refequip, skillsrelacio[listrows[0][j]]))
                            for idnou in cursor:
                                idbo = idnou[0]
                            query = ("UPDATE ProjecteN1.RelacioHabilitats SET Valor = %s WHERE idRelacioHabilitats = %s") 
                            cursor.execute(query, (listrows[i][j], idbo))
                            cnx.commit() 
                
                    print("\n\n La base de dades s'ha actualitzat correctament\n")
        
                    state = 'jugadors'
        
                else:
                    state = 'jugadors'
            except FileNotFoundError:
                print("No s'ha trobat l'arxiu\n")
                state = 'pujar'
                

###########################################################


### CONSULTA D'UN JUGADOR #########

    elif(state == 'skills'):
        query = ("SELECT idJugador, idHabilitat, Valor FROM ProjecteN1.RelacioHabilitats WHERE idJugador = %s AND idRelacioEquips = %s")

        cursor.execute(query, (players[int(action)-1][0], refequip))
        skills = []
        for (idjug, idskill, valskill) in cursor:
            newskill = [idjug, idskill, valskill]
            skills.append(newskill)

        i = 0
        for skill in skills:
            query = ("SELECT Nom FROM ProjecteN1.Habilitats WHERE idHabilitat = %s")
            cursor.execute(query, (skill[1],))
    
            for skillname in cursor:
                skills[i].append(skillname[0])
                i+=1

        print("\nAquests són els valors pel jugador", players[int(action)-1][1], players[int(action)-1][2], players[int(action)-1][3],":\n")

        skillstable = []

        for skill in skills:
            new = [skill[3], skill[2]]
            skillstable.append(new)
    
        print(tabulate(skillstable, headers=["Habilitat", "Valor"]))

        tornar = input("\nSi vols tornar a la llista de jugadors, escriu 'J'\nSi vols tornar a la llista d'equips, escriu 'E'\nSi vols sortir, escriu 'S'\n")
        
        if tornar == 'J':
            state = 'jugadors'
        elif tornar == 'E':
            state = 'equips'
        elif tornar == 'S':
            state = 'exit'
        else:
            print("'",tornar,"' no és una opció vàlida")
            state = 'skills'

###########################################################

### NOU JUGADOR #########

    elif state == 'noujugador':
        dninou = input("Introdueix les següents dades pel nou jugador (Si vols tornar a la taula de jugadors, escriu 'J'):\nDNI:\n")
        if dninou != 'J':
            nomnou = input("Nom\n")
            cognom1nou = input("Cognom 1\n")
            cognom2nou = input("Cognom 2\n")
            datanou = input("Data de Naixement (Format YYYY-MM-DD)\n")
            print("Les dades a introduir són:\nDNI:",dninou,"\nNom:",nomnou,cognom1nou,cognom2nou,"\nData de Naixement:",datanou,"\n")
            confirmar = input("Estàs d'acord? (s/n)")
            if confirmar == 'n':
                state = 'noujugador'
            elif confirmar == 's':
            
                try:
                    noujugador = (int(dninou), nomnou, cognom1nou, cognom2nou, datanou)
                    query = ("INSERT INTO ProjecteN1.Jugadors (idJugador, Nom, Cognom1, Cognom2, DataNaixement) VALUES (%s, %s, %s, %s, %s)")
                    cursor.execute(query, noujugador)
                    cnx.commit()
                    query = ("INSERT INTO ProjecteN1.EquipsJugadors (idEquip, idJugador) VALUES (%s, %s)")
                    cursor.execute(query, (int(refequip), int(dninou)))
                    cnx.commit()
                    query = ("SELECT DISTINCT idHabilitat FROM ProjecteN1.Habilitats")
                    cursor.execute(query)
                    idhabilitats = []
                    for novahabilitat in cursor:
                        idhabilitats.append(novahabilitat[0])
                    for habilitat in idhabilitats:
                        query = ("INSERT INTO ProjecteN1.RelacioHabilitats (idJugador, idRelacioEquips, idHabilitat, Valor) VALUES (%s, %s, %s, %s)")
                        cursor.execute(query, (int(dninou), int(refequip), int(habilitat), 0))
                        cnx.commit()
            
                    print("S'ha actualitzat la base de dades correctament")
                    state = 'jugadors'
            
                except:
                    print("\n\nLes dades no són vàlides. Revisa-les\n")
                    state = 'noujugador'
        
            
            else:
                print(confirmar, "no és una opció vàlida.")
                state = 'noujugador'
        else:
            state = 'jugadors'  



print("\n\nD'acord, adéu!\n\n")
cnx.close()
cursor.close()
