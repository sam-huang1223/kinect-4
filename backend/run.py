from AI import Connect4 as c4

import requests, numpy
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# STORAGE
INFO = {
    'state': {'round': 1, 'wait-confirm': 0, 'turn': 'PC'},
    'game': None, 
    'possible-moves': [],
    'human-moves': [],
    'ai-moves': []
}

def tryMove(human_move):
    INFO['possible-moves'] = c4.generate_moves(INFO['game'].state)
    if not (0 <= human_move <= 6): return 'invalid'
    elif INFO['possible-moves'] == []: return 'tie'
    elif human_move not in INFO['possible-moves']: return 'invalid'
    INFO['game'].state = c4.modify_state(INFO['game'].state, human_move, INFO['game'].human)
    return True

def findMove():
    # Decide AI move
    algorithm = c4.Alpha_Beta_Pruning.Minimax([INFO['game'].nodes, INFO['game'].edges], False)
    ai_move = int(algorithm.path[1][-1])

    # Apply AI move
    INFO['game'].state = c4.modify_state(INFO['game'].state, ai_move, INFO['game'].ai)

# CLASSES

class Board(Resource):
    def get(self):
        return INFO['game'].state.tolist(), 201

    def post(self, move):
        if(move == 9):
            INFO['state']['round'] += 1
            findMove()
            if INFO['game'].evaluate(INFO['game'].state, INFO['game'].ai, c4.generate_moves(INFO['game'].state) == 0) == c4.constant:
                return INFO['game'].state.tolist(), 203 # ai win
            return INFO['game'].state.tolist(), 201
        else:
            if(tryMove(move)):
                INFO['state']['round'] += 1
                if INFO['game'].evaluate(INFO['game'].state, INFO['game'].human, c4.generate_moves(INFO['game'].state) == 0) == -c4.constant:
                    return INFO['game'].state.tolist(), 203 # human win
                return INFO['game'].state.tolist(), 201
            else:
                return 'invalid', 201

class Game(Resource):
    def get(self):
        return INFO['state']
    
    def put(self):
        INFO['game'] = c4.startGame('alpha beta pruning')
        return '', 201

# ADDS
# api.add_resource(Resource, urls, endpoint=Resource.__name__.lower())
api.add_resource(Board, '/board/<int:move>')
api.add_resource(Game, '/game')

# RUN
if __name__ == '__main__':
    '''
    def play(algo_selection):
        while True:
            human_move_values = []
            ai_move_values = []
            possible_human_moves = generate_moves(game.state)
            try:
                human_move = int(input('Please enter your next move (0-6): '))
            except ValueError:
                print('Invalid move. Please enter another move')
                continue
            if human_move == -1:
                print('Thank you for playing!')
                break
            elif possible_human_moves == []:
                print('TIE')
                break
            elif human_move not in possible_human_moves:
                print('Invalid move. Please enter another move')
                continue
            game.state = modify_state(game.state, human_move, game.human)

            print(notuglyprint(game.state))

            if game.evaluate(game.state, game.human, generate_moves(game.state) == 0) == -constant:
                print('HUMAN WON')
                break

            game = Connect4(board=game.state)
            algorithm = Alpha_Beta_Pruning.Minimax([game.nodes, game.edges], False)
            ai_move = int(algorithm.path[1][-1])

            print('AI move:', ai_move)
            game.state = modify_state(game.state, ai_move, game.ai)
            print(notuglyprint(game.state))

            if game.evaluate(game.state, game.ai, generate_moves(game.state) == 0) == constant:
                print('AI WON')
                break

            human_move_value = game.evaluate(game.state, game.human, possible_human_moves == [])
            human_move_values.append(human_move_value)
            print('Human value:', human_move_value)

            ai_move_value = game.evaluate(game.state, game.ai, generate_moves(game.state) == 0)
            ai_move_values.append(ai_move_value)
            print('AI value:', ai_move_value)
            ai_win_prob = ai_move_value / (ai_move_value + human_move_value)
            print('AI probability of winnning:', ai_win_prob)
    '''
    app.run(debug=True)