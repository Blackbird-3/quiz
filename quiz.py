import random  
import sys  
import mysql.connector  
import ctypes  
from datetime import datetime  
  
subject_options=[]  
  
  
#function to perform registration of new user  
def register():  
    print()  
    uname=str(input("Please enter username:")).strip().lower()  
  
    acursor.execute("select username from users")  
  
    ucode=acursor.rowcount+1  
      
    usernames=[item[0] for item in acursor.fetchall()]  
  
    if uname in usernames:  
        print("Username already taken")  
        register()  
         
    else:  
        name=str(input("Please enter your name:")).strip()  
        upwd=str(input("Please enter password:")).strip()  
        #check password  
  
        acursor.execute("select ucode from users")  
          
        acursor.fetchall()  
        admin='0'  
        if ucode==1:  
            admin='1'  
  
        acursor.execute("insert into users values ("+str(ucode)+",'"+name+"','"+uname+"','"+upwd+"',"+admin+")")  
        adb.commit()  
        print("Welcome",name,". You are now registered.")  
  
          
#main menu to select login or registration      
def loginmenu():  
    while True:  
        print()  
        print(75*"-")  
        print("Choose your option")  
        print("1: Login")  
        print("2: Register")  
        print("0: Exit")  
        user=str(input("Enter your choice: ")).strip()  
              
        if user=="1":  
            print()  
            uname=str(input("Please enter username:")).strip().lower()  
            upwd=str(input("Please enter password:")).strip()  
  
            acursor.execute("select * from users")  
            use1=acursor.fetchall()  
  
            use_rec1={}  
            for r in use1:  
                use_rec1[r[2]]=r[3]  
  
            if uname in use_rec1:  
                if use_rec1[uname]==upwd:  
                    use_rec2={}  
                    for r in use1:  
                        use_rec2[r[2]]=r[1]  
                    User_name=use_rec2[uname]  
  
                    use_rec3={}  
                    for r in use1:  
                        use_rec3[r[2]]=r[0]  
                    User_code=use_rec3[uname]  
  
                    use_rec4={}  
                    for r in use1:  
                        use_rec4[r[2]]=r[4]  
                    User_admin=use_rec4[uname]  
                    print()  
                    print("Welcome "+User_name)  
                    while mainmenu(User_code,User_name,User_admin):  
                        print()  
                else:  
                    print("Invalid credentials entered")  
                    loginmenu()  
            else:  
                print("Invalid credentials entered")  
                loginmenu()  
                  
        elif user=="2":  
            register()  
        elif user=="0":  
            print("Goodbye.")  
            sys.exit()  
        else:  
            print()  
            print("Invalid Option Entered")  
  
  
#function for changing password of the current user  
def password(User_code):  
    while True:  
        print()  
        acursor.execute("select password from users where ucode="+str(User_code))  
        a=acursor.fetchall()  
        currentpass=a[0][0]  
        current=str(input("Please enter your current password:")).strip()  
        print()  
        if current==currentpass:  
            new=str(input("Please enter new password:"))  
            while True:  
                print("Are you sure, you want to change your password?")  
                print("Y: Yes")  
                print("N: No")  
                sure=str(input("Enter your choice: ")).strip().lower()  
                print()  
                if sure=='y':  
                    while True:  
                        print()  
                        renew=str(input("Please re-enter new password:"))  
                        if new==renew:  
                            acursor.execute("update users set password='"+new+"' where ucode="+str(User_code))  
                            adb.commit()  
                            print()  
                            print("Password successfully changed.")  
                            input("Press enter to continue...")  
                            return  
                        else:  
                            print()  
                            print("Entered passwords don't match")  
                elif sure=='n':  
                    print("Ignoring the password change request")  
                    input("Press enter to continue...")  
                    return  
                else:  
                    print("Invalid option entered")  
        else:  
            print("Incorrect password entered")  
            while True:  
                print("Do you really want to change your password?")  
                print("Y: Yes")  
                print("N: No")  
                really=str(input("Enter your choice: ")).strip().lower()  
                if really=="y":  
                    break  
                elif really=="n":  
                    return  
                else:  
                    print("Invalid option entered")  
  
  
  
