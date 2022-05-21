from sklearn.metrics import accuracy_score
import STIF
import Eigenfaces
import knn
import xlsxwriter
import time

distortions = ['Sujetos','Sin Distorsion','brightness(-30,10,all_channels)','affine1([10,10,5,5,70,10,75,5,60,60,60,65])', 'affine2([10,10,5,5,70,10,85,15,70,92,85,72])', 'arc1([15,])', 'arc2([18,])', 'scale(112x112,135%)']

lowerLimit = 0
upperLimit = 10
initTime = time.time()

stifGeneralScores, stifSubjectScores = STIF.testingMatrix()
print(stifGeneralScores)

sujetosStif = []
for i in range(40):
    sujetosStif.append(['Sujeto ' + str(i+1)])


for (distortion, averageScore) in zip(distortions, stifGeneralScores):
    for (i, sujeto) in zip(range(40), sujetosStif):
        precisionSujeto = accuracy_score([i for j in range(10)], stifSubjectScores[lowerLimit:upperLimit])
        print("Precision de sujeto %s es: %s" % (i+1, (precisionSujeto)))
        lowerLimit = upperLimit
        upperLimit += 10
        sujeto.append(precisionSujeto)
    print("Resultado promedio para distorsion %s es: %s" % (distortion, averageScore))
sujetosStif.append(['Promedio'] + stifGeneralScores)

#knnGeneralScores = [0.03, 0.0275, 0.0175, 0.055, 0.0425, 0.045]
knnGeneralScores, knnSubjectScores = knn.testingMatrix()

sujetosKnn = []
for i in range(40):
    sujetosKnn.append(['Sujeto ' + str(i+1)])

lowerLimit = 0
upperLimit = 10

for (distortion, averageScore) in zip(distortions, knnGeneralScores):
    for (i, sujeto) in zip(range(40), sujetosKnn):
        precisionSujeto = accuracy_score([i for j in range(10)], knnSubjectScores[lowerLimit:upperLimit])
        print("Precision de sujeto %s es: %s" % (i+1, (precisionSujeto)))
        lowerLimit = upperLimit
        upperLimit += 10
        sujeto.append(precisionSujeto)
    print("Resultado promedio para distorsion %s es: %s" % (distortion, averageScore))
sujetosKnn.append(['Promedio'] + knnGeneralScores)

eigenfacesGeneralScores, eigenfacesSubjectScores = Eigenfaces.testingMatrix()
print(len(eigenfacesSubjectScores))

endTime = time.time()
print("Tiempo de evaluacion %s" % (endTime-initTime))

sujetosEigenfaces = []
for i in range(40):
    sujetosEigenfaces.append(['Sujeto ' + str(i+1)])

print(sujetosEigenfaces)

lowerLimit = 0
upperLimit = 10

for (distortion, averageScore) in zip(distortions, eigenfacesGeneralScores):
    for (i, sujeto) in zip(range(40), sujetosEigenfaces):
        precisionSujeto = accuracy_score([i for j in range(10)], eigenfacesSubjectScores[lowerLimit:upperLimit])
        print("Precision de sujeto %s es: %s" % (i+1, (precisionSujeto)))
        lowerLimit = upperLimit
        upperLimit += 10
        sujeto.append(precisionSujeto)
    print("Resultado promedio para distorsion %s es: %s" % (distortion, averageScore))
sujetosEigenfaces.append(['Promedio'] + eigenfacesGeneralScores)

for sujeto in sujetosEigenfaces:
    print("Precisiones %s" % (sujeto))

workbook = xlsxwriter.Workbook('Resultados.xlsx')
worksheetStif = workbook.add_worksheet('STIF')
worksheetKnn = workbook.add_worksheet('KNN')
worksheetEigenfaces = workbook.add_worksheet('Eigenfaces')

row = 1
column = 0

for distortion in distortions:
    worksheetStif.write(row, column, distortion)
    worksheetKnn.write(row, column, distortion)
    worksheetEigenfaces.write(row, column, distortion)
    column += 1

for (scoreStif, scoreKnn, scoreEigen) in zip(sujetosStif, sujetosKnn,sujetosEigenfaces):
    column = 0
    row += 1
    for (precisionStif, precisionKnn, precisionEigen) in zip(scoreStif, scoreKnn, scoreEigen):
        worksheetStif.write(row, column, precisionStif)
        worksheetKnn.write(row, column, precisionKnn)
        worksheetEigenfaces.write(row, column, precisionEigen)
        column += 1

workbook.close()



