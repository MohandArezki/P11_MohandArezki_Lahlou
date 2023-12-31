from http import HTTPStatus
import json
from flask import Flask,render_template,request,redirect,flash,url_for
from utils import EmailError,BookingError, search_club_by_email, check_booking_validity

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

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = search_club_by_email(request.form['email'],clubs)
        return render_template('welcome.html',club=club,competitions=competitions)
    except EmailError as e:
        flash(e.message)
        return render_template("index.html"), HTTPStatus.BAD_REQUEST


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
        return render_template(
                "booking.html", club=foundClub, competition=foundCompetition
            )
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions), HTTPStatus.BAD_REQUEST



@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])    
    try:
        check_booking_validity(competition, placesRequired, club)
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        # Update available points    
        club['points'] = int(club['points']) - placesRequired
        flash('Great-booking complete!')
        httpResult = HTTPStatus.OK
    except BookingError as error:
        flash(error)
        httpResult = HTTPStatus.BAD_REQUEST  
    return render_template('welcome.html', club=club, competitions=competitions), httpResult



@app.route("/displayPoints", methods=["GET"])
def displayPoints():
    # display points
    return render_template("points.html", clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))