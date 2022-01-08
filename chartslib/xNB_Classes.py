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
    
    def define_xAAD(self,mode=1):
        if mode == 1:
            return xAAD(self.mu_hat[0],self.mu_hat[1])
        else:
            return xAAD(self.nu_hat[0],self.nu_hat[1])

    def hesitation(self):
        return 1.0 - self.mu_hat[0] - self.nu_hat[0]
    
