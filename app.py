from flask import Flask, render_template_string, request, redirect, session
app = Flask(__name__)
app.secret_key = 'hao-jue-kalemie-2026-secret'
STOCK = {}
PIN_GERANT = "1234"
PIN_VENDEUR = "0000"

class Item:
    def __init__(self, qte, prix):
        self.qte = qte
        self.prix = prix

HTML_LOGIN = '''
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>HAOJUE - KALEMIE</title>
<style>
body { background:#e6f0ff; font-family:Arial; display:flex; justify-content:center; align-items:center; height:100vh; margin:0; }
.card { background:white; padding:30px; border-radius:15px; box-shadow:0 4px 15px rgba(0,0,0,0.1); width:85%; max-width:350px; text-align:center; }
h2 { color:#0b3d91; margin:0; }
input { width:100%; padding:12px; margin:15px 0; border:1px solid #ccc; border-radius:8px; font-size:16px; box-sizing:border-box; }
button { width:100%; padding:12px; background:#0b3d91; color:white; border:none; border-radius:8px; font-size:16px; font-weight:bold; }
</style></head>
<body><div class="card">
<h2>HAOJUE - KALEMIE</h2>
<p style="font-size:13px; color:#555;">Test 2 jours - Gérant remplit seul</p>
<h3>TANGA STOCK PRO</h3>
<form method="POST">
<input type="password" name="pin" placeholder="CODE PIN" required>
<button type="submit">Entrer</button>
</form>
</div></body></html>
'''

HTML_APP = '''
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:Arial; background:#f5f7ff; margin:0; padding:15px;}
.card{background:white; padding:15px; border-radius:12px; margin-bottom:15px;}
button{background:#0b3d91; color:white; border:none; padding:10px; border-radius:6px;}
table{width:100%; border-collapse:collapse;} th,td{border:1px solid #ddd; padding:8px;} th{background:#0b3d91; color:white;}</style>
</head><body>
<h2>HAOJUE - KALEMIE</h2><p>{{role}} | <a href="/logout">Deconnexion</a></p>
{% if role == 'Gérant' %}
<div class="card"><h3>Ajouter Stock</h3>
<form method="POST" action="/add">
<input name="nom" placeholder="Nom piece" required>
<input name="qte" type="number" placeholder="Qte" required>
<input name="prix" type="number" placeholder="Prix $" required>
<button>Ajouter</button></form></div>{% endif %}
<div class="card"><h3>Stock Actuel</h3>
<table><tr><th>Piece</th><th>Qte</th><th>Prix</th></tr>
{% for nom, data in stock.items() %}<tr><td>{{nom}}</td><td>{{data.qte}}</td><td>{{data.prix}} $</td></tr>{% endfor %}
</table></div></body></html>
'''

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        pin = request.form.get('pin','').strip()
        if pin == PIN_GERANT:
            session['role'] = 'Gérant'
            return redirect('/stock')
        elif pin == PIN_VENDEUR:
            session['role'] = 'Vendeur'
            return redirect('/stock')
    return render_template_string(HTML_LOGIN)

@app.route('/stock')
def stock_page():
    if 'role' not in session: return redirect('/')
    return render_template_string(HTML_APP, role=session['role'], stock=STOCK)

@app.route('/add', methods=['POST'])
def add_stock():
    if session.get('role')!= 'Gérant': return redirect('/')
    nom = request.form.get('nom').strip().upper()
    qte = int(request.form.get('qte',0))
    prix = float(request.form.get('prix',0))
    STOCK[nom] = Item(qte, prix) if nom not in STOCK else Item(STOCK[nom].qte+qte, prix)
    return redirect('/stock')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
