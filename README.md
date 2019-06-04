# finding_enron_longest_chain
An algorithm to find the longest chain of emails senders and receivers in the Enron DB

The first step for this task is to parse the file data into a data structure which will be easier to work. 
I parsed each mail (each row in the data) with ‘json’ package which allows to get a representing dictionary for each mail. 
For example, the first email looks like this:

{'_id': {'$oid': '52af48b6d55148fa0c199a2a'},
 'sender': 'counciloftheamericas@as-coa.org',
 'recipients': ['klay@enron.com'],
 'cc': [],
 'text': 'Call-in Program for Council of the Americas members only\n\nHon. Anthony S. Harrington\nU.S. Ambassador to Brazil\nFriday, October 27, 2000\n12:30 - 1:30 p.m. (EDT)\n\n - ccharringtonann.doc', 'mid': '22375148.1075840218447.JavaMail.evans@thyme',
 'fpath': 'enron_mail_20110402/maildir/lay-k/all_documents/650.',
 'bcc': [], 
'to': ['klay@enron.com'],
 'replyto': None,
 'ctype': 'text/plain;
 charset=us-ascii', 
'fname': '650.', 
'date': '2000-10-24 01:20:00-07:00',
 'folder': 'all_documents',
 'subject': 'Call-in Program - Amb. Harrington'}
 
Now, in order to find the longest chain of emails, I thought about different ways of solving this question:

Option 1: for each email, iterate rest of emails and decide (according to the keys: subject, sender, recipients),
if they belong to the same chain. Memory will be very cheap but running time will be n^2  in the worst case, 
so I decided to keep thinking and find another options.

Option 2: Sort the data according to subject (including ‘re’ so that the entire chain will be ordered together after sorting),
in n(log(n)) running time, and then iterate the file only once (O(n)) so that the final running complexity will be O(n(log(n))). 
This solution may not be so good because when given larger datasets the sorting may demand to much memory. 

Option 3(The chosen one): Iterate the file once, and use a dictionary with a key of a string, 
made from subject + sorted names of sender and all recipients. 
This creates an identifier for each conversation between a group of people. Run time is O(n).

Assumptions: 
At first I assumed that it would be very rare to have the same identifier for two different  chains of emails. For this to happen, 
two different chains of emails must have same participants and same subject. So when choosing “subject” and “participants” 
(a sorted list I created combining the sender and recipients), I allowed myself to remove “Re:” from mails subjects, 
to make the analysis more simple and aesthetic. But I found out, after some qa I  did to my results, 
that is some cases it does happen that two different chains have same identifier. It happens, for example, 
when commercials or security messages are sent weekly to the same user. In one case I noticed, 
a user recieved 14 different emails from same sender, containing same subject, 
and mistakenly they were analysed as a chain of 14 messages. (Even though, theoretically, 
some people I talked to thought that sending same subject emails to same group of people can be thought as a single big chain).

At this point, I changed the code and now it actually verifies that subjects with “Re:” only are analysed as messages in chain. 
This way, we “lose” the first message in the list, but we simply start counting from 2, 
and I can later add a few lines of code to add the first message withou “Re:” to the list.
I assume that when replying to an email, one cannot change the subject. 
Which means if the first email in the chain’s subject is “Hey mate” then the reply email must have the subject “Re:  Hey mate”.

Another assumption I made is that if a certain group of people started a conversation, 
and reply was send to only a part of the original group, then I call it another chain. 
For example if Yoav sends a message to Alma and Maya, and Maya sends her Re only to Yoav, 
and then Yoav replies only to Maya – Then I call it 2 different chains. 

def generate_key(email):
This function, “generate_key(email)” receives a dictionary representing a single email and generates an identifier key for this email.  It returns an identification string for an email.
For instance, they key generated for mail '52af48b6d55148fa0c1996a7' is:
“Enron Advisory Council rosalee.fleming@enron.com stelzer@aol.com”

def chain_info_from_file(file):
This function iterates the file, returns the "chain_identifier_vs_length” dictionary. This dictionary has a chain identification as key (the return value of  "generate_key(email)" , and has another dictionary as a value. The value dictionary has info length of chain(“length”) and ids of the messages involved in this chain(“ids”).
Output of this function on the given data (only one out of many): 
Re: EXECUTIVE COMMITTEE MEETINGS - MONDAY, JANUARY 17 rosalee.fleming@enron.com sherri.reinartz@enron.com {'length': 4, 'ids': [{'$oid': '52af48b5d55148fa0c199643'}, [{'$oid': '52af48b6d55148fa0c19995a'}], [{'$oid': '52af48b7d55148fa0c19aca8'}]]}
So we can understand from this output than the subject of this chain of emails is “EXECUTIVE COMMITTEE MEETINGS - MONDAY, JANUARY 17”, the chain’s participants are rosalee.fleming@enron.com and  sherri.reinartz@enron.com, and they replaced the messages with ids of: '52af48b5d55148fa0c199643', '52af48b6d55148fa0c19995a', '52af48b7d55148fa0c19aca8'.

def find_longest_chain(file):
This function receives a file iterator and gets information of the file using the function "chain_info_from_file(file)" . it holds a maximum value  and compares each chain's length to it, and replacing or adding (in case of few equal maximum lengths chains) according to the case.
The call for this function is the only command (other than imports and file open and close) that runs outside of a function in my code. It activates the other functions mentioned above.
The output for this function on our data is :
[{'length': 13, 'ids': [{'$oid': '52af48b6d55148fa0c19966b'}, [{'$oid': '52af48b6d55148fa0c199671'}], [{'$oid': '52af48b6d55148fa0c199675'}], [{'$oid': '52af48b6d55148fa0c19990f'}], [{'$oid': '52af48b6d55148fa0c199931'}], [{'$oid': '52af48b6d55148fa0c199958'}], [{'$oid': '52af48b6d55148fa0c19a0ea'}], [{'$oid': '52af48b6d55148fa0c19a10c'}], [{'$oid': '52af48b6d55148fa0c19a10d'}], [{'$oid': '52af48b7d55148fa0c19ad12'}], [{'$oid': '52af48b7d55148fa0c19ad17'}], [{'$oid': '52af48b7d55148fa0c19ad1c'}]]}]
So this is the longest chain of messages within the exact same group of people,  it is 13 emails long and all emails are between   rosalee.fleming@enron.com  and  mtelle@velaw.com   under the subject : "Re: Referendum Campaign".