#main menu for logged in user  
def mainmenu(User_code,User_name,User_admin):  
    print()  
    print(75*"-")  
    print("MAIN MENU")  
    print()  
    print("1: Take quiz")  
    print("2: View past result")  
    print("3: Change password")  
    print("4: Back to main menu")  
    if User_admin==1:  
        print("5: Go to Admin menu")  
    print("0: Exit program")  
    menuopt=str(input("Enter your choice:")).strip()  
  
    if menuopt=="1":  
        print()  
        menu1(User_code,User_name)  
    elif menuopt=="2":  
        print()  
        result(User_code,User_name)  
  
    elif menuopt=="3":  
        print()  
        password(User_code)  
  
    elif menuopt=="4":  
        print()  
        print("Thank you for playing")  
        loginmenu()  
    elif User_admin==1 and menuopt=="5":  
        adminmenu(User_code)  
    elif menuopt=="0":  
        print()  
        print("Thank you for playing")  
        sys.exit()  
    else:  
        print("Invalid Option Entered")  
    return True  
          
  
  
#function to add new question in db  
def addsub():  
    print()  
    print("The following Subjects exist in the DB:")  
    for x in subject_records:  
        print(x,": ",subject_records[x])  
    scode=len(subject_records)+1  
    print()  
    newsub=str(input("Enter new subject name:")).strip()  
    new_dict = dict((k, v.lower()) for k, v in subject_records.items())  
    present=newsub.lower() in new_dict.values()  
    if present==True:  
        print("Subject already exists.")  
    elif present==False:  
        while True:  
            print()  
            print("Are you sure, you want to add "+newsub+" to the database?")  
            print("Y: Yes")  
            print("N: No")  
            print()  
            sure=str(input("Enter your choice: ")).strip().lower()  
            if sure=='y':  
                acursor.execute("insert into subjects values ("+str(scode)+",'"+newsub+"')")  
                adb.commit()  
                subject_records[scode]=newsub  
                subject_options.append(str(len(subject_records)))  
                print(newsub,"successfully added to the database")  
                input("Press enter to continue...")  
                return  
            elif sure=='n':  
                print()  
                print("Ignoring the subject addition")  
                input("Press enter to continue...")  
                return  
            else:  
                print("Invalid option entered")  
                      
  
  
#function to add new question in db  
def addq():  
    while True:  
        for x in subject_records:  
            print(x,": ",subject_records[x])  
        print()      
        scode=str(input("Enter your choice of Subject:")).strip()  
        print()  
        newq=str(input("Enter new question:"))  
        opt1=str(input("Enter option 1:"))  
        opt2=str(input("Enter option 2:"))  
        opt3=str(input("Enter option 3:"))  
        opt4=str(input("Enter option 4:"))  
        ans=str(input("Enter option for answer(1/2/3/4):"))  
        acursor.execute("select qcode from quiz_bank")  
        rows=acursor.rowcount  
        qcode=rows+1  
        while True:  
            print()  
            print("Are you sure, you want to add this question to the database?")  
            print("Y: Yes")  
            print("N: No")  
            print()  
            sure=str(input("Enter your choice: ")).strip().lower()  
            if sure=='y':  
                acursor.execute("insert into quiz_bank values ("+str(qcode)+",'"+scode+"','"+newq+"','"+opt1+"','"+opt2+"','"+opt3+"','"+opt4+"','"+ans+"')")  
                adb.commit()  
                print("New question successfully added to the database.")  
                input("Press enter to continue...")  
                break  
            elif sure=='n':  
                print("Ignoring the question addition")  
                input("Press enter to continue...")  
                return  
            else:  
                print("Invalid option entered")  
        print("Add more?")  
        print("1: Yes")  
        print("2: No")  
        print()  
        addmore=str(input("Enter your choice:")).strip()  
        if addmore=="1":  
            print()  
        elif addmore=="2":  
            return  
        else:  
            print()  
            print("Invalid option entered")  
  
