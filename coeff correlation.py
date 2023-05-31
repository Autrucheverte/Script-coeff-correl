import numpy as np
from sklearn.linear_model import LinearRegression
from random import randint
import math

def fonction_db(h,l,L,v,nb_f,coeff_abs_sol,coeff_abs_mur,nb_eleves,classe):
    return round((((math.sqrt(nb_eleves)-2)-(nb_f/4))*(25+classe)*(1-(coeff_abs_sol+coeff_abs_mur)/2)*(v+2000))/2500*10)/10
    
def new_mesures(nb):
    mesures = list()
    for i in range(nb):
        h = randint(5, 8)/2
        l = randint(60, 150)/10
        L = randint(40, 100)/10
        v = h*l*L
        nb_f = randint(2, 4)
        coeff_abs_sol = randint(1, 30)/100
        coeff_abs_mur = randint(1, 30)/100
        nb_eleves = randint(23, 30)
        classe = randint(1, 6)
        db = fonction_db(h,l,L,v,nb_f,coeff_abs_sol,coeff_abs_mur,nb_eleves,classe)*(randint(9,11)/10)
        
        mesures.append([db,h,l,L,v,coeff_abs_sol,nb_eleves,classe])
    return mesures


type_des_parametres = ["son", "hauteur", "longueur", "Largeur", "Volume", "coefficient de absorption sol", "nombre d'eleves", "classe"]
type_des_parametres_short = ["h", "l", "L", "v", "coeff_abs_sol", "nb_eleve", "classe"]
mesures = [[[68,58], 2.6,13.5,8,280.8, 0.20, 25, 3], [[60,43], 2.6,7.5,5.5,107.25, 0.02, 22, 6], [[66,51], 2.6,9,5.5,128.7, 0.20, 25, 2], [[69,54], 3,14,5.7,(3*14*5.7), 0.02, 22, 3], [[41.4,66], 3.3,11.2,8.6,(3.3*11.2*8.6), 0.20, 22, 6], [[60,72], 3.5,9.8,6,(3.5*9.8*6), 0.20, 27, 2], [[40,59], h,l,L,(h*l*L), 0.20, 21, 6], [[49,64], h,l,L,(h*l*L), 0.20, 25, 2]]


# mesures = new_mesures(3)

resultats = [m[0][0] for m in mesures]
parametres = [m[1:] for m in mesures]

coefficients_correlation = []
for i in range(len(parametres[0])):
    coef_corr = np.corrcoef(resultats, [p[i] for p in parametres])[0,1]
    coefficients_correlation.append(round(coef_corr*100)/100)

print("Coefficients de correlation:")
for i in range(len(coefficients_correlation)):
    print("    {}: {}".format(type_des_parametres[i+1], coefficients_correlation[i]))
    
    
    


modele = LinearRegression()

modele.fit(parametres, resultats)

def prediction_mesure(mesure):
    return modele.predict([mesure[1:]])[0]

coefficients = modele.coef_
constante = modele.intercept_

equation = "y = " + " + ".join([f"{coefficients[i]:.2f}*{type_des_parametres_short[i]}" for i in range(len(coefficients))])
if constante > 0:
    equation += f" + {constante:.2f}"
elif constante < 0:
    equation += f" - {abs(constante):.2f}"
print("\n\nEquation de la fonction de regression lineaire:")
print(equation)


def modelisation_db(coefficients,constante,mesure):
    resultat = 0
    for i in range(len(coefficients)):
        resultat += coefficients[i]*mesure[i+1]
    resultat += constante
    return resultat

incertitudes = list()
incertidude_moyenne = 0
# mesures = new_mesures(10000)





# for mesure in mesures:
#     incertitude = round(abs(mesure[0]-modelisation_db(coefficients, constante, mesure))/mesure[0]*100)/100
#     incertitudes.append(incertitude)
#     incertidude_moyenne += incertitude
    
# incertidude_moyenne = round(incertidude_moyenne/len(mesures)*100)/100

# print("\nIncertitude max: "+str(round(max(incertitudes)*1000)/10)+"%\nIncertitude moyenne: "+str(round(incertidude_moyenne*1000)/10)+"%")
