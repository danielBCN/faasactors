class userCode():
    x=0
    def userFunction(self):
        """
        Function for the user to fill
        """
        print("User function starts")
        global x
        self.x += 1
        print("x: ",self.x)
        print("User function ends")

