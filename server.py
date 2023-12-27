from http import HTTPStatus
import json
from flask import Flask, render_template, request, redirect, flash, url_for
from utils import EmailError, BookingError, search_club_by_email, check_booking_validity


def load_clubs():
    """Load clubs from JSON file."""
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    """Load competitions from JSON file."""
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')


@app.route('//showSummary', methods=['POST'])
def show_summary():
    """Show summary page based on provided email."""
    try:
        club = search_club_by_email(request.form['email'], clubs)
        return render_template('welcome.html', club=club, competitions=competitions)
    except EmailError as e:
        flash(e.message)
        return render_template("index.html"), HTTPStatus.BAD_REQUEST


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """Render booking page for a competition and club."""
    try:
        found_club = [c for c in clubs if c["name"] == club][0]
        found_competition = [c for c in competitions if c["name"] == competition][0]
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions), HTTPStatus.BAD_REQUEST


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    """Process the purchase of places for a competition and club."""
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    try:
        check_booking_validity(competition, places_required, club)
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        # Update available points
        club['points'] = int(club['points']) - places_required
        flash('Great-booking complete!')
        http_result = HTTPStatus.OK
    except BookingError as error:
        flash(error)
        http_result = HTTPStatus.BAD_REQUEST
    return render_template('welcome.html', club=club, competitions=competitions), http_result


@app.route("/displayPoints", methods=["GET"])
def display_points():
    """Display points for clubs."""
    return render_template("points.html", clubs=clubs)


@app.route('/logout')
def logout():
    """Logout and redirect to the index page."""
    return redirect(url_for('index'))
