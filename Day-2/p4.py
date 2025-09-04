def bill(tu):
    if(1<=tu<=50):
        cbill= tu*3.80
    elif(51<=tu<=100):
         cbill=(50*3.80)+((tu-50)*4.40)
    elif(100<=tu<=200):
         cbill=(50*3.80)+((50)*4.40)+((tu-100)*5.10)
    elif(200<=tu<=300):
         cbill=(50*3.80)+(50*4.40)+(100*5.10)+((tu-200)*6.30)
    elif(300<=tu<=400):
         cbill=(50*3.80)+(50*4.40)+(100*5.10)+(100*6.30)+((tu-300)*7.20)
    else:
         print('invalid')
         return
    print('total bill:',cbill)
        
bill(90)

