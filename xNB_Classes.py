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
        return 'data: ' + str(self.x) + '\nmu: '+str(self.mu_hat) + '\nnu: ' + str(self.nu_hat)
        
    def buoyancy(self):
        return self.mu_hat[0] - self.nu_hat[0]
    
    def hesitation(self):
        return 1.0 - self.mu_hat[0] - self.nu_hat[0]
    
