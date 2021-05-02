import csv
from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
from tempfile import mkdtemp
import random

app = Flask(__name__)
app.secret_key = "unwintoe"


def check(li, f, ch):
    flag = f

    # horizontal checking
    for i in range(3):
        co = 0
        for j in range(3):
            if li[i][j] == ch:
                co += 1
        if co == 2 and flag == 0:
            for k in range(3):
                if li[i][k] == None:
                    li[i][k] = "O"
                    flag = 1
                    check(li, flag, ch)
                    return 1
        if co == 3:
            winner = ch
            return ch

    # vertical checking
    for i in range(3):
        c1 = 0
        for j in range(3):
            if li[j][i] == ch:
                c1 += 1
        if c1 == 2 and flag == 0:
            for k in range(3):
                if li[k][i] == None:
                    li[k][i] = "O"
                    flag = 1
                    check(li, flag, ch)
                    return 1
        if c1 == 3:
            winner = ch
            return ch

    # diagonal checking
    c3 = 0
    for i in range(3):
        if li[i][i] == ch:
            c3 += 1
            a = i
            b = i
    if c3 == 2 and flag == 0:
        for k in range(3):
            if li[k][k] == None:
                li[k][k] = "O"
                flag = 1
                check(li, flag, ch)
                return 1
    if c3 == 3:
        winner = ch
        return ch

    # diagonal 2 checking
    j = 2
    c4 = 0
    for i in range(3):
        if li[i][j] == ch:
            c4 += 1
            a = i
            b = j
        j -= 1
    if c4 == 2 and flag == 0:
        j = 2
        for k in range(3):
            if li[k][j] == None:
                li[k][j] = "O"
                flag = 1
                check(li, flag, ch)
                return 1
            j -= 1
    if c4 == 3:
        winner = ch
        return ch

    # Counter over. Code for game play
    if flag == 0 and ch == "O":
        if (c3 == 1 or c4 == 1) and li[2-a][2-b] == None:
            li[2-a][2-b] = "O"
            flag = 1
            return

    # to return to counter O, to first counter from 2nd counter
    if flag == 0 and ch == "X":
        return 0

    # to send to counter X
    if flag == 0 and ch == "O":
        flag = check(li, flag, "X")

    # sanity check
    if flag == 4 and ch == "O":
        flag = check(li, flag, "X")

    if flag == "O" or flag == "X":
        return flag

    if flag == 0:
        for i in range(0, 3, 2):
            for j in range(0, 3, 2):
                if li[i][j] == None:
                    li[i][j] = "O"
                    flag = 1
                    fn = check(li, flag, "O")
                    return fn
    if flag == 0:
        for i in range(3):
            for j in range(3):
                if li[i][j] == None:
                    li[i][j] = "O"
    # DRAW
    flag1 = 0
    for i in range(3):
        for j in range(3):
            if li[i][j] == None:
                flag1 = 1
    if flag1 == 0:
        return 3


# username = None
# game = None
score_comp = 0
score_player = 0


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template("index.html")

    else:

        username = request.form.get("username")
        session["username"] = username
        # print(username)

        # with open("users.csv", mode="a") as users_file:
        #     users = csv.writer(users_file)
        #     users.writerow(username)

        return redirect("/start")


@app.route("/start")
def start():
    global score_comp
    global score_player
    # global game
    # global username

    if "board" not in session:
        score_comp = 0
        score_player = 0
        game = [[None, None, None], [None, None, None], [None, None, None]]
        session["toe"] = game
        turn = "X"
        a = random.randrange(0, 3, 2)
        b = random.randrange(0, 3, 2)
        game[a][b] = "O"

    return render_template("game.html", game=game, username=session["username"], sc=score_comp, su=score_player)


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    fl = 0
    global score_comp
    global score_player, username
    game = session["toe"]
    game[row][col] = "X"
    session["toe"] = game
    fl = check(game, 0, "O")

    # this is just to check for winner
    fl = check(game, 4, "O")

    if fl == "O":
        score_comp += 1
        return render_template("win.html", game=game, winner="Computer", sc=score_comp, su=score_player, username=session["username"])
    elif fl == "X":
        score_player += 1
        return render_template("win.html", game=game, winner=session["username"], sc=score_comp, su=score_player)
    elif fl == 3:
        return render_template("draw.html", game=game, sc=score_comp, su=score_player, username=session["username"])
    else:
        return render_template("game.html", game=game, sc=score_comp, su=score_player, username=session["username"])


@app.route("/reset")
def reset():
    global score_comp
    global score_player, username
    game = [[None, None, None], [None, None, None], [None, None, None]]
    session["toe"] = game
    turn = "X"
    a = random.randrange(0, 3, 2)
    b = random.randrange(0, 3, 2)
    game[a][b] = "O"

    return render_template("game.html", game=session["toe"], sc=score_comp, su=score_player, username=session["username"])


@app.route("/about")
def about():

    return render_template("about.html")
