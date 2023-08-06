def es_primo(n):
    
    if n<2:
        return False
    
    for i in range(2,n):
        if n % i ==0:
            return False
    return True

def primos(num1, num2):  

    cont =+ 0
  
    for i in range(num1, num2+1):
        if es_primo(i) == True: 
            cont += 1           
            print (i)               
  
    print ("")  
    print ("Hay", cont, "numeros primos") 
       
print (primos(1, 5))


        
   

               
    
        


