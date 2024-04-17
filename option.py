import numpy as np
from scipy.stats import norm

S = 100
K = 90
T = 1
r = 0.05
sigma = 0.2

#function for d1 and d2
def calculate_d1_d2(S, K, T, r, sigma):
    d1 = (np.log(S / K) + ( r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

#function for price call opcion
def black_scholes_call(S, K, T, r, sigma):
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

#function for price put opcion
def black_scholes_pyt(S, K, T, r, sigma):
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price


call_price = black_scholes_call(S, K, T, r, sigma)
put_price = black_scholes_pyt(S, K, T, r, sigma)

print(f"Price call opcion: {call_price:.2f}")
print(f"Price put opcion: {put_price:.2f}")

# function for Delta for call and put opcion
def delta(S, K, T, r, sigma):
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    call_delta = norm.cdf(d1)
    put_delta = call_delta - 1
    return call_delta, put_delta

# function for Gamma for call and put opcion 
def gamma(S, K, T, r, sigma):
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    gamma_value = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    return gamma_value

# function for  Vega for call and put opcion
def vega(S, K, T, r, sigma):
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    vega_value = S * norm.pdf(d1) * np.sqrt(T) * 0.01
    return vega_value

# function for Theta call and put opcion 
def theta(S, K, T, r, sigma):
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    term1 = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
    term2 = r * K * np.exp(-r * T) * norm.cdf(d2)
    call_theta = (term1 - term2) / 365
    put_theta = (term1 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    return call_theta, put_theta

# function for Rho for call and put opcion
def rho(S, K, T, r, sigma):
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    call_rho = K * T * np.exp(-r * T) * norm.cdf(d2) * 0.01
    put_rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) * 0.01
    return call_rho, put_rho

# call funcion grec
call_delta, put_delta = delta(S, K, T, r, sigma)
gamma_value = gamma(S, K, T, r, sigma)
vega_value = vega(S, K, T, r, sigma)
call_theta, put_theta = theta(S, K, T, r, sigma)
call_rho, put_rho = rho(S, K, T, r, sigma)

# result
print(f"Call Delta: {call_delta:.4f}, Put Delta: {put_delta:.4f}")
print(f"Gamma: {gamma_value:.4f}")
print(f"Vega (per 1% change in vol): {vega_value:.4f}")
print(f"Call Theta (per day): {call_theta:.4f}, Put Theta (per day): {put_theta:.4f}")
print(f"Call Rho (per 1% change in rate): {call_rho:.4f}, Put Rho (per 1% change in rate): {put_rho:.4f}")
