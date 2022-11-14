import numpy as np
import pandas as pd
import random

def lambdaGeneral(df, equipo):
    pais = df[(df['home_team'] == equipo)|(df['away_team'] == equipo)].tail(10)
    
    df1 = pais[pais["home_team"] == equipo]
    df2 = pais[pais["away_team"] == equipo]

    goles = df1['home_score'].sum() + df2['away_score'].sum()
    promGol = goles/10 

    return promGol

def findLambdas(df, equipoA, equipoB):
    df1 = df[((df["home_team"] == equipoA) & (df["away_team"] == equipoB))]
    df2 = df[((df["home_team"] == equipoB) & (df["away_team"] == equipoA))]
    
    noPartidos = df1.shape[0] + df2.shape[0]
    
    if(noPartidos == 0):
        penA, penB = 1, 1
        partidosA = df[((df["home_team"] == equipoA) | (df["away_team"] == equipoA))]
        partidosB = df[((df["home_team"] == equipoB) | (df["away_team"] == equipoB))]
        cantPartidosFifaA = partidosA[partidosA['tournament'] == 'FIFA World Cup'].shape[0]
        cantPartidosFifaB = partidosB[partidosB['tournament'] == 'FIFA World Cup'].shape[0]
        if(cantPartidosFifaA < 7*cantPartidosFifaB): penA = 0.7
        if(cantPartidosFifaB < 7*cantPartidosFifaA): penB = 0.7
        
        promGolA = lambdaGeneral(df, equipoA) * penA
        promGolB = lambdaGeneral(df, equipoB) * penB
        
    else: 
        golA = df1['home_score'].sum() + df2['away_score'].sum()
        golB = df2['home_score'].sum() + df1['away_score'].sum()
        
        promGolA = golA / noPartidos
        promGolB = golB / noPartidos
        
    if(promGolA == 0): lambdaA = (90*100)/1
    else: lambdaA = 90/promGolA
        
    if(promGolB == 0): lambdaB = (90*100)/1
    else: lambdaB = 90/promGolB
    
    return lambdaA, lambdaB

def dist_expo(Lambda):
    u = random.uniform(0,1)
    t = -Lambda*np.log(1-u)
    return t

def simulGoles(Lambda):      
    minutos = 0
    goles = 0
    while(minutos <= 90):
        minutos += dist_expo(Lambda)
        if(minutos <= 90): goles += 1
        
    return goles

def simulPartido(df, equipoA, equipoB):
    lambdaA, lambdaB = findLambdas(df, equipoA, equipoB)
    golesA, golesB = simulGoles(lambdaA), simulGoles(lambdaB)
    
    return golesA, golesB

def simulPartido_Win(df, equipoA, equipoB):
    lambdaA, lambdaB = findLambdas(df, equipoA, equipoB)
    winner = ''
    while(winner == ''):
        golesA, golesB = simulGoles(lambdaA), simulGoles(lambdaB)
        if(golesA > golesB): winner = equipoA
        if(golesA < golesB): winner = equipoB
    return winner

def puntos(goles):
    resA, resB = 1, 1
    if(goles[0] > goles[1]):
        resA, resB = 3, 0
    if(goles[0] < goles[1]):
        resA, resB = 0, 3
    return resA, resB
    
def simulGrupo(df, equipoA, equipoB, equipoC, equipoD):
    matchAB = simulPartido(df, equipoA, equipoB)
    matchAC = simulPartido(df, equipoA, equipoC)
    matchAD = simulPartido(df, equipoA, equipoD)
    matchBC = simulPartido(df, equipoB, equipoC)
    matchBD = simulPartido(df, equipoB, equipoD)
    matchCD = simulPartido(df, equipoC, equipoD)
    
    ptsAB = puntos(matchAB)
    ptsAC = puntos(matchAC)
    ptsAD = puntos(matchAD)
    ptsBC = puntos(matchBC)
    ptsBD = puntos(matchBD)
    ptsCD = puntos(matchCD)
    
    ptsA = ptsAB[0] + ptsAC[0] + ptsAB[0]
    ptsB = ptsAB[1] + ptsBC[0] + ptsBD[0]
    ptsC = ptsAC[1] + ptsBC[1] + ptsCD[0]
    ptsD = ptsAD[1] + ptsBD[1] + ptsCD[1]
    
    ptsGrupo = [[equipoA, ptsA], [equipoB, ptsB], [equipoC, ptsD], [equipoD, ptsD]]
    
    ptsGrupo = sorted(ptsGrupo, key = lambda x: x[1], reverse = True)
    
    
    return ptsGrupo[0][0], ptsGrupo[1][0]

def simulMundial(df):
    # Grupos
    equipo1A, equipo2A = simulGrupo(df, 'Qatar', 'Ecuador', 'Senegal', 'Netherlands')
    equipo1B, equipo2B = simulGrupo(df, 'England', 'Iran', 'United States', 'Wales')
    equipo1C, equipo2C = simulGrupo(df, 'Argentina','Saudi Arabia', 'Mexico', 'Poland')
    equipo1D, equipo2D = simulGrupo(df, 'France','Australia', 'Denmark', 'Tunisia')
    equipo1E, equipo2E = simulGrupo(df, 'Spain','Costa Rica', 'Germany', 'Japan')
    equipo1F, equipo2F = simulGrupo(df, 'Belgium', 'Canada', 'Morocco', 'Croatia')
    equipo1G, equipo2G = simulGrupo(df, 'Brazil','Serbia','Switzerland','Cameroon')
    equipo1H, equipo2H = simulGrupo(df, 'Portugal', 'Ghana', 'Uruguay', 'South Korea')

    # Octavos
    equipoW49 = simulPartido_Win(df, equipo1A, equipo2B)
    equipoW50 = simulPartido_Win(df, equipo1C, equipo2D)
    equipoW51 = simulPartido_Win(df, equipo1B, equipo2A)
    equipoW52 = simulPartido_Win(df, equipo1D, equipo2C)

    equipoW53 = simulPartido_Win(df, equipo1E, equipo2F)
    equipoW54 = simulPartido_Win(df, equipo1G, equipo2H)
    equipoW55 = simulPartido_Win(df, equipo1F, equipo2E)
    equipoW56 = simulPartido_Win(df, equipo1H, equipo2G)

    # Cuartos
    equipoW57 = simulPartido_Win(df, equipoW49, equipoW50)
    equipoW58 = simulPartido_Win(df, equipoW53, equipoW54)
    equipoW59 = simulPartido_Win(df, equipoW51, equipoW52)
    equipoW60 = simulPartido_Win(df, equipoW55, equipoW56)

    # Semifinal
    equipoW61 = simulPartido_Win(df, equipoW57, equipoW58)
    equipoW62 = simulPartido_Win(df, equipoW59, equipoW60)

    # Final
    ganador = simulPartido_Win(df, equipoW61, equipoW62)
    
    return ganador

    
    

df_mundiales = pd.read_csv('results.csv')
#equipo1B, equipo2B = simulGrupo(df_mundiales, 'England', 'Iran', 'United States', 'Wales')

#Inicial simulacion
for i in range(20):
    ganador = simulMundial(df_mundiales)
    print(ganador)


    
    

