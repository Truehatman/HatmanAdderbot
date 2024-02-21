from pyrogram import Client
import time

api_id = "25047326"
api_hash = "9673ea812441c77e912979cd0f8a2572"

app = Client("my_account", api_id, api_hash)

# Funzione per ottenere la lista dei gruppi dell'account
def get_user_groups(client):
    dialogs = client.get_dialogs()
    return [(i + 1, dialog.chat.id, dialog.chat.title) for i, dialog in enumerate(dialogs)]

# Funzione per ottenere la lista dei membri di un gruppo
def get_group_members(client, chat_id):
    members = client.get_chat_members(chat_id)
    return [member.user for member in members]

# Funzione per verificare se un utente è già nel gruppo
def is_member_in_group(client, chat_id, user_id):
    try:
        member = client.get_chat_member(chat_id, user_id)
        return True
    except:
        return False

# Funzione per aggiungere un membro con ritardo
def add_member_with_delay(client, chat_id, member, delay=60):
    try:
        
        
        # Verifica se l'utente è già nel gruppo
        if not is_member_in_group(client, chat_id, member.id):
            client.add_chat_members(chat_id, user_ids=[member.id])
            print(f"Utente {member.username} aggiunto con successo al gruppo.")
            time.sleep(delay)
        else:
            print(f"L'utente {member.username} è già presente nel gruppo e verrà skippato.")
        
        return True
    except Exception as e:
        print(f"Errore durante l'aggiunta dell'utente {member.username}: {e}")
        return False

# Funzione per aggiungere i membri ad un gruppo con ritardo
def add_members_to_group_with_delay(client, chat_id, members, delay=150):
    for member in members:
        if not member.is_bot and member.username and member.username.lower() != 'anonymous':
            # Verifica se l'utente non è un bot e ha un username
            add_member_with_delay(client, chat_id, member, delay)
        else:
            print(f"Skippato l'utente {member.username} nel processo di aggiunta.")

with app:
    # Ottenere la lista dei gruppi dell'account
    user_groups = get_user_groups(app)

    # Stampa la lista numerata dei gruppi
    print("Lista dei gruppi:")
    for num, group_id, group_title in user_groups:
        print(f"{num}.{group_title}")

    # Chiedi all'utente di scegliere il numero del gruppo da cui esportare
    selected_group_num = int(input("Inserisci il numero del gruppo da cui esportare i membri: "))
    
    # Verifica se il numero scelto è valido
    if 1 <= selected_group_num <= len(user_groups):
        # Ottieni l'ID del gruppo selezionato
        export_group_id = user_groups[selected_group_num - 1][1]

        print("Lista dei gruppi:")
        for num, group_id, group_title in user_groups:
            print(f"{num}.{group_title}")

        # Chiedi all'utente di scegliere il numero del gruppo in cui importare
        selected_group_num = int(input("Inserisci il numero del gruppo in cui importare i membri: "))
        
        # Verifica se il numero scelto è valido
        if 1 <= selected_group_num <= len(user_groups):
            # Ottieni l'ID del gruppo selezionato
            import_group_id = user_groups[selected_group_num - 1][1]

            # Ottenere la lista dei membri del gruppo di esportazione
            export_group_members = get_group_members(app, export_group_id)
            print("Lista dei membri da esportare:")
            print(export_group_members)

            # Aggiungere i membri al gruppo di importazione con ritardo
            add_members_to_group_with_delay(app, import_group_id, export_group_members)

            print("Membri aggiunti con successo!")
        else:
            print("Numero del gruppo non valido. Per favore, inserisci un numero valido.")
    else:
        print("Numero del gruppo non valido. Per favore, inserisci un numero valido.")
