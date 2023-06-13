import joblib
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X = pd.DataFrame(iris.data)
y = pd.DataFrame(iris.target)

# Поділ на тренувальну та тестову вибірки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=111)
# Створення пайплайну
pipeline = Pipeline([
    ('scaling', StandardScaler()),  # Масштабування даних
    ('pca', PCA()),  # Відбір ознак методом головних компонент
    ('classification', LogisticRegression(max_iter=100))
])

# Визначення сітки гіперпараметрів для пошуку
parameters = {
    'pca__n_components': [2, 3],  # Кількість головних компонент для відбору
    'classification__C': [0.1, 1, 10]  # Гіперпараметри моделі Logistic Regression
}

# Настройка гіперпараметрів та відбір ознак
grid_search = GridSearchCV(pipeline, parameters, scoring='accuracy')
grid_search.fit(X_train, y_train.values.ravel())

# Оцінка на тестовій вибірці
y_pred = grid_search.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)

# Збереження навченого пайплайну
joblib.dump(grid_search, 'pipeline.joblib')

# Завантаження пайплайну для подальшого використання
loaded_pipeline = joblib.load('pipeline.joblib')
