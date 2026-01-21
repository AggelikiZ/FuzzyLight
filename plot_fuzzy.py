import numpy as np
import matplotlib.pyplot as plt

# Ρυθμίσεις για καθαρό, επαγγελματικό στυλ με χρώματα
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.7,
    "axes.linewidth": 1.2,
    "xtick.direction": "in",
    "ytick.direction": "in"
})

class FuzzyLogic:
    def trapmf(self, x, a, b, c, d):
        if x <= a or x >= d: return 0.0
        if b <= x <= c: return 1.0
        if a < x < b: return (x - a) / (b - a + 1e-9)
        return (d - x) / (d - c + 1e-9)
    
    def demand_membership(self, x, penalty=1.0):
        # Εφαρμογή του penalty στην είσοδο x
        low  = self.trapmf(x * penalty, 0, 0, 1, 3)
        med  = self.trapmf(x * penalty, 2, 4, 8, 12)
        high = self.trapmf(x * penalty, 10, 18, 100, 100)
        return low, med, high
    
    def starvation_membership(self, x):
        low  = self.trapmf(x, 0, 0, 30, 50) 
        high = self.trapmf(x, 40, 60, 500, 500) 
        return low, high

fl = FuzzyLogic()

# --- PLOT 1: DEMAND MEMBERSHIP FUNCTIONS ---
plt.figure(figsize=(10, 6))
x_demand = np.linspace(0, 35, 1000)
# Παίρνουμε τις τιμές για penalty = 1.0 (Normal)
y_demand = np.array([fl.demand_membership(x, 1.0) for x in x_demand])

plt.plot(x_demand, y_demand[:, 0], color='#1f77b4', lw=2.5, label='Low Demand')
plt.plot(x_demand, y_demand[:, 1], color='#2ca02c', lw=2.5, label='Medium Demand')
plt.plot(x_demand, y_demand[:, 2], color='#d62728', lw=2.5, label='High Demand')

plt.fill_between(x_demand, y_demand[:, 0], color='#1f77b4', alpha=0.1)
plt.fill_between(x_demand, y_demand[:, 1], color='#2ca02c', alpha=0.1)
plt.fill_between(x_demand, y_demand[:, 2], color='#d62728', alpha=0.1)

plt.title('Demand Membership Functions', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Traffic Demand (x)', fontsize=13)
plt.ylabel('Membership Degree ($\mu$)', fontsize=13)
plt.xlim(0, 35)
plt.ylim(0, 1.05)
plt.legend(loc='upper right', frameon=True, shadow=True)
plt.tight_layout()
plt.show()

# --- PLOT 2: STARVATION MEMBERSHIP FUNCTIONS ---
plt.figure(figsize=(10, 6))
x_starv = np.linspace(0, 150, 1000)
y_starv = np.array([fl.starvation_membership(x) for x in x_starv])

plt.plot(x_starv, y_starv[:, 0], color='#9467bd', lw=2.5, label='Low Starvation')
plt.plot(x_starv, y_starv[:, 1], color='#ff7f0e', lw=2.5, label='High Starvation')

plt.fill_between(x_starv, y_starv[:, 0], color='#9467bd', alpha=0.1)
plt.fill_between(x_starv, y_starv[:, 1], color='#ff7f0e', alpha=0.1)

plt.title('Starvation Membership Functions', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Starvation Level (x)', fontsize=13)
plt.ylabel('Membership Degree ($\mu$)', fontsize=13)
plt.xlim(0, 150)
plt.ylim(0, 1.05)
plt.legend(loc='center right', frameon=True, shadow=True)
plt.tight_layout()
plt.show()