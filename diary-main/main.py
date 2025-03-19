#Import
from flask import Flask, render_template, request, redirect
#Datenbank-Bibliothek einbinden
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#SQLite einbinden
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Datenbank erstellen
db = SQLAlchemy(app)
#Tabelle erstellen

class Card(db.Model):
    #Felder erstellen
    #id
    id = db.Column(db.Integer, primary_key=True)
    #Titel
    title = db.Column(db.String(100), nullable=False)
    #Beschreibung
    subtitle = db.Column(db.String(300), nullable=False)
    #Text
    text = db.Column(db.Text, nullable=False)

    #Objekt und ID ausgeben
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Aufgabe Nr.1: Tabelle "User" erstellen
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)



#Seite mit Inhalt starten
@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            #Aufgabe Nr.4: Benutzerauthentifizierung implementieren
            users_db = User.query.all()
            for user in users_db:
                if form_login == user.login and form_password == user.password:
                    return redirect('/index')
            else:
                error = 'Falscher Benutzername oder Passwort'
                return render_template('login.html', error=error)
        
        else:
            return render_template('login.html')


@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login= request.form['email']
        password = request.form['password']
        
        #Aufgabe Nr.3: Benutzerregistrierung implementieren
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


#Seite mit Inhalt starten
@app.route('/index')
def index():
    #Objekte aus der Datenbank anzeigen
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

#Seite mit Karte starten
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)
    print(f"DEBUG: card.text = {card.text}")  # Prüfen, ob Text vorhanden ist
    return render_template('card.html', card=card)

#Seite zum Erstellen einer Karte starten
@app.route('/create')
def create():
    return render_template('create_card.html')

#Kartenformular
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        #Objekt zur Speicherung in der Datenbank erstellen
        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')




if __name__ == "__main__":
    app.run(debug=True)
