class Answer:
    def __init__(self,title,Description,author):
        self.Title=title
        self.Description=Description
        self.Author=author
    Challenges=[]
    Responses=[]
    def set(self,response,**kwargs):
        self.Challenges.append(kwargs)
        self.Responses.append(response)
    
    def check(self,expFunc):
        correct=0
        wrong=0
        print("\n["+self.Title+"]")
        print('"'+self.Description+'"\n')

        for challengeId in range(0,len(self.Challenges)):
            challenge=self.Challenges[challengeId]
            #print(challenge)
            res=expFunc(**challenge)
            if res==self.Responses[challengeId]:
                print("[Correct]:%s --> %s" % (challenge,res))
                correct+=1
            else:
                print("[Wrong]:%s --> %s Answer: %s" % (challenge,res,self.Responses[challengeId]))
                wrong+=1
        print("\nCorrect: %s/%s" % (correct,len(self.Challenges)))
        print("Wrong: %s/%s" % (wrong,len(self.Challenges)))
        if wrong==0:
            print("\nThis Challenge Has Been Solved By "+self.Author)
        else:
            print("\n"+self.Author+"! Try again!")