from server import app,loadClubs,loadCompetitions
import pytest
import json
from flask import Flask,render_template

@pytest.fixture
def test():
    app.config['TEST'] = True
    with app.test_client() as test:
        yield test

def test_home_page_returns_correect_html(test):
    response = test.get('/')
    assert response.status_code == 200
    assert b'<input' in response.data

def test_summary_valide(test):
    rv = test.post('/showSummary', data={"email":"admin@irontemple.com"}, follow_redirects=True)
    assert rv.status_code==200
    data = rv.data.decode()
    assert "Welcome, admin@irontemple.com" in data

def test_summary_invalide(test):
    rv = test.post('/', data={"email":"admin@admin.com"}, follow_redirects=True)
    assert rv.status_code==405
    assert rv.data.decode().find("Désolé cet email n'a pas été trouvé") 


       

def test_clubs_competion_booking_valide(test):
    rv = test.post('/showSummary', data={"email":"kate@shelifts.co.uk"}, follow_redirects=True)
    assert rv.status_code==200
    data = rv.data.decode()
    assert "/book/Spring%20Festival/She%20Lifts" in data


def test_clubs_competion_booking_invalide(test):
    rv = test.get('/book/Spring%20Festival/She%20Liftsinvalide',follow_redirects=True)
    assert rv.status_code==200
    data = rv.data.decode()
    assert "Welcome to the GUDLFT Registration Portal!" in data


def test_user_club_point(test):
    rv = test.post('/showSummary', data={"email":"admin@irontemple.com"}, follow_redirects=True)
    assert rv.status_code==200
    rv_test= test.get('/book/Spring%20Festival/She%20Lifts',follow_redirects=True)
    assert rv_test.status_code==200
    rv_test=test.post('/purchasePlaces', data =dict(club = 'Iron Temple', competition='Spring Festival', places = 5), follow_redirects = True)
    data =rv_test.data.decode()
    assert 'Number of Places: 20' in data
    assert 'Points available: 4' in data

def test_nbplace_invalide(test):
    rv = test.post('/showSummary', data={"email":"admin@irontemple.com"}, follow_redirects=True)
    assert rv.status_code==200
    rv_test= test.get('/book/Spring%20Festival/She%20Lifts',follow_redirects=True)
    assert rv_test.status_code==200
    rv_test=test.post('/purchasePlaces', data =dict(club = 'Iron Temple', competition='Spring Festival', places = 13), follow_redirects = True)
    data =rv_test.data.decode()
    assert 'Too many places requiered' in data

def test_points_invalide(test):
    rv = test.post('/showSummary', data={"email":"john@simplylift.co"}, follow_redirects=True)
    assert rv.status_code==200
    rv_test= test.get('/book/Spring%20Festival/Simply%20Lift',follow_redirects=True)
    assert rv_test.status_code==200
    rv_test=test.post('/purchasePlaces', data =dict(club = 'Simply Lift', competition='Spring Festival', places = 10), follow_redirects = True)
    data =rv_test.data.decode()
    assert 'Not enought points !' in data

def test_logout(test):
    rv = test.post('/showSummary', data={"email":"admin@irontemple.com"}, follow_redirects=True)
    assert rv.status_code==200
    rv_logout = test.get("/logout", follow_redirects=True)
    assert rv_logout.status_code == 200
    data= rv_logout.data.decode()
    assert 'Welcome to the GUDLFT Registration Portal!' in data

def test_score_disconnect(test):
    rv_logout = test.get("/score", follow_redirects=True)
    assert rv_logout.status_code == 200
    data= rv_logout.data.decode()
    assert 'Welcome to the Score and Points Portal!' in data

def test_score_connected(test):
    rv = test.post('/showSummary', data={"email":"admin@irontemple.com"}, follow_redirects=True)
    assert rv.status_code==200 
    rv_logout = test.get("/score", follow_redirects=True)
    assert rv_logout.status_code == 200
    data= rv_logout.data.decode()
    assert 'Welcome to the Score and Points Portal!' in data


def test_amount_invalide(test):
    rv = test.post('/showSummary', data={"email":"john@simplylift.co"}, follow_redirects=True)
    assert rv.status_code==200
    rv_test= test.get('/book/Spring%20Festival/Simply%20Lift',follow_redirects=True)
    assert rv_test.status_code==200
    rv_test=test.post('/purchasePlaces', data =dict(club = 'Simply Lift', competition='Spring Festival', places = 0), follow_redirects = True)
    data =rv_test.data.decode()
    assert 'Invalid amount of requiered places' in data

def test_place_invalide(test):
    rv = test.post('/showSummary', data={"email":"john@simplylift.co"}, follow_redirects=True)
    assert rv.status_code==200
    rv_test= test.get('/book/Spring%20Festival/Simply%20Lift',follow_redirects=True)
    assert rv_test.status_code==200
    rv_test=test.post('/purchasePlaces', data =dict(club = 'Simply Lift', competition='Spring Festival', places = 50), follow_redirects = True)
    data =rv_test.data.decode()
    assert "Not enought places availible !" in data

def test_date_invalide(test):
    rv = test.post('/showSummary', data={"email":"john@simplylift.co"}, follow_redirects=True)
    assert rv.status_code==200
    rv_test= test.get('/book/Fall%20Classic/Simply%20Lift',follow_redirects=True)
    assert rv_test.status_code==200
    rv_test=test.post('/purchasePlaces', data =dict(club = 'Simply Lift', competition='Fall Classic', places = 2), follow_redirects = True)
    data =rv_test.data.decode()
    assert "La date de la compétition est déjà passé" in data


def test_integration(test):
    club= loadClubs()
    assert list(club[0].keys())==['name','email','points','solde']
    competitions = loadCompetitions()
    assert list(competitions[0].keys())==['name','date','numberOfPlaces']

    response = test.get('/')
    assert response.status_code == 200
    assert b'<input' in response.data

    rv = test.post('/showSummary', data={"email":"admin@irontemple.com"}, follow_redirects=True)
    assert rv.status_code==200
    data = rv.data.decode()
    assert "Welcome, admin@irontemple.com" in data

    rv_test= test.get('/book/Spring%20Festival/Simply%20Lift',follow_redirects=True)
    assert rv_test.status_code==200
    assert "Spring Festival" in data

    rv_test=test.post('/purchasePlaces', data =dict(club = 'Simply Lift', competition='Spring Festival', places = 2), follow_redirects = True)
    data =rv_test.data.decode()
    assert "Great-booking complete!" in data

    rv_logout = test.get("/logout", follow_redirects=True)
    assert rv_logout.status_code == 200
    data= rv_logout.data.decode()
    assert 'Welcome to the GUDLFT Registration Portal!' in data

















