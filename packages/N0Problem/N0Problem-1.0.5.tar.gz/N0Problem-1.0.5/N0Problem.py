class Answer:
    def __init__(self,title,Description,author):
        self.Title=title
        self.Description=Description
        self.Author=author
    Challenges=dict()
    def set(self,challenge,response="$n0p"):
        if type(challenge)==dict:
            self.Challenges=challenge
        else:
            if response!="$n0p":
                self.Challenges[challenge]=response
            else:
                print(challenge+" need a response.")
    def check(self,expFunc):
        correct=0
        wrong=0
        print("\n["+self.Title+"]")
        print('"'+self.Description+'"\n')
        
        for challenge in self.Challenges:
            #print(challenge)
            if type(challenge)==tuple:
                res=expFunc(*challenge)
            else:
                res=expFunc(challenge)
            if res==self.Challenges[challenge]:
                print("[Correct]:%s --> %s" % (challenge,self.Challenges[challenge]))
                correct+=1
            else:
                print("[Wrong]:%s --> %s Answer: %s" % (challenge,res,self.Challenges[challenge]))
                wrong+=1
        print("\nCorrect: %s/%s" % (correct,len(self.Challenges)))
        print("Wrong: %s/%s" % (wrong,len(self.Challenges)))
        if wrong==0:
            print("\nThis Challenge Has Been Solved By "+self.Author)
        else:
            print("\n"+self.Author+"! Try again!")