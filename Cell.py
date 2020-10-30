class cell:
    def __init__(self,x,y,status = -1,clue = -1, safeSurr = 0, mineSurr = 0, hiddenSurr = 8):
        """[summary]

        Args:
            status (int): 10 for flagged as mine, 0 for safe, -1 for covered. Defaults to -1.
            clue (int, optional): [description]. Defaults to -1.
            safeSurr (int, optional): [description]. Defaults to 0.
            mineSurr (int, optional): [description]. Defaults to 0.
            hiddenSurr (int, optional): [description]. Defaults to 8.
        """
        self.x = x
        self.y = y
        self.status = status
        self.clue = clue
        self.safeSurr = safeSurr
        self.mineSurr = mineSurr
        self.hiddenSurr = hiddenSurr
    
    def set(self,status = -1,clue = -1, safeSurr = 0, mineSurr = 0, hiddenSurr = 8):
        """[summary]

        Args:
            status (int): 10 for flagged as mine, 0 for safe, -1 for covered. Defaults to -1.
            clue (int, optional): [description]. Defaults to -1.
            safeSurr (int, optional): [description]. Defaults to 0.
            mineSurr (int, optional): [description]. Defaults to 0.
            hiddenSurr (int, optional): [description]. Defaults to 8.
        """
        self.status = status
        self.clue = clue
        self.safeSurr = safeSurr
        self.mineSurr = mineSurr
        self.hiddenSurr = hiddenSurr
