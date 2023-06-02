from priodict import EmptyDict

class HeapDict(dict):

    def __init__(self) -> None:
        super().__init__()
        self.t = []

    def __getitem__(self, key):
        idx = super().__getitem__(key)
        return self.t[idx][0]

    def parent(i):
        """ étant donné l'indice 'i' d'un nœud,
    retourne l'indice du nœud parent """
        return (i-1)//2
    def gauche(i):
        """ étant donnée l'indice 'i' d'un nœud,
    retourne l'indice de l'enfant de gauche """
        return 2*i+1
    def droite(i):
        """ étant donné  l'indice 'i' d'un nœud,
    retourne l'indice de l'enfant de gauche """
        return 2*i+2

    def echange (self,i,j):
        x =self.t[i]
        y = self.t[j]
        self.t[i]=y
        self.t[j]=x
        super().__setitem__(x[1],j)
        super().__setitem__(y[1],i)

    def versracine(self,i):
        courrant=i
        val=self.t[i]
        while True:
            if courrant == 0:
                break
            p=parent(courrant)
            if self.t[p]<val:
                break
            self.echange(courrant, p)
            courrant = p
    
    def __setitem__(self, key, newprio):
        pass