
import time
import random
import colorama

##defs:

def escrever(txt):
    print(txt)

def perguntar(type, qst):
    if type == 'inteiro':
        msg = int(input(qst))
        return msg
    elif type == 'decimal':
        msg = float(input(qst))
        return msg
    elif type == 'texto':
        msg = str(input(qst))
        return msg
    elif type == 'vof':
        msg = bool(input(qst))
        return msg
    elif type == None:
        print('# ERRO: Informe um tipo correto para recolher sua pergunta (texto, decimal, inteiro, vorf)')

def aleatorizarNumeros(np, nf):
    r = random.randint(np, nf)
    
    return r

def aguardar(tempo):
    time.sleep(tempo)

def somar(x, y):
    return x+y

def subtrair(x, y):
    return x - y

def multiplicar(x, y):
    return x*y

def dividir_completo(x, y):
    return x/y

def dividir(x, y):
    return x//y

def elevar(x, y):
    return pow(x, y)

##Cores:

def cor(cor):

    if cor== 0 or cor== 'branco':
        return colorama.Fore.RESET
    elif cor== 1 or cor == 'vermelho':
        return colorama.Fore.RED
    elif cor== 2 or cor== 'verde':
        return colorama.Fore.GREEN
    elif cor== 3 or cor== 'azul':
        return colorama.Fore.BLUE
    elif cor== 4 or cor== 'amarelo':
        return colorama.Fore.YELLOW
    elif cor== 5 or cor== 'roxo':
        return colorama.Fore.MAGENTA
    
def aleatorizarListas(lista):
    return random.choice(lista)

def se(firstcondition, maincondition, secondcontion, react, freac):
    if maincondition == '=' or maincondition == '==':
        if firstcondition == secondcontion:
            if type(react) == str:
                print(react)
            else:
                print(colorama.Fore.RED + '# ERRO: O termo `react`, deve ser considerado TEXTO #')  
        else:
            if isinstance(freac, str) == True:
                print(freac)
            else: 
                print(colorama.Fore.RED + '# ERRO: O termo `freact` deve ser considerado TEXTO #')
    elif maincondition == '>':
        if firstcondition > secondcontion:
            if isinstance(react, str) == True:
                print(react)
            else:
                print(colorama.Fore.RED + '# ERRO: O termo `react`, deve ser considerado TEXTO #')
        else:
            if isinstance(freac, str) == True:
                print(freac)
            else: 
                print(colorama.Fore.RED + '# ERRO: O termo `freact` deve ser considerado TEXTO #')
    elif maincondition == '>=':
        if firstcondition >= secondcontion:
            if isinstance(react, str) == True:
                print(react)
            else:
                print(colorama.Fore.RED + '# ERRO: O termo `react`, deve ser considerado TEXTO #')
        else:
            if isinstance(freac, str) == True:
                print(freac)
            else: 
                print(colorama.Fore.RED + '# ERRO: O termo `freact` deve ser considerado TEXTO #')
    elif maincondition == '<':
        if firstcondition < secondcontion:
            if isinstance(react, str) == True:
                print(react)
            else:
                print(colorama.Fore.RED + '# ERRO: O termo `react`, deve ser considerado TEXTO #')
        else:
            if isinstance(freac, str) == True:
                print(freac)
            else: 
                print(colorama.Fore.RED + '# ERRO: O termo `freact` deve ser considerado TEXTO #')
    elif maincondition == '<=':
        if firstcondition <= secondcontion:
            if isinstance(react, str) == True:
                print(react)
            else:
                print(colorama.Fore.RED + '# ERRO: O termo `react`, deve ser considerado TEXTO #')
        else:
            if isinstance(freac, str) == True:
                print(freac)
            else: 
                print(colorama.Fore.RED + '# ERRO: O termo `freact` deve ser considerado TEXTO #')

