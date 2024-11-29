from flask import Flask, request, jsonify, send_from_directory
from scipy.spatial.distance import squareform
from scipy.optimize import linear_sum_assignment
from flask import render_template
import numpy as np
import os

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

print(GOOGLE_MAPS_API_KEY)
app = Flask(__name__, static_folder='static', template_folder='templates')

# Example Python function to solve TSP using a greedy algorithm
def solve_tsp(distance_matrix):
    n = len(distance_matrix)
    best_route = None
    best_cost = float('inf')

    # Try starting at each location and compute the cost
    for start in range(n):
        visited = [False] * n
        route = [start]
        visited[start] = True
        current_cost = 0

        # Greedy TSP logic
        for _ in range(1, n):
            last = route[-1]
            next_city = int(np.argmin([distance_matrix[last][j] if not visited[j] else np.inf for j in range(n)]))
            route.append(next_city)
            visited[next_city] = True
            current_cost += distance_matrix[last][next_city]

        # Complete the loop by returning to the starting point
        current_cost += distance_matrix[route[-1]][start]

        # Update the best solution
        if current_cost < best_cost:
            best_cost = current_cost
            best_route = route

    return best_route


@app.route('/solve-tsp', methods=['POST'])
def solve_tsp_route():
    data = request.get_json()
    distance_matrix = data['distances']

    # Solve the TSP using the provided distance matrix
    route = solve_tsp(distance_matrix)
    return jsonify({"route": route})

@app.route('/')
def serve_home():
    return render_template('index.html', api_key=GOOGLE_MAPS_API_KEY)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
