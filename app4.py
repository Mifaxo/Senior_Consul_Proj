# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 11:41:14 2026

@author: pasto
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="BPCE - Votre Espace", layout="wide", page_icon="🏦")

st.markdown("""
    <style>
    /* Boutons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
    }
    
    /* Carte Compte Standard */
    .metric-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #eee;
        transition: transform 0.2s;
    }
    .metric-container:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .metric-container h2 { color: #2c3e50; margin-bottom: 0;}
    
    /* Carte Total Avoirs (Nouveau) */
    .total-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: left;
        margin-bottom: 20px;
    }
    .total-card h1 { color: white; margin: 0; font-size: 2.5em; }
    .total-card p { margin: 0; opacity: 0.8; font-size: 1.1em; }

    /* Carte Recommandation */
    .reco-card {
        padding: 15px; border: 1px solid #ddd; border-radius: 10px; height: 100%; background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Carte Bancaire Visuelle */
    .card-visual {
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        height: 200px;
        position: relative;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Notifications */
    .notif-box {
        padding: 10px;
        border-left: 3px solid #2196F3;
        background-color: #f1f8ff;
        margin-bottom: 10px;
        font-size: 0.9em;
    }
    
    /* Footer (Nouveau) */
    .footer {
        margin-top: 80px;
        padding-top: 20px;
        border-top: 1px solid #e0e0e0;
        text-align: center;
        color: #666;
        font-size: 0.85em;
    }
    .footer a {
        color: #666;
        text-decoration: none;
        margin: 0 10px;
    }
    .footer a:hover {
        color: #004e92;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'accueil'

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

def get_dummy_data():
    profil = {
        "nom": "Dupont", "prenom": "Jean", "risque": "Modéré", 
        "epargne_actuelle": 15000, "salaire_net": 3200
    }
    comptes = pd.DataFrame([
        {"Type": "Compte Courant", "Solde": 2450.50, "IBAN": "FR76 1234..."},
        {"Type": "Livret A", "Solde": 12000.00, "IBAN": "FR76 5678..."},
        {"Type": "PEA (Bourse)", "Solde": 5400.00, "IBAN": "FR76 9012..."}
    ])
    
    categories = ["Alimentation", "Logement", "Transports", "Loisirs", "Abonnements", "Shopping", "Santé", "Restaurants"]
    data = []
    data.append({"Catégorie": "Revenus", "Montant": 3200.00, "Date": datetime.now().replace(day=1), "Type": "Crédit"})
    data.append({"Catégorie": "Logement", "Montant": 950.00, "Date": datetime.now().replace(day=5), "Type": "Débit"})
    
    for _ in range(150):
        cat = random.choice(categories)
        if cat == "Logement": continue 
        base_amount = random.uniform(5, 120)
        if cat == "Alimentation": base_amount *= 1.5
        if cat == "Shopping": base_amount *= 2.0
        
        random_day = random.randint(1, 28)
        date_transac = datetime.now().replace(day=random_day)
        data.append({"Catégorie": cat, "Montant": round(base_amount, 2), "Date": date_transac, "Type": "Débit"})
    
    df_depenses = pd.DataFrame(data)
    return profil, comptes, df_depenses

def generate_market_data(start_price, trend_seed, volatility, name):
    days = 365
    dates = [datetime.today() - timedelta(days=x) for x in range(days)]
    dates.reverse()
    np.random.seed(trend_seed)
    returns = np.random.normal(loc=0.0003, scale=volatility, size=days)
    price_path = start_price * np.cumprod(1 + returns)
    return pd.DataFrame({"Date": dates, "Close": price_path, "Indice": name})

# Initialisation
if 'profil' not in st.session_state:
    st.session_state.profil, st.session_state.comptes, st.session_state.depenses = get_dummy_data()
    st.session_state.cac40 = generate_market_data(7000, trend_seed=42, volatility=0.008, name="CAC 40")
    st.session_state.sp500 = generate_market_data(4500, trend_seed=12, volatility=0.007, name="S&P 500")
    st.session_state.nasdaq = generate_market_data(14000, trend_seed=7, volatility=0.012, name="Nasdaq-100")
if 'dialog_shown' not in st.session_state:
    st.session_state.dialog_shown = False

@st.dialog("🔔 Briefing Mensuel IA")
def show_monthly_briefing():
    st.write(f"Bonjour {st.session_state.profil['prenom']}, votre assistant IA a analysé votre mois. Que souhaitez-vous faire ?")
    c1, c2, c3 = st.columns(3)
    if c1.button("💬 Conseiller"):
        st.session_state.dialog_shown = True
        st.toast("Demande transmise.", icon="✅")
        st.rerun()
    if c2.button("📊 Rapport IA", type="primary"):
        st.session_state.dialog_shown = True
        navigate_to('report')
    if c3.button("📅 Plus tard"):
        st.session_state.dialog_shown = True
        st.rerun()

def generate_ai_recommendations(df, profil):
    df_debit = df[df['Type'] == 'Débit']
    total_depenses = df_debit['Montant'].sum()
    cats = df_debit.groupby('Catégorie')['Montant'].sum()
    
    recos = []
    if cats.get('Restaurants', 0) > 300:
        recos.append({"titre": "Budget Restaurants", "msg": f"Vous avez dépensé {cats['Restaurants']:.0f}€. Cuisiner 2 repas de plus par semaine économiserait ~80€.", "action": "Défi Cuisine", "type": "eco", "color": "#2196F3", "icon": "🍳"})
    if cats.get('Transports', 0) > 150:
        recos.append({"titre": "Optimisation Transports", "msg": "Vos frais de transport sont élevés. Un pass annuel ou l'usage du vélo pourrait réduire ce poste de 40%.", "action": "Comparer les offres", "type": "eco", "color": "#2196F3", "icon": "🚇"})
    if cats.get('Shopping', 0) > 400:
        recos.append({"titre": "Shopping & Impulsion", "msg": "Pic de dépenses shopping détecté. Appliquez la règle des 24h avant tout achat > 50€.", "action": "Activer alerte seuil", "type": "eco", "color": "#2196F3", "icon": "🛍️"})
    
    reste = profil['salaire_net'] - total_depenses
    epargne_suggeree = 0
    if reste > 300:
        epargne_suggeree = reste * 0.6
        recos.append({"titre": "Boost Épargne", "msg": f"Le mois est positif (+{reste:.0f}€). Sécurisez immédiatement une partie de ce surplus.", "action": f"Virer {epargne_suggeree:.0f}€ vers Livret A", "type": "placement", "color": "#4CAF50", "icon": "💰"})
    
    if profil['risque'] in ["Modéré", "Audacieux"]:
        recos.append({"titre": "Opportunité PEA", "msg": "Le secteur technologique (Nasdaq) surperforme. Diversifiez votre épargne long terme.", "action": "Investir 200€ ETF Tech", "type": "bourse", "color": "#FF9800", "icon": "📈"})
        
    return total_depenses, recos, epargne_suggeree, reste

with st.sidebar:
    st.image("bpce.png", width=150)
    st.title("Votre Espace")
    st.write(f"Bonjour, **{st.session_state.profil['prenom']}**")
    st.markdown("---")
    
    if st.button("🏠 Accueil", type="secondary" if st.session_state.page != 'accueil' else "primary"): navigate_to('accueil')
    if st.button("💳 Comptes & Cartes", type="secondary" if st.session_state.page != 'comptes' else "primary"): navigate_to('comptes')
    st.button("📈 Mes Placements")
    if st.button("🤖 Rapport IA", type="secondary" if st.session_state.page != 'report' else "primary"): navigate_to('report')
    
    st.markdown("---")
    if st.button("🔄 Reset Démo"):
        st.session_state.dialog_shown = False
        st.session_state.page = 'accueil'
        st.rerun()

if not st.session_state.dialog_shown:
    show_monthly_briefing()

if st.session_state.page == 'accueil':
    st.title("Tableau de Bord")
    
    col_total, col_notif = st.columns([2, 1])
    
    with col_total:
        total_avoirs = st.session_state.comptes['Solde'].sum()
        st.markdown(f"""
        <div class="total-card">
            <p>Total de vos avoirs</p>
            <h1>{total_avoirs:,.2f} €</h1>
        </div>
        """, unsafe_allow_html=True)
        
    with col_notif:
        with st.container(border=True, height=130):
            st.markdown("#### 🔔 Notifications")
            st.markdown("""
            <div style="font-size: 0.9em;">
            • <b>Sécurité :</b> Connexion détectée (Paris).<br>
            • <b>Conseil :</b> Rapport mensuel disponible.
            </div>
            """, unsafe_allow_html=True)

    st.subheader("Mes Comptes")
    cols = st.columns(3)
    for index, row in st.session_state.comptes.iterrows():
        with cols[index % 3]:
            st.markdown(f"""
            <div class="metric-container">
                <h4>{row['Type']}</h4>
                <h2>{row['Solde']:,.2f} €</h2>
                <small style="color: gray;">{row['IBAN']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.write("") 
    st.subheader("Accès Rapide")
    q1, q2, q3, q4 = st.columns(4)
    if q1.button("💳 Mes Cartes"): navigate_to('comptes')
    if q2.button("💸 Faire un virement"): navigate_to('comptes')
    if q3.button("🤖 Mon Coach IA"): navigate_to('report')
    if q4.button("📁 Mes Documents"): pass

elif st.session_state.page == 'comptes':
    st.title("Comptes & Opérations")
    
    tab1, tab2, tab3 = st.tabs(["📜 Historique", "💸 Virements", "💳 Mes Cartes"])
    
    with tab1:
        st.subheader("Dernières opérations")
        df_display = st.session_state.depenses.sort_values(by="Date", ascending=False)
        col_f1, col_f2 = st.columns(2)
        with col_f1: cat_filter = st.multiselect("Filtrer par catégorie", df_display['Catégorie'].unique())
        if cat_filter: df_display = df_display[df_display['Catégorie'].isin(cat_filter)]
        st.dataframe(df_display, column_config={"Date": st.column_config.DatetimeColumn(format="D MMM YYYY"), "Montant": st.column_config.NumberColumn(format="%.2f €")}, use_container_width=True, hide_index=True)
        
    with tab2:
        st.subheader("Effectuer un virement")
        with st.container(border=True):
            c_vir1, c_vir2 = st.columns(2)
            with c_vir1:
                st.selectbox("Compte à débiter", st.session_state.comptes['Type'])
                st.selectbox("Compte bénéficiaire", ["Nouveau bénéficiaire"] + list(st.session_state.comptes['Type']))
            with c_vir2:
                st.number_input("Montant (€)", min_value=1.0)
                st.text_input("Libellé (Optionnel)")
            if st.button("Valider le virement", type="primary"): st.success("Virement effectué avec succès !")

    with tab3:
        st.subheader("Gestion des Cartes")
        col_card, col_opts = st.columns([1, 2])
        with col_card:
            st.markdown(f"""
            <div class="card-visual">
                <h3 style="margin:0;">BPCE</h3>
                <p>GOLD PREMIUM</p>
                <p style="margin-top: 50px; font-family: monospace; font-size: 1.2em;">**** **** **** 4242</p>
                <div style="display:flex; justify-content:space-between;">
                    <span>{st.session_state.profil['nom'].upper()}</span>
                    <span>12/28</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_opts:
            st.toggle("🔒 Verrouiller temporairement la carte", value=False)
            st.toggle("🌍 Paiements à l'étranger", value=True)
            st.slider("Plafond de retrait (Hebdo)", 200, 2000, 500, step=100)

elif st.session_state.page == 'report':
    st.title("🤖 Rapport d'Analyse IA")
    total_spent, recommendations, suggestion_epargne_montant, reste_a_vivre = generate_ai_recommendations(st.session_state.depenses, st.session_state.profil)
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Dépenses du mois", f"{total_spent:,.2f} €")
    k2.metric("Reste à vivre estimé", f"{reste_a_vivre:,.2f} €", help="Revenus - Dépenses du mois.")
    k3.metric("Taux d'épargne pot.", f"{(reste_a_vivre/st.session_state.profil['salaire_net'])*100:.1f} %")

    fig_pie = px.pie(st.session_state.depenses[st.session_state.depenses['Type']=='Débit'], names='Catégorie', values='Montant', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_pie.update_layout(height=300, margin=dict(t=20, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("💡 Recommandations Personnalisées")
    rec_cols = st.columns(len(recommendations))
    for i, reco in enumerate(recommendations):
        with rec_cols[i]:
            st.markdown(f"""
            <div class="reco-card" style="border-top: 5px solid {reco['color']};">
                <div style="font-size: 2em;">{reco['icon']}</div>
                <h3>{reco['titre']}</h3>
                <p style="font-size: 0.9em; min-height: 80px;">{reco['msg']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.button(reco['action'], key=f"btn_rec_{i}", use_container_width=True)

    st.markdown("---")
    with st.expander("🔮 Simulateur Long Terme", expanded=False):
        s_c1, s_c2 = st.columns([1,2])
        with s_c1:
            m_save = st.slider("Épargne mensuelle", 50, 1000, 200)
            y_dur = st.slider("Durée (ans)", 5, 30, 15)
        with s_c2:
            capital = sum([m_save * ((1 + 0.05/12)**(i)) for i in range(y_dur*12)])
            st.metric(f"Capital projeté dans {y_dur} ans (5%)", f"{capital:,.0f} €")
            st.progress(min(capital/100000, 1.0))

    st.markdown("---")
    st.subheader("📉 Marchés Financiers")
    tab_cac, tab_sp, tab_nas = st.tabs(["CAC 40", "S&P 500", "Nasdaq"])
    def plot_market(df, color):
        fig = px.line(df, x="Date", y="Close")
        fig.update_traces(line_color=color)
        fig.update_layout(height=250, margin=dict(t=10, b=10, l=10, r=10))
        return fig
    with tab_cac: st.plotly_chart(plot_market(st.session_state.cac40, "#0055A4"), use_container_width=True)
    with tab_sp: st.plotly_chart(plot_market(st.session_state.sp500, "#B22234"), use_container_width=True)
    with tab_nas: st.plotly_chart(plot_market(st.session_state.nasdaq, "#FF6F00"), use_container_width=True)

st.markdown("""
<div class="footer">
    <div style="margin-bottom: 10px;">
        <a href="#">FAQ</a> • 
        <a href="#">Engagements RSE</a> • 
        <a href="#">Sécurité</a> • 
        <a href="#">Tarifs</a> • 
        <a href="#">Nous rejoindre</a>
    </div>
    <div style="margin-bottom: 10px;">
        <a href="#">Mentions légales</a> • 
        <a href="#">Données personnelles</a> • 
        <a href="#">Cookies</a> • 
        <a href="#">Garantie des dépôts</a>
    </div>
    <p>© 2024 BPCE France. Tous droits réservés. Il s'agit d'une interface fictive.</p>
</div>
""", unsafe_allow_html=True)