#function to make normal user admin  
def makead(User_code):  
    acursor.execute("select ucode, username, name from users where admin=0 and ucode<>"+str(User_code))  
    people=acursor.fetchall()  
    options=[]  
    x=1  
    print("Current non-admin users are:-")  
    for r in people:  
        print(x,":","username:",r[1],"-->",r[2])  
        options.append(str(x))  
        x+=1  
    print()  
    print("0 : Back to admin menu")  
    options.append(str(0))  
    while True:  
        print()  
        ad=str(input("Enter option to make admin or 0 to exit: ")).strip()  
        if ad in options:  
            if ad=="0":  
                return  
            ch=int(ad)  
            while True:  
                print()  
                print("Please confirm if you want to make "+people[ch-1][2]+" an admin?")  
                print("Y: Yes")  
                print("N: No")  
                print()  
                sure=str(input("Enter your choice: ")).strip().lower()  
                print()  
                if sure=='y':  
                    acursor.execute("update users set admin=1 where ucode="+str(people[ch-1][0]))  
                    adb.commit()  
                    print(str(people[ch-1][2]),"is now an admin")  
                    input("Press enter to continue...")  
                    return  
                elif sure=='n':  
                    print()  
                    print("Ignoring the admin change")  
                    input("Press enter to continue...")  
                    return  
                else:  
                    print()  
                    print("Invalid option entered")  
                    print()  
  
        else:  
            print("Invalid Input")  
            print()  
      
  
#function to remove admin credentials of admin user  
def removead(User_code):  
    acursor.execute("select ucode, username, name from users where admin=1 and ucode<>"+str(User_code))  
    people=acursor.fetchall()  
    options=[]  
    x=1  
    print("Current admins are:-")  
    for r in people:  
        print(x,":","username:",r[1],"-->",r[2])  
        options.append(str(x))  
        x+=1  
    print()  
    print("0 : Back to admin menu")  
    options.append(str(0))  
    while True:  
        print()  
        ad=str(input("Enter option to remove admin or 0 to exit: ")).strip()  
        if ad in options:  
            if ad=="0":  
                return  
            ch=int(ad)  
            while True:  
                print()  
                print("Please confirm if you want to remove "+people[ch-1][2]+" as an admin?")  
                print("Y: Yes")  
                print("N: No")  
                print()  
                sure=str(input("Enter your choice: ")).strip().lower()  
                print()  
                if sure=='y':  
                    acursor.execute("update users set admin=0 where ucode="+str(people[ch-1][0]))  
                    adb.commit()  
                    print(str(people[ch-1][2]),"is now no longer an admin")  
                    input("Press enter to continue...")  
                    return  
                elif sure=='n':  
                    print()  
                    print("Ignoring the admin change")  
                    input("Press enter to continue...")  
                    return  
                else:  
                    print()  
                    print("Invalid option entered")  
                    print()  
  
        else:  
            print("Invalid Input")  
            print()  
  
#admin menu option to check result of any user  
def checkuserresult(User_code):  
    acursor.execute("select ucode, username, name from users")  
    people=acursor.fetchall()  
    options=[]  
    x=1  
    print("List of users:")  
    for r in people:  
        print(x,":","username:",r[1],"-->",r[2])  
        options.append(str(x))  
        x+=1  
    print()  
    print("0 : Back to admin menu")  
    options.append(str(0))  
    while True:  
        print()  
        ad=str(input("Select user to view result: ")).strip()  
        if ad in options:  
            if ad=="0":  
                return  
            ch=int(ad)  
            result(people[ch-1][0],people[ch-1][2])  
            x=1  
            print()  
            print("List of users:")  
            for r in people:  
                print(x,":","username:",r[1],"-->",r[2])  
                x+=1  
            print()  
            print("0 : Back to admin menu")  
              
        else:  
            print("Invalid Input")  
            print()  
  
