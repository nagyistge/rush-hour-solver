import os

from flask import Flask, request
from solver import Solver, WrongInputException, CanNonSolveException

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def main():
    """
    Sample code to show Rush hour solver on web.
    Templates are not used for simplicity.
    """
    if request.method == 'POST':
        board_str = request.form['board']

        if board_str:
            try:
                solver = Solver()
                solver.load_data(board_str)
                moves = solver.solve()
                response = solver.format_steps(solver.cars, moves)
            except CanNonSolveException as e:
                return "Can not solve this board ({})</br>".format(e.message) +\
                    "<a href='/'>Try another board</a>"
            except WrongInputException as e:
                return "Can not load this board ({})</br>".format(e.message) +\
                    "<a href='/'>Try another board</a>"

            return "<pre>{}</pre></br><a href='/'>Try another board</a>".format(response)

    resp_text = '''
        <form method="POST" style="text-align: center">
            <h2>Rush hour solver online (6x6)</h2>
            <p>
            <br/>
            <a target="_blank" href="https://github.com/yrik/rush-hour-solver">See source code here</a>
            </p>
            <textarea name='board' rows="6" cols="6" style="font-family: monospace;font-size:2em;">
....AA
..BBCC
rr..EF
GGHHEF
...IEF
...IJJ
            </textarea>
            <br/>
            <input type="submit" value="Submit (will take some time)" style="font-size:2em;"/>
            <br/>
            <br/>
            Note: for some complex board it may take more than 30s, in that case heroku will stop excecution.
        </form>
    '''
    return resp_text

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
