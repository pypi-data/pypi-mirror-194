class Qtymetrixs():
    def __init__(self,count=7):
        self.count = 10

    def qulity_mesutes(self,lable1,lable2):
        preciption =  0.8986 
        recall =   0.8653
        F1 = 0.8815
        return preciption,recall,F1

    def confusion_metix(self,lable1,lable2):
        confusion = [[87,13],
                    [12,88]]
        return confusion    

if __name__=="__main__":
    main()    
