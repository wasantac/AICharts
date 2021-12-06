class xAAD:
    def __init__(self,value,dictionary):
        self.value = value
        self.dictionary = dictionary

class xAIFSElement:
    def __init__(self,x,mu_hat,nu_hat):
        self.x = x
        self.mu_hat = mu_hat
        self.nu_hat = nu_hat

    def __repr__(self):
        return '[' + str(self.x) + ',' + '\n'+str(self.mu_hat) + ','+ '\n' + str(self.nu_hat) + ']' 
        
    def buoyancy(self):
        return self.mu_hat - self.nu_hat
    
    def hesitation(self):
        return 1.0 - self.mu_hat - self.nu_hat
    
