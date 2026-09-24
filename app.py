from flask import Flask, render_template_string, request, redirect, session
app = Flask(__name__)
app.secret_key = 'hao-jue-kalemie-2026-pro-secret'
STOCK = {}
PIN_GERANT = "1234"
PIN_VENDEUR = "0000"
class Item:
    def __init__(self,qte,prix):
        self.qte=qte;self.prix=prix
LOGIN_HTML='''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>HAOJUE - KALEMIE</title><style>body{background:#e6f0ff;font-family:Arial;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}.card{background:#fff;padding:30px;border-radius:16px;box-shadow:0 6px 20px rgba(0,0,0,.12);width:88%;max-width:360px;text-align:center}h2{color:#0b3d91;margin:0 0 5px}.sub{color:#666;font-size:13px;margin-bottom:15px}input{width:100%;padding:13px;margin:12px 0;border:1px solid #ccc;border-radius:10px;font-size:16px;box-sizing:border-box}button{width:100%;padding:13px;background:#0b3d91;color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:bold}</style></head><body><div class="card"><h2>HAOJUE - KALEMIE</h2><div class="sub">Test 2 jours - Gérant remplit seul</div><h3 style="color:#0b3d91">TANGA STOCK PRO</h3><form method="POST"><input type="password" name="pin" placeholder="CODE PIN" required><button>Entrer</button></form>{% if error %}<p style="color:red">{{error}}</p>{% endif %}</div></body></html>'''
DASH_HTML='''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>HAOJUE STOCK</title><style>body{font-family:Arial;background:#f2f5ff;margin:0;padding:12px}.header{background:#0b3d91;color:#fff;padding:14px;border-radius:12px;display:flex;justify-content:space-between}.card{background:#fff;padding:15px;border-radius:12px;margin-top:12px;box-shadow:0 2px 10px rgba(0,0,0,.06)}input,button{padding:11px;border-radius:8px;border:1px solid #ccc}button{background:#0b3d91;color:#fff;border:none;font-weight:bold}table{width:100%;border-collapse:collapse;margin-top:10px}th{background:#0b3d91;color:#fff;padding:10px}td{border:1px solid #e5e5e5;padding:9px}.msg{background:#d4edda;color:#155724;padding:10px;border-radius:8px;margin-top:10px}</style></head><body><div class="header"><div><b>HAOJUE - KALEMIE</b><br><small>{{role}}</small></div><div><a href="/logout" style="color:white">Déconnexion</a></div></div>{% if msg %}<div class="msg">{{msg}}</div>{% endif %}{% if role=='Gérant' %}<div class="card"><h3>Ajouter Stock</h3><form method="POST" action="/add"><input name="nom" placeholder="Nom pièce ex: BOUGIE" required><input name="qte" type="number" placeholder="Qté" required><input name="prix" type="number" step="0.01" placeholder="Prix $" required><button>Ajouter</button></form></div>{% endif %}<div class="card"><h3>Stock Actuel ({{stock|length}})</h3><table><tr><th>Pièce</th><th>Qté</th><th>Prix</th>{% if role=='Gérant' %}<th>X</th>{% endif %}</tr>{% for nom,data in stock.items() %}<tr><td><b>{{nom}}</b></td><td>{{data.qte}}</td><td>{{data.prix}} $</td>{% if role=='Gérant' %}<td><a href="/delete/{{nom}}" style="color:red">X</a></td>{% endif %}</tr>{% else %}<tr><td colspan="4" style="text-align:center;color:#888;padding:20px">Aucun stock</td></tr>{% endfor %}</table></div><div class="card"><h3>Vendre / Facturer</h3><form method="POST" action="/sell"><input name="nom" placeholder="Nom pièce" required><input name="qte" type="number" placeholder="Qté vendue" required><button>Vendre</button></form></div></body></html>'''
@app.route('/',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        pin=request.form.get('pin','').strip()
        if pin==PIN_GERANT:
            session['role']='Gérant';return redirect('/stock')
        elif pin==PIN_VENDEUR:
            session['role']='Vendeur';return redirect('/stock')
        else:error="Code incorrect"
    return render_template_string(LOGIN_HTML,error=error)
@app.route('/stock')
def stock():
    if 'role' not in session:return redirect('/')
    return render_template_string(DASH_HTML,role=session['role'],stock=STOCK,msg=request.args.get('msg'))
@app.route('/add',methods=['POST'])
def add():
    if session.get('role')!='Gérant':return redirect('/stock')
    nom=request.form.get('nom','').strip().upper();qte=int(request.form.get('qte',0));prix=float(request.form.get('prix',0))
    if nom in STOCK:STOCK[nom].qte+=qte;STOCK[nom].prix=prix
    else:STOCK[nom]=Item(qte,prix)
    return redirect('/stock?msg=Ajoute:'+nom)
@app.route('/delete/<nom>')
def delete(nom):
    if session.get('role')!='Gérant':return redirect('/stock')
    STOCK.pop(nom,None);return redirect('/stock?msg=Supprime')
@app.route('/sell',methods=['POST'])
def sell():
    nom=request.form.get('nom','').strip().upper();qte=int(request.form.get('qte',0))
    if nom in STOCK and STOCK[nom].qte>=qte:
        STOCK[nom].qte-=qte;total=qte*STOCK[nom].prix
        return redirect(f'/stock?msg=VENTE+{qte}x{nom}={total}$+OK')
    return redirect('/stock?msg=Stock+insuffisant')
@app.route('/logout')
def logout():
    session.clear();return redirect('/')
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