#admin menu option to check result of any subject  
def checksubjectresult():  
    while True:  
        print()  
        print(75*"-")  
        for x in subject_records:  
            print(x,": ",subject_records[x])  
  
        print("0 :  Exit")  
        print()  
          
        scode=str(input("Select a Subject to view Result Summary:")).strip()  
          
        if scode=="0":  
            print()  
            return   
        elif scode in subject_options:  
            acursor.execute("select name, sum(score), sum(max), count(date) from users, results where scode="+scode+" and users.ucode=results.ucode group by name order by name")  
            if acursor.rowcount==0:  
                print("No one has attempted any quiz in this subject")  
            else:  
                people=acursor.fetchall()  
  
                print(75*"-")  
                print("Result Summary for: ",subject_records[int(scode)])  
                print(75*"-")  
                print("Name".ljust(53)[:53],"No. of Quiz  Score")  
                print(75*"-")  
                sumscore=0  
                summax=0  
                squiz=0  
                for r in people:  
                    print(r[0].ljust(59)[:59],str(r[3]).ljust(6)[:6],str(round(r[1]/r[2]*100,2)).rjust(6),"%")  
                    sumscore+=r[1]  
                    summax+=r[2]  
                    squiz+=r[3]  
  
                print(75*"-")  
                print("Overall Summary".ljust(59)[:59],str(squiz).ljust(6)[:6],str(round(sumscore/summax*100,2)).rjust(6),"%")  
                print(75*"-")  
                print()  
                input("Press enter to continue...")  
              
        else:  
            print("Invalid Option Entered")  
  
def split(word):   
    return [char for char in word]  
  
#admin menu option to check graph of subject  
def checksubjectgraph():  
    while True:  
        print()  
        print(75*"-")  
        for x in subject_records:  
            print(x,": ",subject_records[x])  
  
        print("0 :  Exit")  
        print()  
          
        scode=str(input("Select a Subject to view Results Graph:")).strip()  
          
        if scode=="0":  
            print()  
            return   
        elif scode in subject_options:  
            acursor.execute("select name, sum(score), sum(max), count(date) from users, results where scode="+scode+" and users.ucode=results.ucode group by name order by name")  
            if acursor.rowcount==0:  
                print("No one has attempted any quiz in this subject")  
            else:  
                people=acursor.fetchall()  
      
                glen=len(people)*3+3  
                ustr=""  
                for r in range(len(people)):  
                    ustr=ustr+str(r+1).rjust(3)[:3]  
  
                gstr=[]  
                gstr.append(split("     | "+glen*" "))  
                gstr.append(split("100% | "+glen*" "))  
                gstr.append(split("     | "+glen*" "))  
                gstr.append(split(" 80% | "+glen*" "))  
                gstr.append(split("     | "+glen*" "))  
                gstr.append(split(" 60% | "+glen*" "))  
                gstr.append(split("     | "+glen*" "))  
                gstr.append(split(" 40% | "+glen*" "))  
                gstr.append(split("     | "+glen*" "))  
                gstr.append(split(" 20% | "+glen*" "))  
                gstr.append(split("     |"+glen*"_"))  
                gstr.append(split("  0%  "+ustr))  
  
                i=1  
                for r in people:  
                    s=int(round(r[1]/r[2]*100,-1))  
                    x=10  
                    j=10  
  
                    while x<=s:  
                        gstr[j][5+(i*3)]="█"  
                        j-=1  
                        x+=10  
                    i+=1  
                      
                for line in gstr:  
                    print("".join(line))  
                      
                print(75*"-")  
                print("Result Summary for: ",subject_records[int(scode)])  
                print(75*"-")  
                print(" # Name".ljust(53)[:53],"No. of Quiz  Score")  
                print(75*"-")  
                sumscore=0  
                summax=0  
                squiz=0  
                i=1  
                for r in people:  
                    print(str(i).rjust(2)[:2],r[0].ljust(56)[:56],str(r[3]).ljust(6)[:6],str(round(r[1]/r[2]*100,2)).rjust(6),"%")  
                    sumscore+=r[1]  
                    summax+=r[2]  
                    squiz+=r[3]  
                    i+=1  
  
                print(75*"-")  
                print("Overall Summary".ljust(59)[:59],str(squiz).ljust(6)[:6],str(round(sumscore/summax*100,2)).rjust(6),"%")  
                print(75*"-")  
                print()  
                input("Press enter to continue...")  
              
        else:  
            print("Invalid Option Entered")  
  
