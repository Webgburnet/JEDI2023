from priodict import EmptyDict

class SimpleDict(dict):
    """Version naïve avec un dictionnaire"""

    def pop_smallest(self):
        if not self:
            raise EmptyDict
        valmin= float ('inf')
        for k,v in self.items() :
            if v < valmin:
                valmin=v
                kmin=k
        del self[kmin]
        return(kmin,valmin)
        #raise NotImplementedError("il faut coder uniquement pop_smallest !")
