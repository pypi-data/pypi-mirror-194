from random import randint
def choserandom():
    a=range(ord("A"),ord("Z")+1)
    a2=range(ord("a"),ord("z")+1)
    a3=range(ord("0"),ord("9")+1)
    x=randint(0,3)
    if(x==0):
        return chr(a[randint(0,len(a)-1)])
    elif x==1:
        return chr(a2[randint(0,len(a2)-1)])
    else:
        
        return chr(a3[randint(0,len(a3)-1)])
def generatepwd(**args):
    cd=""
    nb=8
    for i in args:
        
        if( i.lower()=="len" and type(args[i])==int):
            nb=args[i]

    for i in range(nb):
        cd+=choserandom()
    return cd
