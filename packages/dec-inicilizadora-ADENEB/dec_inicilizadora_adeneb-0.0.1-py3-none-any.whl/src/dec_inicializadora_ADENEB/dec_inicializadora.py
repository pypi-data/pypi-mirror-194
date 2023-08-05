import sys

def decoradora(fun = {}, var = []):
    
    try:
        
        def dec(cls):
            
            class MetaClase(type):
                
                def __init__(cls, nombre, base, dic):  
                    type.__init__(cls, nombre, base, dic)
            
            clase_inicializadora = MetaClase("mid_inicializadora", (cls,), fun)
            
            class Inicializadora(clase_inicializadora):
                
                def __init__(self, lista = var, **kwargs):
                        
                    try:   
                        
                        self.lista = lista
                        list(map(lambda x : exec(f"self.{x[0]} = x[1]", {}, {'self' : self, 'x' : x, 'kwargs' : kwargs}) if x[0] not in self.lista else exec('raise(Exception("variable no utilizable"))') , kwargs.items()))
                        
                        super().__init__(self, lista = var, **kwargs)
                        
                    except Exception as e:
                            
                        print(e)
                            
                        if str(e) == "variable no utilizable":
                            print(f"las variables utilizables son: {self.lista}")
                                
                        sys.exit()
                        
                    
            return Inicializadora
        
        return dec

    except Exception as e:
        
        print(e)