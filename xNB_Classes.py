class xAAD:
    def __init__(self,value,dictionary):
        self.value = value
        self.dictionary = dictionary

class xAIFSElement:
    def __init__(self,x,mu_hat,nu_hat):
        self.object = x
        self.object = mu_hat
        self.object = nu_hat

    def buoyancy(self):
        return self.mu_hat - self.nu_hat
    
    def hesitation(self):
        return 1.0 - self.mu_hat - self.nu_hat