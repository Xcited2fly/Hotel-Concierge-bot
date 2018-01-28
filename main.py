from tkinter import *
from nltk import word_tokenize
import yaml
from csv import writer
import json
from copy import copy
#create tkinter 
tk=Tk()
tk.configure(background='orange')
tk.title("CONCIERGE CHATBOT")
tk.geometry('600x400')
#initialize global variables
name,tokens="",""
ctr,total=0,1
reply=[]
pos=0
def greet():
    #function for all types of greetings
    global name,tokens,ctr,t,total
    greetings=['hi','hii','hello','wassup','suup','yoo']
    for i in range(len(tokens)):
        for j in range(len(greetings)):
            if tokens[i]==greetings[j]:
                name=e1.get()
                if name!='bye':
                    s=name[0]
                    s=s.upper()
                    name=s+name[1:]
                    ctr=1
                    rep=("How can I help you %s?"%name)
                    l2.configure(text=rep)
                    total=1
                else:
                    t=False
                    break
def address():
    #function to reply for all enquiries about address and directions 
    global total
    if 'reach' in tokens or 'address' in tokens or 'directions' in tokens or ("where" in tokens and "hotel" in tokens):
        rep=("The ABC International hotel\nRoad no- 9, behind RBI, Janakpuri,\nJaipur-302021\n\nThe city is well connected with roads.\nNearest railway station is Jaipur junction.\nNearest airport is Jaipur International Airport.")
        l2.configure(text=rep)
        total=1

def password():
    #function to access wifi password from a password.yml file and give it to user
    global tokens,total
    if 'wifi' in tokens:
        if 'password' in tokens:
            with open("password.yml",'r') as stream:
                d=yaml.load(stream)
            rep=("the wifi password is : %s\nFell free to ask anything about our services!"%d['password'])
            l2.configure(text=rep)
            total=1

def save():
    #function to save all the unattended queries of a user in a output.csv file 
    reply1=[[]]*1
    for i in range(len(reply)):
        reply1.append(reply[i])
    with open("output.csv","w") as file:
        f=writer(file,dialect='excel')
        f.writerow(reply1)
def check_room_availability():
    #function to check for availability of rooms in a given date. The data is fetched from data.json file where it has data of all days in January 2018
    global total,tokens
    f,pos=0,0
    for index,i in enumerate(tokens):
        for j in range(10):
            if i[0].isdigit() and f==0:
                for k in range(10):
                    if i[1].isdigit():
                        day=int(i[0:2])
                        pos=copy(index)
                        f=1
                    else:
                        day=int(i[1])
                        pos=copy(index)
                        f=1
    if f==1:
        year=int(tokens[pos+2])
        months={' ':0,'jan':1,'january':1,'feb':2,'february':2,'mar':3,'march':3,'april':4,'apr':4,'may':5,'june':6,'jun':7,'july':7,'jul':8,'august':9,'aug':9,'september':10,'sep':10,'october':11,'oct':11,'november':11,'nov':11,'december':12,'dec':12}
        for m in months:
            if m==tokens[pos+1]:
                month=months["%s"%m]
        days=[0,31,28,31,30,31,30,31,31,30,31,30,31]
        if year%4==0:
            days[2]=29
        total=1
        
        if month>0 and month<=12:
            if day>0 and day<=days[month]:
                with open('data.json','r') as fp:
                    data=json.load(fp)
                    check=data.get('%s'%year,{}).get('%s'%month,{}).get('%s'%day)
                    if check=='available':
                        rep=("Yes\nFor booking log on to www.ABChotels.com/bookings.html")
                        l2.configure(text=rep)
                    else:
                        rep=("Sorry, we are out of rooms at this date.")
                        l2.configure(text=rep)
            else:
                rep=("Enter valid date")
                l2.configure(text=rep)
        else:
            rep=("Enter valid date.")
            l2.configure(text=rep)

def booking():
    #function to reply for queries about bookings
    global total
    if 'booking' in tokens or 'reservations' in tokens:
        rep=("Goto www.ABChotels.com/booking.html\nTo check availability kindly type the date in dd 'month name' yyyy format.")
        l2.configure(text=rep)
        total=1

def contact():
    #function to reply for all queries about how to contact the hotel
    global total
    if 'contact' in tokens or 'phone' in tokens or 'email' in tokens or 'landline' in tokens or 'mobile' in tokens:
        rep=("Phone no.- 9123456789\nLandline.- 0326-8756535\nE-mail: abchotels@mail.com")
        l2.configure(text=rep)
        total=1

def services():
    #function to reply for queries about services
    global total
    if 'service' in tokens or 'services' in tokens:
        rep=("We offer many services. Some of them include\n1. Free Parking\n2. High speed WiFi\n3. Fitness Centre\n4. Pool\n5. Restaurant\n6. Dry cleaning\n7. Multilingual staff\n8. Laundry service\n9. Room service")
        l2.configure(text=rep)
        total=1
def package():
    #function to reply for all queries about packages
    global total
    if 'package' in tokens or 'offers' in tokens or 'payment' in tokens:
        rep=("Single bed : Rs. 2000/night\nDouble bed : Rs. 4000/night\nAll exclusive of taxes. \nFor more details log on to www.ABChotels.com/package.html")
        l2.configure(text=rep)
        total=1
def a():
    #this function makes all the calls for the enquiries 
    global pos,tokens,total
    n=e.get()
    pos+=1
    total=0
    N=n.lower()
    tokens=word_tokenize(N)
    if n=='bye':
        save()
        tk.destroy()
    else:
        if ctr==0:
            greet()
        address()
        password()
        booking()
        contact()
        services()
        check_room_availability()
        package()
        if total==0:
            rep=("Sorry, I did't get that. Please say that again %s."%name)
            l2.configure(text=rep)
            reply.append(n)

#placing of tkinter widgets - labels,button,entry
l8=Label(tk,text="Greetings.\nI am your hotel concierge from ABC International.\nHow can I help you?\nType 'bye' to exit.",bg="red",font="Times 15 bold")
l8.pack()
l1=Label(tk,text="Type your name :",bg="red")
l1.pack()
e1=Entry(tk)
e1.pack()
l=Label(tk,text="Reply :",bg="red")
l.pack()
e=Entry(tk)
e.pack()
b=Button(tk,text="Enter",command=a,bg="light blue",activebackground="red",bd=4)
b.pack()
l2=Label(tk,text="",bg="red")
l2.pack()
tk.mainloop()
