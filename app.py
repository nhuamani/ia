from flask import Flask
from flask import render_template
from flask import request, Response
import json

import numpy as np
import pandas as pd
from sklearn import svm

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.2)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')


@app.route('/ajax-login', methods=['POST'])
def ajax_login():
    print(request.form)
    edad = request.form['edad']
    colesterol = request.form['colesterol']
    print(edad)
    print(colesterol)

    # ========================================
    pacientes = pd.read_csv('file_limpio.csv')
    pacientes

    sns.lmplot('age', 'chol', data=pacientes, hue='ries',
               palette='Set1', fit_reg=False, scatter_kws={"s": 70})

    # ingredientes = pacientes[['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']].values
    ingredientes = pacientes[['age', 'chol']].values
    type_label = np.where(pacientes['ries'] == 1, 0, 1)

    recipe_features = pacientes.columns.values[1:].tolist()
    recipe_features

    model = svm.SVC(kernel='linear')
    model.fit(ingredientes, type_label)


    # Get the separating hyperplane
    w = model.coef_[0]
    a = -w[0] / w[1]
    xx = np.linspace(30, 60)
    yy = a * xx - (model.intercept_[0]) / w[1]

    # Plot the parallels to the separating hyperplane that pass through the
    # support vectors
    b = model.support_vectors_[0]
    yy_down = a * xx + (b[1] - a * b[0])
    b = model.support_vectors_[-1]
    yy_up = a * xx + (b[1] - a * b[0])

    # Plot the hyperplane
    sns.lmplot('age', 'chol', data=pacientes, hue='ries',
               palette='Set1', fit_reg=False, scatter_kws={"s": 70})
    plt.plot(xx, yy, linewidth=2, color='black')

    # Look at the margins and support vectors
    sns.lmplot('age', 'chol', data=pacientes, hue='ries',
               palette='Set1', fit_reg=False, scatter_kws={"s": 70})
    plt.plot(xx, yy, linewidth=2, color='black')
    plt.plot(xx, yy_down, 'k--')
    plt.plot(xx, yy_up, 'k--')
    plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[
                :, 1], s=80, facecolors='none')

    # Create a function to guess when a recipe is a muffin or a cupcake


    def riesgo_or_noriesgo(age, chol):
        if(model.predict([[age, chol]])) == 0:
            mensaje = "Pertenece al cluster 1, es un paciente potencialmente a tener un problema serio en el corazón"
            print(mensaje)
        else:
            mensaje = "Pertenece al cluster 0, es un paciente que no puede tener un problema serio en el corazón!"
            print(mensaje)

        return mensaje

    calcular = riesgo_or_noriesgo(edad, colesterol)
    print("hola mundpsalksasaaisaskjaskjas ", calcular)
    # Plot the point to visually see where the point lies
    sns.lmplot('age', 'chol', data=pacientes, hue='ries',
               palette='Set1', fit_reg=False, scatter_kws={"s": 70})
    plt.plot(xx, yy, linewidth=2, color='black')
    plt.plot(50, 150, 'yo', markersize='9')

    # ==============================================
    data = {'status': 'OK', 'edad': edad, 'colesterol': colesterol, 'rpta': calcular}

    return Response(json.dumps(data), mimetype='aplication/json')


if __name__ == "__main__":
    app.run(debug=True)
