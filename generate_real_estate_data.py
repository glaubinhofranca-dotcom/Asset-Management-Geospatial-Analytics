import pandas as pd
import numpy as np
import random

# Configurações
NUM_PROPERTIES = 2000
random.seed(42)
np.random.seed(42)

print(">>> Generating Boston Real Estate Market Data...")

# 1. Bairros e Características
neighborhoods = {
    'Beacon Hill': {'base_price': 1500000, 'rent_factor': 0.04},
    'Back Bay': {'base_price': 1800000, 'rent_factor': 0.038},
    'South End': {'base_price': 1200000, 'rent_factor': 0.045},
    'Fenway': {'base_price': 800000, 'rent_factor': 0.05},
    'Dorchester': {'base_price': 600000, 'rent_factor': 0.06},
    'Seaport': {'base_price': 1400000, 'rent_factor': 0.042},
    'Cambridge': {'base_price': 950000, 'rent_factor': 0.048}
}

data = []

for i in range(NUM_PROPERTIES):
    prop_id = f"PROP_{i:04d}"
    neighborhood = random.choice(list(neighborhoods.keys()))
    base = neighborhoods[neighborhood]['base_price']
    
    # Gerar tamanho (SqFt) e Quartos
    sqft = np.random.randint(600, 3500)
    bedrooms = np.random.randint(1, 6)
    
    # Preço de Mercado "Justo" (Fair Market Value)
    # Baseado no bairro + tamanho + ruído
    fair_value = (base * (sqft / 1500)) + (bedrooms * 50000) + np.random.randint(-50000, 50000)
    
    # Preço de Listagem (Listing Price)
    # Algumas casas estão "Discounted" (oportunidade), outras "Overpriced"
    discount_factor = np.random.normal(1.0, 0.15) # Média 1.0, desvio 15%
    listing_price = fair_value * discount_factor
    
    # Condição do Imóvel (Afeta custo de reforma)
    condition_score = np.random.randint(1, 11) # 1 (Ruim) a 10 (Novo)
    renovation_cost = 0
    if condition_score < 5:
        renovation_cost = np.random.randint(50000, 150000)
    elif condition_score < 8:
        renovation_cost = np.random.randint(10000, 40000)
    
    # Métricas de Investimento (Asset Allocation Logic)
    total_investment = listing_price + renovation_cost
    
    # Aluguel Anual Estimado
    annual_rent = fair_value * neighborhoods[neighborhood]['rent_factor']
    
    # Cap Rate (Retorno Operacional Líquido / Valor do Ativo)
    # Capitalization Rate é O KPI de Real Estate
    cap_rate = (annual_rent / total_investment) * 100
    
    # ROI Potencial (Se vender após reforma pelo Fair Value)
    # Se compramos com desconto, o ROI é alto
    potential_profit = fair_value - total_investment
    roi_percent = (potential_profit / total_investment) * 100
    
    # Decisão do Algoritmo (Flag de Oportunidade)
    # Compramos se Cap Rate > 5% OU ROI > 15%
    recommendation = "Pass"
    if cap_rate > 5.5 or roi_percent > 15:
        recommendation = "Buy"

    data.append([prop_id, neighborhood, sqft, bedrooms, condition_score, 
                 round(listing_price, 2), round(fair_value, 2), 
                 round(renovation_cost, 2), round(total_investment, 2),
                 round(cap_rate, 2), round(roi_percent, 2), recommendation])

# Criar DataFrame
df = pd.DataFrame(data, columns=[
    'Property_ID', 'Neighborhood', 'Square_Feet', 'Bedrooms', 'Condition_Score',
    'Listing_Price', 'Fair_Market_Value', 'Renovation_Cost', 'Total_Investment',
    'Cap_Rate_Pct', 'ROI_Pct', 'Action_Recommendation'
])

# Salvar
df.to_csv('boston_real_estate_data.csv', index=False)
print("✅ Real Estate Dataset Generated Successfully!")
print(f"🏠 Buying Opportunities Found: {df[df['Action_Recommendation'] == 'Buy'].shape[0]}")