#admin menu option to set number of questions  
def qno():  
    acursor.execute("select noofques from config")  
    current=acursor.fetchall()[0][0]      
    print("Current number of questions are:",current)  
    while True:  
        print()  
        new=int(input("Enter new number of questions (between 1 and 20): "))  
        if new in range(1,21):  
            acursor.execute("update config set noofques="+str(new))  
            adb.commit()  
            print("Number of questions updated.")  
            input("Press enter to continue...")  
            print()  
            return  
        else:  
            print("Invalid value entered")  
          
         
  
      
#admin menu to add question, subjects, set no of questions in the quiz and manage admin rights  
def adminmenu(User_code):  
    while True:  
        print(75*"-")  
        print("ADMIN MENU")  
        print()  
        print("1: Add new subject")  
        print("2: Add new question")  
        print("3: Make admin")  
        print("4: Remove admin")  
        print("5: Set number of questions")  
        print("6: Check user result")  
        print("7: Check subject result")  
        print("8: Check subject graph")  
        print("0: Exit")  
        admenuopt=str(input("Enter your choice:")).strip()  
        print()  
          
        if admenuopt=="1":  
            addsub()  
        elif admenuopt=="2":  
            addq()  
        elif admenuopt=="3":  
            makead(User_code)  
        elif admenuopt=="4":  
            removead(User_code)  
        elif admenuopt=="5":  
            qno()  
        elif admenuopt=="6":  
            checkuserresult(User_code)  
        elif admenuopt=="7":  
            checksubjectresult()  
        elif admenuopt=="8":  
            checksubjectgraph()  
        elif admenuopt=="0":  
            return  
        else:  
            print("Invalid Option Entered")  
  
  
  
#menu for subject selection when taking quiz  
def menu1(User_code,User_name):  
    print(75*"-")  
  
    for x in subject_records:  
        print(x,": ",subject_records[x])  
  
    print("0 :  Exit")  
    print()  
      
    scode=str(input("Enter your choice of Subject:")).strip()  
      
    if scode=="0":  
        print()  
          
        return False  
    elif scode in subject_options:  
        print("You have selected: ",subject_records[int(scode)])  
        print()  
        print()  
        quiz(scode,User_code,User_name)  
    else:  
        print("Invalid Option Entered")  
  
#function to take quiz of selected subject  
def quiz(scode,User_code,User_name):  
    qdb=mysql.connector.connect(host="localhost",user="root",passwd="shreshth", database="quiz_project")  
    qcursor=qdb.cursor(buffered=True)  
    qcursor.execute("select * from config")  
    noofques=[item[0] for item in qcursor.fetchall()][0]  
  
    qcursor.execute("select * from quiz_bank where scode="+scode)  
  
    if qcursor.rowcount==0:  
        print("Question bank for this subject is empty")  
        return   
    elif qcursor.rowcount<noofques:  
        noofques=qcursor.rowcount  
      
    quelist=qcursor.fetchall()  
    finalques=random.sample(quelist,noofques)  
      
    global marks  
    marks=0  
    a=1  
    response=''  
    for x in finalques:  
        print("Q"+str(a)+": "+x[2])  
        print("    1: ",x[3])  
        print("    2: ",x[4])  
        print("    3: ",x[5])  
        print("    4: ",x[6])  
  
        while response not in ['1','2','3','4']:  
            response=str(input("Enter option number:")).strip()  
            if response not in ['1','2','3','4']:  
                print("This is not a valid option")  
                  
        if response==str(x[7]):  
            print("Your answer is correct")  
            marks+=1  
        else:  
            print("Sorry, your answer is incorrect.","Correct option was:",x[7])  
        a+=1  
        response=''  
        print()  
        print(75*"-")  
  
    print()  
    print("Your Quiz Score:")  
    if marks==noofques:  
        print("Congratulations! You got a perfect score!", marks,"out of", noofques)  
    elif marks==0:  
        print("Sorry... you did not get any questions right.")  
    elif marks>=noofques*0.4:  
        print("Congratulations! You got", marks,"out of", noofques)  
    else:  
        print("You only got", marks,"out of", noofques)  
  
  
    now = datetime.now()  
    date_time = now.strftime("%Y%m%d%H%M%S")  
      
  
    qcursor.execute("insert into results values ("+str(User_code)+","+scode+","+str(marks)+","+str(noofques)+","+date_time+")")  
    qdb.commit()  
    qcursor.close()  
    qdb.close()  
    input("Press enter to continue...")  
  
      
          
