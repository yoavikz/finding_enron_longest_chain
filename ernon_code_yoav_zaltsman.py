import json

#this function recieves a single email as dict, returns a key(identification\
#  to be later used). for each email the key is a string starting with the\
#  subject and then the participants of the email sorted alphabetically
def generate_key(email):
    participants = [email['sender']]
    for rec in email['recipients']:
        participants.append(str(rec))
    #Sorting participants list because as long as we have the same subject\
    #and same participants, it's the same chain, we don't mind who's the\
    #sender and who recieves the message
    participants = sorted(participants)
    key = email['subject']
    for par in participants:
        key += ' '
        key += str(par)
    # removing spaces and unwated char from beggining of the key
    #We remove "Re:" because we want the same identification for both send \
    #and reply
    while (key[0] == ' '):
        key = key[1:]
    return key

#This function iterates the file, returns "chain_identifier_vs_length"\
#a dictionary with chain identification as key (the return value of \
# "generate_key(email)" the value is another dict with length of chain and \
# ids of the messages involved in this chain
def chain_info_from_file(file):
    chain_identifier_vs_length = {}
    for mail in file:
        mail = json.loads(mail)
        mail_key = generate_key(mail)
        if not "Re:" in mail_key[:5]:
            continue
        if (mail_key in chain_identifier_vs_length):
            chain_identifier_vs_length[mail_key]["length"] += 1
            chain_identifier_vs_length[mail_key]["ids"].append([mail['_id']])

        else:
            chain_identifier_vs_length[mail_key] = {}
            chain_identifier_vs_length[mail_key]["length"] = 2
            chain_identifier_vs_length[mail_key]["ids"] = [mail['_id']]
        # if chain_identifier_vs_length[mail_key[4:]]:
        #     chain_identifier_vs_length[mail_key]["ids"].append([mail['_id']])
    return chain_identifier_vs_length

#This function recieves a file iterator and gets information of the file\
#using the function "chain_info_from_file(file)" . it holds a maximum value \
#and compares each chain's length to it
def find_longest_chain(file):
    chain_identifier_vs_length = chain_info_from_file(file)
    max = 1
    longest_chain = []
    for identifier in chain_identifier_vs_length:
        if chain_identifier_vs_length[identifier]["length"] > max:
            max = chain_identifier_vs_length[identifier]["length"]
            longest_chain = [chain_identifier_vs_length[identifier]]
        elif chain_identifier_vs_length[identifier]["length"] == max:
            longest_chain.append\
                (chain_identifier_vs_length[identifier]["length"])
    return longest_chain

file = open("enron.json")
print(find_longest_chain(file))
file.seek(0)
file.close()
