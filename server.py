import json,datetime,time
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime
import sys


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/score')
def index_score():
    lesclub = [lesclub for lesclub in clubs]
    return render_template('score.html',clubs=clubs)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]

    if club:
        club_email = club[0]
        return render_template('welcome.html',club=club_email, competitions=competitions)
    else:
        return render_template('index.html', error="Désolé cet email n'a pas été trouvé")

@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club ][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
    except:
        return render_template('index.html')

    
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])

        if int(club["solde"]) < (placesRequired*3) and (placesRequired<12):
            flash("Not enought points !")
        
        elif int(placesRequired) > 12 and (placesRequired)<26:
            flash('Too many places requiered')

        elif int(placesRequired) <= 0:
            flash('Invalid amount of requiered places')
        
        elif placesRequired > int(competition["numberOfPlaces"]):
            flash("Not enought places availible !")

        elif int(datetime.timestamp(datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S"))) <= int(datetime.timestamp(datetime.now())):
            flash("La date de la compétition est déjà passé")

        elif int(club["solde"]) > 0:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['solde'] = int(club['solde']) - (placesRequired*3)
            #club['solde'] = club['points']
            flash('Great-booking complete!')
    except Exception as error:
        flash("Something went wrong-please try again")
    return render_template('welcome.html', club=club, competitions=competitions), 403
        

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/score')
def score():
    return redirect(url_for('index_score'))



if __name__ == '__main__':
    app.run(debug=True)