#function to display past results of user by subject  
def result(User_code,User_name):  
    rdb=mysql.connector.connect(host="localhost",user="root",passwd="shreshth", database="quiz_project")  
    rcursor=rdb.cursor()  
    query="select name, score, max, date from results, subjects where ucode="+str(User_code)+" and subjects.scode=results.scode order by name, date"  
    rcursor.execute(query)  
    recs=rcursor.fetchall()  
  
    print(75*"-")  
    if len(recs)==0:  
        print(str(User_name)+" has not attempted any quizzes.")  
    else:  
        sub=""  
        print("Following are the scores of: "+User_name)  
        oscore=0  
        omax=0  
        oquiz=0  
        for r in recs:  
            subject=r[0]  
            if subject!=sub:  
                if sub!='':  
                    print("Summary of",sub,": Quizzes attempted:",squiz,"   Subject result:",round(sumscore/summax*100,2),"%")  
                print()  
                print("Subject: "+subject)  
                print()  
                sumscore=0  
                summax=0  
                squiz=0  
                sub=subject  
                  
            score=r[1]  
            maximum=r[2]  
            dt=r[3]  
            sumscore+=score  
            summax+=maximum  
            squiz+=1  
            oscore+=score  
            omax+=maximum  
            oquiz+=1  
            print("Result on",dt.strftime("%c"),":",score,"out of",maximum,"      :",round(score/maximum*100,2),"%")  
  
        print("Summary of",subject,": Quizzes attempted:",squiz,"   Subject result:",round(sumscore/summax*100,2),"%")  
  
        print()  
        print("Overall Summary: Quizzes attempted:",oquiz,"   Overall result:",round(oscore/omax*100,2),"%")  
    print()  
    input("Press enter to continue...")  
  
    rcursor.close()  
    rdb.close()  
  
  
  
#main program  
mydb=mysql.connector.connect(host="localhost",user="root",passwd="shreshth", database="quiz_project")  
mycursor=mydb.cursor()  
mycursor.execute("select * from subjects")  
recs=mycursor.fetchall()  
mycursor.close()  
mydb.close()  
  
subject_records= {}  
for r in recs:  
    subject_records[r[0]]=r[1]  
    subject_options.append(str(r[0]))  
  
subject_options.append(str(0))  
  
adb=mysql.connector.connect(host="localhost",user="root",passwd="shreshth", database="quiz_project")  
acursor=adb.cursor(buffered=True)  
  
while True:  
    print()  
    print()  
    print("                   ______             ____     ___               ______")  
    print("\              /  |        |         /        /   \   |\    /|  |      ")  
    print(" \            /   |        |        /        /     \  | \  / |  |      ")  
    print("  \    /\    /    |------  |       |        |       | |  \/  |  |------")  
    print("   \  /  \  /     |        |        \        \     /  |      |  |      ")  
    print("    \/    \/      |______  |______   \_____   \___/   |      |  |______")  
    print()  
    loginmenu()  
  
