# -*- coding: cp936 -*-
#���ߣ������� ѧ�ţ�5110309074
from string import *
from random import *
from graphics import *
from button import *

familyname=['��','Ǯ','��','��','��','��','֣','��']
debug=0


class problem_type:
    def __init__(self):
        self.problem=''
        self.choice=[]
        self.answer=''

    def set_problem(self,a):
        self.problem=a

    def add_choice(self,a):
        self.choice.append(a)

    def set_answer(self,a):
        a=replace(a,' ','')
        self.answer=a

    def get_question(self):
        return self.problem

    def get_choice(self):
        return self.choice

    def get_answer(self):
        return self.answer

    def answer_question(self,ans):
        return ans==self.answer

class problem_set:
    def __init__(self,database):
        self.total=0
        self.problemlist=[]
        self.decision=[]

        while(True):
            line=database.readline()
            line=replace(line,'\n','')
            if(line==""):break
 
            p=problem_type()
            p.set_problem(line)
            for i in range(4):
                line=database.readline()
                line=replace(line,'\n','')
                p.add_choice(line)
            line=database.readline()
            line=replace(line,'\n','')
            p.set_answer(line)

            self.total+=1
            self.problemlist.append(p)

        for i in range(self.total):
            self.decision.append(i)
        for i in range(1000):
            pos1=randrange(0,self.total)
            pos2=randrange(0,self.total)
            temp=self.decision[pos1]
            self.decision[pos1]=self.decision[pos2]
            self.decision[pos2]=temp
            
    def get_kth_question(self,k):
        return self.problemlist[self.decision[k]].get_question()
    
    def get_kth_choice(self,k):
        return self.problemlist[self.decision[k]].get_choice()

    def get_kth_answer(self,k):
        return self.problemlist[self.decision[k]].get_answer()
    
    def answer_kth_question(self,k,a):
        return self.problemlist[self.decision[k]].answer_question(a)


class interface:
    def __init__(self):
        fin=open("database.txt","r")
        self.ps=problem_set(fin)
        
        self.win=GraphWin(title=u'Ȥζ�ʴ�',width=800,height=600)

        self.times=[99999,1,1,1,1]
        if(debug):self.times=[99999,99999,99999,99999,99999]

        self.but=[]
        
        self.but.append(Button(self.win,Point(60,200),70,30,u"�ش�����"))
        self.but.append(Button(self.win,Point(60,250),70,30,u"������"))
        self.but.append(Button(self.win,Point(60,300),70,30,u"��·��"))
        self.but.append(Button(self.win,Point(60,350),70,30,u"50%����"))
        self.but.append(Button(self.win,Point(60,400),70,30,u"��������"))

        self.but.append(Button(self.win,Point(300,550),50,30,"A"))
        self.but.append(Button(self.win,Point(400,550),50,30,"B"))
        self.but.append(Button(self.win,Point(500,550),50,30,"C"))
        self.but.append(Button(self.win,Point(600,550),50,30,"D"))

        self.split_line=Line(Point(120,0),Point(120,800))
        self.split_line.draw(self.win)
        
        self.label=Text(Point(450,50),u"��ӭʹ�� Ȥζ�ʴ�-���԰�")
        self.label.draw(self.win)

        self.box=Text(Point(450,150),u"����˴�����")
        self.box.draw(self.win)

        self.P=''
        self.A=''
        self.S=''
        self.C=[]
        
        self.win.getMouse()        

    def game_over(self):
        self.win.close()

    def show_button(self):
        for j in range(5):
            if self.times[j]>0:
                self.but[j].activate()
            else:
                self.but[j].deactivate()


    def update_desktop(self,i):
        self.label.setText(unicode('�����ڻش��'+str(1+i)+'��','gb2312'))
        self.box.setText('')

    def get_info(self,i):
        self.P=self.ps.get_kth_question(i)
        self.C=self.ps.get_kth_choice(i)
        self.A=self.ps.get_kth_answer(i)
        self.S=self.P+'\n'
        for j in range(4):
            self.S+=chr(65+j)+'.'+self.C[j]+'\n'
        self.S=unicode(self.S,'gb2312')
        if(debug):self.S+=unicode(self.A,"gb2312")

    def get_command(self):
        p=self.win.getMouse()
        for i in range(9):
            if(self.but[i].clicked(p)):
                return i
        return -1

    def enable_choose(self):
        for i in range(5,9):
            self.but[i].activate()

    def forbid_choose(self):
        for i in range(5,9):
            self.but[i].deactivate()
            
    def show_info(self):
        self.box.setText(self.S)
        self.enable_choose()
        
    def ask_friend(self):
        self.times[1]-=1
        self.forbid_choose()
        level=randrange(1,4)
        name='С'+familyname[randrange(0,8)]
        out=name+':\n'
        if(level==1): out=out+'�������Ѱ���\n'
        if(level==2): out+='������Ҵ��֪����\n'
        if(level==3): out+='�����С��һ����\n'
        out+='��ѡ:'

        if(randrange(0,5)<=level):
            out+=self.A
        else:
            L=['A','B','C','D']
            L.remove(self.A)
            out+=L[randrange(0,3)]

        self.box.setText(unicode(out,'gb2312'))

    def ask_passerby(self):
        t=randrange(0,50)+50
        self.forbid_choose()
        self.times[2]-=1
        left=100-t
        L=[]
        for c in ['A','B','C','D']:
            if(c==self.A):
                L.append(t)
            else:
                tt=randrange(0,left)
                left-=tt
                L.append(tt)
        L[randrange(0,4)]+=left
        out='�����������ʾ������£�\n'
        for c in ['A','B','C','D']:
            out+=c+':  '+str(L.pop(0))+'%\n'
        self.box.setText(unicode(out,'gb2312'))

    def half(self):
        self.forbid_choose()
        self.times[3]-=1
        out='��ȷ������������֮һ��\n'
        l=['A','B','C','D']
        l.remove(self.A)
        ll=[self.A]
        ll.append(l[randrange(0,3)])
        ll.sort()
        out+=ll[0]+'    '+ll[1]+'\n'
        self.box.setText(unicode(out,'gb2312'))

    def fail(self):
        out='��ʧ���ˣ�\n��ȷ���ǣ�'+self.A+':'+self.C[ord(self.A)-65]
        self.box.setText(unicode(out,'gb2312'))
        for i in range(5):
            self.times[i]=0
        for i in range(9):
            self.but[i].deactivate()
        self.win.getMouse()

    def succeed(self):
        out='ͨ�أ�\n'
        self.box.setText(unicode(out,'gb2312'))
        for i in range(5):
            self.times[i]=0
        for i in range(9):
            self.but[i].deactivate()
        self.win.getMouse()
    
    def work(self):
        for i in range(16):
            if(self.times[0]<1):break
            self.update_desktop(i)
            S=self.get_info(i)
            #self.forbid_choose()
            self.show_info()
            while(1):
                self.show_button()
                cmd=self.get_command()
                #print cmd
                #if(debug):self.win.getMouse()
                if(cmd<0):continue
                if(cmd==0):self.show_info()
                if(cmd==1):self.ask_friend()
                if(cmd==2):self.ask_passerby()
                if(cmd==3):self.half()
                if(cmd==4):
                    self.times[4]-=1
                    break
                if(cmd>4):
                    Ans=chr(60+cmd)
                    if(self.ps.answer_kth_question(i,Ans)):
                        break
                    else:
                        self.fail()
                        break
        if(self.times[0]):self.succeed()

seed()
ifc=interface()
ifc.work()
ifc.game_over()
