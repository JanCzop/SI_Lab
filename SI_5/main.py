from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup, Comment, NavigableString
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

should_analyze = False

def read_jokes():
    jokes = []
    for i in range(1, 101):
        filename = f"jokes/init{i}.html"

        with open(filename, "r") as file:
            soup = BeautifulSoup(file, "html.parser")

        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for i, comment in enumerate(comments):
            if "begin of joke" in comment:
                joke = ''
                next_node = comment.next_element
                while next_node and not (isinstance(next_node, Comment) and "end of joke" in next_node):
                    if isinstance(next_node, NavigableString):
                        joke += next_node.strip()
                    next_node = next_node.next_element
                jokes.append(joke)
    return jokes

jokes_texts = read_jokes()

jester_df1 = pd.read_excel('jester-data-1.xls', header=None)
jester_df2 = pd.read_excel('jester-data-2.xls', header=None)
jester_df3 = pd.read_excel('jester-data-3.xls', header=None)

jokes = pd.concat([jester_df1, jester_df2, jester_df3], ignore_index=True)
jokes.columns = ['num_jokes_rated'] + ['joke_rating_'+str(i) for i in range(1, 101)]

print(jokes)

model = SentenceTransformer('bert-base-cased')

mean_joke_ratings = jokes.replace(99, np.nan).iloc[:, 1:].mean()
jokes_with_ratings = pd.DataFrame({'Joke': jokes_texts, 'Rating': mean_joke_ratings})

X = model.encode(jokes_with_ratings['Joke'])
y = jokes_with_ratings['Rating']

print(jokes_with_ratings)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train)
print(y_train)

def analyze_models():
    all_errors = []

    learning_rates = [0.001, 0.01, 0.1]
    hidden_layer_sizes = [10, 100, 1000]

    epochs = 200

    for lr in learning_rates:
        for hls in hidden_layer_sizes:
            mlp = MLPRegressor(hidden_layer_sizes=(hls, ), solver='sgd', alpha=0.0, learning_rate_init=lr, random_state=42, max_iter=1, warm_start=True)
            train_errors = []
            test_errors = []
            for _ in range(epochs):
                mlp.fit(X_train, y_train)
                train_errors.append(mean_squared_error(y_train, mlp.predict(X_train)))
                test_errors.append(mean_squared_error(y_test, mlp.predict(X_test)))
            all_errors.append({'learning_rate': lr, 'hidden_layer_size': hls, 'train_errors': train_errors, 'test_errors': test_errors})

    # Użyteczne wykresy
    for errors in all_errors:
        df = pd.DataFrame({
            'Epoch': range(1, len(errors['train_errors']) + 1),
            'Train': errors['train_errors'],
            'Test': errors['test_errors']
        })
        df_melted = df.melt(id_vars=['Epoch'], value_vars=['Train', 'Test'], var_name='Dataset', value_name='MSE')
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df_melted, x='Epoch', y='MSE', hue='Dataset')
        plt.title(f'Learning Rate: {errors["learning_rate"]}, Hidden Layer Size: {errors["hidden_layer_size"]}')
        plt.show()

    # Pozostałe wykresy
    plt.figure(figsize=(10, 6))
    for errors in all_errors:
        if errors['hidden_layer_size'] == hidden_layer_sizes[0]:
            plt.plot(range(1, len(errors['train_errors']) + 1), errors['train_errors'], label=f'Learning Rate: {errors["learning_rate"]}')
    plt.title(f'Train Errors for different Learning Rates, Hidden Layer Size: {hidden_layer_sizes[0]}')
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.legend()
    plt.show()


    plt.figure(figsize=(10, 6))
    for errors in all_errors:
        if errors['hidden_layer_size'] == hidden_layer_sizes[0]:
            plt.plot(range(1, len(errors['test_errors']) + 1), errors['test_errors'], label=f'Learning Rate: {errors["learning_rate"]}')
    plt.title(f'Test Errors for different Learning Rates, Hidden Layer Size: {hidden_layer_sizes[0]}')
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.legend()
    plt.show()


    for lr in learning_rates:
        plt.figure(figsize=(10, 6))
        for errors in all_errors:
            if errors['learning_rate'] == lr:
                plt.plot(range(1, len(errors['train_errors']) + 1), errors['train_errors'], label=f'Hidden Layer Size: {errors["hidden_layer_size"]}')
        plt.title(f'Train Errors for different Hidden Layer Sizes, Learning Rate: {lr}')
        plt.xlabel('Epoch')
        plt.ylabel('MSE')
        plt.legend()
        plt.show()


    plt.figure(figsize=(10, 6))
    for errors in all_errors:
        if errors['learning_rate'] == learning_rates[0]:
            plt.plot(range(1, len(errors['train_errors']) + 1), errors['train_errors'], label=f'Hidden Layer Size: {errors["hidden_layer_size"]}')
    plt.title(f'Train Errors for different Hidden Layer Sizes, Learning Rate: {learning_rates[0]}')
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.legend()
    plt.show()


    plt.figure(figsize=(10, 6))
    for errors in all_errors:
        if errors['learning_rate'] == learning_rates[0]:
            plt.plot(range(1, len(errors['test_errors']) + 1), errors['test_errors'], label=f'Hidden Layer Size: {errors["hidden_layer_size"]}')
    plt.title(f'Test Errors for different Hidden Layer Sizes, Learning Rate: {learning_rates[0]}')
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.legend()
    plt.show()


    for hls in hidden_layer_sizes:
        plt.figure(figsize=(10, 6))
        for errors in all_errors:
            if errors['hidden_layer_size'] == hls:
                plt.plot(range(1, len(errors['train_errors']) + 1), errors['train_errors'], label=f'Learning Rate: {errors["learning_rate"]}')
        plt.title(f'Train Errors for different Learning Rates, Hidden Layer Size: {hls}')
        plt.xlabel('Epoch')
        plt.ylabel('MSE')
        plt.legend()
        plt.show()

if should_analyze:
    analyze_models()

# Testowanie modelu w praktyce

lr = 0.001
hls = 100
epochs = 180

mlp = MLPRegressor(hidden_layer_sizes=(hls, ), solver='sgd', alpha=0.0, learning_rate_init=lr, random_state=42, max_iter=1, warm_start=True)
for _ in range(epochs):
    mlp.fit(X_train, y_train)

joke = "Q: What's the difference between a Lawyer and a Plumber? A: A Plumber works to unclog the system."

joke_encoded = model.encode([joke])
predicted_rating = mlp.predict(joke_encoded)

print(f"Predicted rating for the joke: {predicted_rating[0]}")

joke = "What's the difference between a used tire and 365 used condoms? One's a Goodyear, the other's a great year."

joke_encoded = model.encode([joke])
predicted_rating = mlp.predict(joke_encoded)


print(f"Predicted rating for the joke: {predicted_rating[0]}")
