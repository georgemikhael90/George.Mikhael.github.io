import pandas as pd
import numpy as np
from datetime import datetime, date
from enum import Enum

class ServiceCategory(Enum):
    ARMY_NG = "Army National Guard"
    AIR_NG = "Air National Guard"
    TEXAS_SG = "Texas State Guard"

# Texas State Guard fixed rates
TEXAS_SG_RATES = {
    'daily_base_rate': 173.67,
    'special_pay': 22.00,
    'daily_allowance': 68.00,
    'total_daily_rate': 263.67
}

PER_DIEM_RATE = 68.00  # $68/day Per Diem rate
MINIMUM_DAILY_RATE = 241.67  # Minimum daily rate for Army NG and Air NG

def calculate_minimum_income_adjustment(daily_base_rate, daily_bah_rate, daily_bas_rate):
    """Calculate the minimum income adjustment if needed"""
    # Calculate daily total (Base Pay + BAH + BAS + Per Diem)
    daily_total = daily_base_rate + daily_bah_rate + daily_bas_rate + PER_DIEM_RATE
    
    # If the total is less than the minimum daily rate, calculate the adjustment needed
    if daily_total < MINIMUM_DAILY_RATE:
        return MINIMUM_DAILY_RATE - daily_total
    
    # No adjustment needed if the total already meets or exceeds the minimum
    return 0.0

def get_base_pay_rate(grade, years_of_service):
    """Calculate daily base pay rate based on military grade and years of service"""
    # Daily base pay rates from 2024 military pay table
    pay_grades = {
        'O-6': {
            0: 297.70, 1: 297.70, 2: 325.40, 3: 345.67, 4: 345.67, 5: 345.67,
            6: 346.93, 7: 346.93, 8: 361.08, 9: 361.08, 10: 362.96, 11: 362.96,
            12: 362.96, 13: 362.96, 14: 382.64, 15: 382.64, 16: 417.43, 17: 417.43,
            18: 437.85, 19: 437.85, 20: 458.26, 21: 458.26, 22: 469.88, 23: 469.88,
            24: 481.64, 25: 481.64, 26: 504.43, 27: 504.43, 28: 504.43, 29: 504.43,
            30: 514.17, 31: 514.17, 32: 514.17, 33: 514.17, 34: 514.17, 35: 514.17,
            36: 514.17, 37: 514.17, 38: 514.17, 39: 514.17, 40: 514.17
        },
        'O-5': {
            0: 250.95, 1: 250.95, 2: 280.58, 3: 298.85, 4: 302.29, 5: 302.29,
            6: 313.70, 7: 313.70, 8: 320.50, 9: 320.50, 10: 335.50, 11: 335.50,
            12: 346.53, 13: 346.53, 14: 360.76, 15: 360.76, 16: 382.48, 17: 382.48,
            18: 392.84, 19: 392.84, 20: 403.08, 21: 403.08, 22: 414.70, 23: 414.70,
            24: 414.70, 25: 414.70, 26: 414.70, 27: 414.70, 28: 414.70, 29: 414.70,
            30: 414.70, 31: 414.70, 32: 414.70, 33: 414.70, 34: 414.70, 35: 414.70,
            36: 414.70, 37: 414.70, 38: 414.70, 39: 414.70, 40: 414.70
        },
        'O-4': {
            0: 218.81, 1: 218.81, 2: 250.66, 3: 266.30, 4: 269.75, 5: 269.75,
            6: 284.24, 7: 284.24, 8: 299.79, 9: 299.79, 10: 319.17, 11: 319.17,
            12: 334.21, 13: 334.21, 14: 344.69, 15: 344.69, 16: 350.70, 17: 350.70,
            18: 354.17, 19: 354.17, 20: 354.17, 21: 354.17, 22: 354.17, 23: 354.17,
            24: 354.17, 25: 354.17, 26: 354.17, 27: 354.17, 28: 354.17, 29: 354.17,
            30: 354.17, 31: 354.17, 32: 354.17, 33: 354.17, 34: 354.17, 35: 354.17,
            36: 354.17, 37: 354.17, 38: 354.17, 39: 354.17, 40: 354.17
        },
        'O-3': {
            0: 194.39, 1: 194.39, 2: 218.14, 3: 234.09, 4: 253.75, 5: 253.75,
            6: 265.13, 7: 265.13, 8: 277.60, 9: 277.60, 10: 285.64, 11: 285.64,
            12: 298.89, 13: 298.89, 14: 305.82, 15: 305.82, 16: 305.82, 17: 305.82,
            18: 305.82, 19: 305.82, 20: 305.82, 21: 305.82, 22: 305.82, 23: 305.82,
            24: 305.82, 25: 305.82, 26: 305.82, 27: 305.82, 28: 305.82, 29: 305.82,
            30: 305.82, 31: 305.82, 32: 305.82, 33: 305.82, 34: 305.82, 35: 305.82,
            36: 305.82, 37: 305.82, 38: 305.82, 39: 305.82, 40: 305.82
        },
        'O-2': {
            0: 170.23, 1: 170.23, 2: 191.56, 3: 218.10, 4: 224.91, 5: 224.91,
            6: 229.18, 7: 229.18, 8: 229.18, 9: 229.18, 10: 229.18, 11: 229.18,
            12: 229.18, 13: 229.18, 14: 229.18, 15: 229.18, 16: 229.18, 17: 229.18,
            18: 229.18, 19: 229.18, 20: 229.18, 21: 229.18, 22: 229.18, 23: 229.18,
            24: 229.18, 25: 229.18, 26: 229.18, 27: 229.18, 28: 229.18, 29: 229.18,
            30: 229.18, 31: 229.18, 32: 229.18, 33: 229.18, 34: 229.18, 35: 229.18,
            36: 229.18, 37: 229.18, 38: 229.18, 39: 229.18, 40: 229.18
        },
        'O-1': {
            0: 149.95, 1: 149.95, 2: 155.40, 3: 184.38, 4: 184.38, 5: 184.38,
            6: 184.38, 7: 184.38, 8: 184.38, 9: 184.38, 10: 184.38, 11: 184.38,
            12: 184.38, 13: 184.38, 14: 184.38, 15: 184.38, 16: 184.38, 17: 184.38,
            18: 184.38, 19: 184.38, 20: 184.38, 21: 184.38, 22: 184.38, 23: 184.38,
            24: 184.38, 25: 184.38, 26: 184.38, 27: 184.38, 28: 184.38, 29: 184.38,
            30: 184.38, 31: 184.38, 32: 184.38, 33: 184.38, 34: 184.38, 35: 184.38,
            36: 184.38, 37: 184.38, 38: 184.38, 39: 184.38, 40: 184.38
        },
        'O3E': {
            0: 0.00, 1: 0.00, 2: 0.00, 3: 0.00, 4: 253.75, 5: 253.75,
            6: 265.13, 7: 265.13, 8: 277.60, 9: 277.60, 10: 285.64, 11: 285.64,
            12: 298.89, 13: 298.89, 14: 310.09, 15: 310.09, 16: 316.51, 17: 316.51,
            18: 325.26, 19: 325.26, 20: 325.26, 21: 325.26, 22: 325.26, 23: 325.26,
            24: 325.26, 25: 325.26, 26: 325.26, 27: 325.26, 28: 325.26, 29: 325.26,
            30: 325.26, 31: 325.26, 32: 325.26, 33: 325.26, 34: 325.26, 35: 325.26,
            36: 325.26, 37: 325.26, 38: 325.26, 39: 325.26, 40: 325.26
        },
        'O2E': {
            0: 0.00, 1: 0.00, 2: 0.00, 3: 0.00, 4: 224.91, 5: 224.91,
            6: 229.18, 7: 229.18, 8: 235.94, 9: 235.94, 10: 247.36, 11: 247.36,
            12: 256.20, 13: 256.20, 14: 262.77, 15: 262.77, 16: 262.77, 17: 262.77,
            18: 262.77, 19: 262.77, 20: 262.77, 21: 262.77, 22: 262.77, 23: 262.77,
            24: 262.77, 25: 262.77, 26: 262.77, 27: 262.77, 28: 262.77, 29: 262.77,
            30: 262.77, 31: 262.77, 32: 262.77, 33: 262.77, 34: 262.77, 35: 262.77,
            36: 262.77, 37: 262.77, 38: 262.77, 39: 262.77, 40: 262.77
        },
        'O1E': {
            0: 0.00, 1: 0.00, 2: 0.00, 3: 0.00, 4: 184.38, 5: 184.38,
            6: 195.75, 7: 195.75, 8: 202.38, 9: 202.38, 10: 209.15, 11: 209.15,
            12: 215.79, 13: 215.79, 14: 224.91, 15: 224.91, 16: 224.91, 17: 224.91,
            18: 224.91, 19: 224.91, 20: 224.91, 21: 224.91, 22: 224.91, 23: 224.91,
            24: 224.91, 25: 224.91, 26: 224.91, 27: 224.91, 28: 224.91, 29: 224.91,
            30: 224.91, 31: 224.91, 32: 224.91, 33: 224.91, 34: 224.91, 35: 224.91,
            36: 224.91, 37: 224.91, 38: 224.91, 39: 224.91, 40: 224.91
        },
        'W-5': {
            0: 0.00, 1: 0.00, 2: 0.00, 3: 0.00, 4: 0.00, 5: 0.00,
            6: 0.00, 7: 0.00, 8: 0.00, 9: 0.00, 10: 0.00, 11: 0.00,
            12: 0.00, 13: 0.00, 14: 0.00, 15: 0.00, 16: 0.00, 17: 0.00,
            18: 0.00, 19: 0.00, 20: 343.25, 21: 343.25, 22: 359.82, 23: 359.82,
            24: 372.17, 25: 372.17, 26: 385.81, 27: 385.81, 28: 385.81, 29: 385.81,
            30: 404.30, 31: 404.30, 32: 404.30, 33: 404.30, 34: 423.65, 35: 423.65,
            36: 423.65, 37: 423.65, 38: 444.04, 39: 444.04, 40: 444.04
        },
        'W-4': {
            0: 200.35, 1: 200.35, 2: 214.23, 3: 219.90, 4: 225.48, 5: 225.48,
            6: 235.10, 7: 235.10, 8: 244.61, 9: 244.61, 10: 254.24, 11: 254.24,
            12: 268.70, 13: 268.70, 14: 281.40, 15: 281.40, 16: 293.48, 17: 293.48,
            18: 303.39, 19: 303.39, 20: 313.04, 21: 313.04, 22: 327.19, 23: 327.19,
            24: 338.83, 25: 338.83, 26: 352.10, 27: 352.10, 28: 352.10, 29: 352.10,
            30: 358.79, 31: 358.79, 32: 358.79, 33: 358.79, 34: 358.79, 35: 358.79,
            36: 358.79, 37: 358.79, 38: 358.79, 39: 358.79, 40: 358.79
        },
        'W-3': {
            0: 184.41, 1: 184.41, 2: 191.38, 3: 198.57, 4: 200.90, 5: 200.90,
            6: 208.41, 7: 208.41, 8: 223.19, 9: 223.19, 10: 238.59, 11: 238.59,
            12: 245.84, 13: 245.84, 14: 254.23, 15: 254.23, 16: 262.85, 17: 262.85,
            18: 278.40, 19: 278.40, 20: 288.88, 21: 288.88, 22: 295.15, 23: 295.15,
            24: 301.82, 25: 301.82, 26: 310.91, 27: 310.91, 28: 310.91, 29: 310.91,
            30: 310.91, 31: 310.91, 32: 310.91, 33: 310.91, 34: 310.91, 35: 310.91,
            36: 310.91, 37: 310.91, 38: 310.91, 39: 310.91, 40: 310.91
        },
        'W-2': {
            0: 165.09, 1: 165.09, 2: 179.13, 3: 183.44, 4: 186.42, 5: 186.42,
            6: 196.03, 7: 196.03, 8: 210.99, 9: 210.99, 10: 218.42, 11: 218.42,
            12: 225.71, 13: 225.71, 14: 234.64, 15: 234.64, 16: 241.62, 17: 241.62,
            18: 247.93, 19: 247.93, 20: 255.49, 21: 255.49, 22: 260.46, 23: 260.46,
            24: 264.40, 25: 264.40, 26: 264.40, 27: 264.40, 28: 264.40, 29: 264.40,
            30: 264.40, 31: 264.40, 32: 264.40, 33: 264.40, 34: 264.40, 35: 264.40,
            36: 264.40, 37: 264.40, 38: 264.40, 39: 264.40, 40: 264.40
        },
        'W-1': {
            0: 146.94, 1: 146.94, 2: 160.98, 3: 164.74, 4: 172.71, 5: 172.71,
            6: 182.12, 7: 182.12, 8: 196.00, 9: 196.00, 10: 202.48, 11: 202.48,
            12: 211.57, 13: 211.57, 14: 220.48, 15: 220.48, 16: 227.49, 17: 227.49,
            18: 233.95, 19: 233.95, 20: 241.79, 21: 241.79, 22: 241.79, 23: 241.79,
            24: 241.79, 25: 241.79, 26: 241.79, 27: 241.79, 28: 241.79, 29: 241.79,
            30: 241.79, 31: 241.79, 32: 241.79, 33: 241.79, 34: 241.79, 35: 241.79,
            36: 241.79, 37: 241.79, 38: 241.79, 39: 241.79, 40: 241.79
        },
        'E-9': {
            0: 0.00, 1: 0.00, 2: 0.00, 3: 0.00, 4: 0.00, 5: 0.00,
            6: 0.00, 7: 0.00, 8: 0.00, 9: 0.00, 10: 238.58, 11: 238.58,
            12: 243.60, 13: 243.60, 14: 249.93, 15: 249.93, 16: 257.39, 17: 257.39,
            18: 264.93, 19: 264.93, 20: 276.95, 21: 276.95, 22: 287.16, 23: 287.16,
            24: 297.87, 25: 297.87, 26: 314.29, 27: 314.29, 28: 314.29, 29: 314.29,
            30: 329.14, 31: 329.14, 32: 329.14, 33: 329.14, 34: 344.78, 35: 344.78,
            36: 344.78, 37: 344.78, 38: 361.22, 39: 361.22, 40: 361.22
        },
        'E-8': {
            0: 0.00, 1: 0.00, 2: 0.00, 3: 0.00, 4: 0.00, 5: 0.00,
            6: 0.00, 7: 0.00, 8: 198.32, 9: 198.32, 10: 206.36, 11: 206.36,
            12: 211.33, 13: 211.33, 14: 217.29, 15: 217.29, 16: 223.74, 17: 223.74,
            18: 235.40, 19: 235.40, 20: 241.31, 21: 241.31, 22: 251.36, 23: 251.36,
            24: 256.93, 25: 256.93, 26: 270.65, 27: 270.65, 28: 270.65, 29: 270.65,
            30: 275.74, 31: 275.74, 32: 275.74, 33: 275.74, 34: 275.74, 35: 275.74,
            36: 275.74, 37: 275.74, 38: 275.74, 39: 275.74, 40: 275.74
        },
        'E-7': {
            0: 142.94, 1: 142.94, 2: 154.48, 3: 154.48, 4: 166.74, 5: 166.74,
            6: 172.22, 7: 172.22, 8: 181.59, 9: 181.59, 10: 186.88, 11: 186.88,
            12: 196.24, 13: 196.24, 14: 204.05, 15: 204.05, 16: 209.38, 17: 209.38,
            18: 215.04, 19: 215.04, 20: 217.24, 21: 217.24, 22: 224.61, 23: 224.61,
            24: 228.56, 25: 228.56, 26: 243.63, 27: 243.63, 28: 243.63, 29: 243.63,
            30: 243.63, 31: 243.63, 32: 243.63, 33: 243.63, 34: 243.63, 35: 243.63,
            36: 243.63, 37: 243.63, 38: 243.63, 39: 243.63, 40: 243.63
        },
        'E-6': {
            0: 125.89, 1: 125.89, 2: 136.87, 3: 136.87, 4: 147.33, 5: 147.33,
            6: 152.69, 7: 152.69, 8: 164.80, 9: 164.80, 10: 169.51, 11: 169.51,
            12: 178.63, 13: 178.63, 14: 181.42, 15: 181.42, 16: 183.45, 17: 183.45,
            18: 185.83, 19: 185.83, 20: 185.83, 21: 185.83, 22: 185.83, 23: 185.83,
            24: 185.83, 25: 185.83, 26: 185.83, 27: 185.83, 28: 185.83, 29: 185.83,
            30: 185.83, 31: 185.83, 32: 185.83, 33: 185.83, 34: 185.83, 35: 185.83,
            36: 185.83, 37: 185.83, 38: 185.83, 39: 185.83, 40: 185.83
        },
        'E-5': {
            0: 116.72, 1: 116.72, 2: 123.46, 3: 123.46, 4: 133.91, 5: 133.91,
            6: 142.13, 7: 142.13, 8: 150.73, 9: 150.73, 10: 157.82, 11: 157.82,
            12: 158.66, 13: 158.66, 14: 158.66, 15: 158.66, 16: 158.66, 17: 158.66,
            18: 158.66, 19: 158.66, 20: 158.66, 21: 158.66, 22: 158.66, 23: 158.66,
            24: 158.66, 25: 158.66, 26: 158.66, 27: 158.66, 28: 158.66, 29: 158.66,
            30: 158.66, 31: 158.66, 32: 158.66, 33: 158.66, 34: 158.66, 35: 158.66,
            36: 158.66, 37: 158.66, 38: 158.66, 39: 158.66, 40: 158.66
        },
        'E-4': {
            0: 108.41, 1: 108.41, 2: 113.10, 3: 113.10, 4: 123.48, 5: 123.48,
            6: 128.05, 7: 128.05, 8: 128.05, 9: 128.05, 10: 128.05, 11: 128.05,
            12: 128.05, 13: 128.05, 14: 128.05, 15: 128.05, 16: 128.05, 17: 128.05,
            18: 128.05, 19: 128.05, 20: 128.05, 21: 128.05, 22: 128.05, 23: 128.05,
            24: 128.05, 25: 128.05, 26: 128.05, 27: 128.05, 28: 128.05, 29: 128.05,
            30: 128.05, 31: 128.05, 32: 128.05, 33: 128.05, 34: 128.05, 35: 128.05,
            36: 128.05, 37: 128.05, 38: 128.05, 39: 128.05, 40: 128.05
        },
        'E-3': {
            0: 99.49, 1: 99.49, 2: 104.69, 3: 104.69, 4: 110.03, 5: 110.03,
            6: 110.03, 7: 110.03, 8: 110.03, 9: 110.03, 10: 110.03, 11: 110.03,
            12: 110.03, 13: 110.03, 14: 110.03, 15: 110.03, 16: 110.03, 17: 110.03,
            18: 110.03, 19: 110.03, 20: 110.03, 21: 110.03, 22: 110.03, 23: 110.03,
            24: 110.03, 25: 110.03, 26: 110.03, 27: 110.03, 28: 110.03, 29: 110.03,
            30: 110.03, 31: 110.03, 32: 110.03, 33: 110.03, 34: 110.03, 35: 110.03,
            36: 110.03, 37: 110.03, 38: 110.03, 39: 110.03, 40: 110.03
        },
        'E-2': {
            0: 95.43, 1: 95.43, 2: 95.43, 3: 95.43, 4: 95.43, 5: 95.43,
            6: 95.43, 7: 95.43, 8: 95.43, 9: 95.43, 10: 95.43, 11: 95.43,
            12: 95.43, 13: 95.43, 14: 95.43, 15: 95.43, 16: 95.43, 17: 95.43,
            18: 95.43, 19: 95.43, 20: 95.43, 21: 95.43, 22: 95.43, 23: 95.43,
            24: 95.43, 25: 95.43, 26: 95.43, 27: 95.43, 28: 95.43, 29: 95.43,
            30: 95.43, 31: 95.43, 32: 95.43, 33: 95.43, 34: 95.43, 35: 95.43,
            36: 95.43, 37: 95.43, 38: 95.43, 39: 95.43, 40: 95.43
        },
        'E-1': {
            0: 86.94, 1: 86.94, 2: 86.94, 3: 86.94, 4: 86.94, 5: 86.94,
            6: 86.94, 7: 86.94, 8: 86.94, 9: 86.94, 10: 86.94, 11: 86.94,
            12: 86.94, 13: 86.94, 14: 86.94, 15: 86.94, 16: 86.94, 17: 86.94,
            18: 86.94, 19: 86.94, 20: 86.94, 21: 86.94, 22: 86.94, 23: 86.94,
            24: 86.94, 25: 86.94, 26: 86.94, 27: 86.94, 28: 86.94, 29: 86.94,
            30: 86.94, 31: 86.94, 32: 86.94, 33: 86.94, 34: 86.94, 35: 86.94,
            36: 86.94, 37: 86.94, 38: 86.94, 39: 86.94, 40: 86.94
        }
    }

    # Find the appropriate pay based on years of service
    grade_pay = pay_grades.get(grade, pay_grades['E-1'])

    # Find the closest year bracket that's less than or equal to the given years of service
    valid_years = sorted([y for y in grade_pay.keys() if y <= years_of_service])
    if not valid_years:
        year_bracket = min(grade_pay.keys())
    else:
        year_bracket = max(valid_years)

    return grade_pay[year_bracket]

def get_bah_rate(grade, has_dependents):
    """Get daily BAH rate based on grade and dependent status"""
    # BAH rates from the provided table
    bah_rates = {
        'O-6': {'without': 72.35, 'with': 87.39},
        'O-5': {'without': 69.67, 'with': 84.24},
        'O-4': {'without': 64.55, 'with': 74.24},
        'O-3': {'without': 51.77, 'with': 61.43},
        'O-2': {'without': 41.01, 'with': 52.41},
        'O-1': {'without': 35.21, 'with': 46.92},
        'O3E': {'without': 55.87, 'with': 66.02},
        'O2E': {'without': 47.51, 'with': 59.58},
        'O1E': {'without': 41.32, 'with': 55.07},
        'W-5': {'without': 65.62, 'with': 71.70},
        'W-4': {'without': 58.26, 'with': 65.73},
        'W-3': {'without': 48.98, 'with': 60.25},
        'W-2': {'without': 43.47, 'with': 55.36},
        'W-1': {'without': 36.45, 'with': 47.92},
        'E-9': {'without': 47.82, 'with': 63.07},
        'E-8': {'without': 43.96, 'with': 58.17},
        'E-7': {'without': 40.49, 'with': 53.97},
        'E-6': {'without': 37.42, 'with': 49.88},
        'E-5': {'without': 33.68, 'with': 44.90},
        'E-4': {'without': 33.68, 'with': 44.90},
        'E-3': {'without': 33.68, 'with': 44.90},
        'E-2': {'without': 33.68, 'with': 44.90},
        'E-1': {'without': 33.68, 'with': 44.90},
    }

    rates = bah_rates.get(grade, bah_rates['E-1'])
    return rates['with'] if has_dependents else rates['without']

def get_bas_rate(grade):
    """Get daily BAS rate based on whether the member is an officer or enlisted"""
    if grade.startswith(('O-', 'O1E', 'O2E', 'O3E')):
        return 10.69  # Officer BAS rate
    return 15.53  # Enlisted BAS rate (including warrant officers)

def get_hazardous_duty_pay(has_completed_365_days, present_this_month):
    """Calculate Hazardous Duty Allowance"""
    if has_completed_365_days and present_this_month:
        return 1000  # $1000 lump sum for the month if present any day
    return 0

def get_hardship_duty_pay(present_this_month):
    """Calculate Hardship Duty Pay"""
    if present_this_month:
        return 500  # $500 lump sum for the month if present any day
    return 0

def get_imminent_danger_pay(present_this_month, at_border):
    """Calculate Imminent Danger Pay"""
    if present_this_month and at_border:
        return 225  # $225 lump sum for the month if present any day and at border
    return 0

def calculate_daily_allowances(grade, has_dependents):
    """Calculate and adjust daily BAH and BAS rates"""
    daily_bah_rate = get_bah_rate(grade, has_dependents)
    daily_bas_rate = get_bas_rate(grade)

    # Return the exact BAH and BAS rates without adjustment
    return round(daily_bah_rate, 2), round(daily_bas_rate, 2)

def calculate_texas_sg_pay(start_date, end_date):
    """Calculate pay for Texas State Guard with fixed rates"""
    current_date = start_date
    monthly_breakdown = {}

    while current_date <= end_date:
        month_key = current_date.strftime('%B %Y')

        # Calculate days in this month
        month_start = max(start_date, date(current_date.year, current_date.month, 1))
        if current_date.month == 12:
            next_month = date(current_date.year + 1, 1, 1)
        else:
            next_month = date(current_date.year, current_date.month + 1, 1)
        month_end = min(end_date, next_month - pd.Timedelta(days=1))
        days_in_month = (month_end - month_start).days + 1

        # Calculate fixed rate pay components
        base_pay = TEXAS_SG_RATES['daily_base_rate'] * days_in_month
        special_pay = TEXAS_SG_RATES['special_pay'] * days_in_month
        allowances = TEXAS_SG_RATES['daily_allowance'] * days_in_month
        monthly_total = TEXAS_SG_RATES['total_daily_rate'] * days_in_month

        monthly_breakdown[month_key] = {
            'days': days_in_month,
            'base_pay': round(base_pay, 2),
            'special_pay': round(special_pay, 2),
            'allowances': round(allowances, 2),
            'total': round(monthly_total, 2),
            # Set other pay types to 0 for consistent reporting
            'bah': 0,
            'bas': 0,
            'per_diem': 0,
            'minimum_income_adjustment': 0,
            'hazard_pay': 0,
            'hardship_pay': 0,
            'danger_pay': 0
        }

        # Move to next month
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)

    total_days = (end_date - start_date).days + 1
    grand_total = sum(month['total'] for month in monthly_breakdown.values())

    return {
        'daily_base_rate': TEXAS_SG_RATES['daily_base_rate'],
        'daily_special_rate': TEXAS_SG_RATES['special_pay'],
        'daily_allowance_rate': TEXAS_SG_RATES['daily_allowance'],
        'monthly_breakdown': monthly_breakdown,
        'total_days': total_days,
        'grand_total': round(grand_total, 2)
    }

def calculate_total_pay(service_category, grade, years_of_service, start_date, end_date, has_dependents=False, 
                       hazardous_duty=False, hardship_duty=False, at_border=False, present_this_month=False):
    """Calculate total pay based on service category"""

    if service_category == ServiceCategory.TEXAS_SG:
        return calculate_texas_sg_pay(start_date, end_date)

    # For Army NG and Air NG, use existing calculation logic
    daily_base_rate = get_base_pay_rate(grade, years_of_service)
    daily_bah_rate, daily_bas_rate = calculate_daily_allowances(grade, has_dependents)

    # Calculate minimum income adjustment if needed
    daily_adjustment = calculate_minimum_income_adjustment(daily_base_rate, daily_bah_rate, daily_bas_rate)

    # Initialize monthly breakdown
    monthly_breakdown = {}

    # Get month range
    current_date = start_date
    while current_date <= end_date:
        month_key = current_date.strftime('%B %Y')

        # Calculate days in this month
        month_start = max(start_date, date(current_date.year, current_date.month, 1))
        if current_date.month == 12:
            next_month = date(current_date.year + 1, 1, 1)
        else:
            next_month = date(current_date.year, current_date.month + 1, 1)
        month_end = min(end_date, next_month - pd.Timedelta(days=1))
        days_in_month = (month_end - month_start).days + 1

        # Calculate pay for this month
        base_pay = daily_base_rate * days_in_month
        bah = daily_bah_rate * days_in_month
        bas = daily_bas_rate * days_in_month
        per_diem = PER_DIEM_RATE * days_in_month

        # Calculate minimum income adjustment for the month
        adjustment = daily_adjustment * days_in_month

        # Monthly incentives (full amount if present any day in the month)
        hazard_pay = get_hazardous_duty_pay(hazardous_duty, present_this_month)
        hardship_pay = get_hardship_duty_pay(present_this_month if hardship_duty else False)
        danger_pay = get_imminent_danger_pay(present_this_month, at_border)

        monthly_total = base_pay + bah + bas + per_diem + adjustment + hazard_pay + hardship_pay + danger_pay

        # Store monthly breakdown
        monthly_breakdown[month_key] = {
            'days': days_in_month,
            'base_pay': round(base_pay, 2),
            'bah': round(bah, 2),
            'bas': round(bas, 2),
            'per_diem': round(per_diem, 2),
            'minimum_income_adjustment': round(adjustment, 2),
            'hazard_pay': round(hazard_pay, 2),
            'hardship_pay': round(hardship_pay, 2),
            'danger_pay': round(danger_pay, 2),
            'total': round(monthly_total, 2)
        }

        # Move to next month
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)

    # Calculate overall totals
    total_days = (end_date - start_date).days + 1
    grand_total = sum(month['total'] for month in monthly_breakdown.values())

    return {
        'daily_base_rate': daily_base_rate,
        'daily_bah_rate': daily_bah_rate,
        'daily_bas_rate': daily_bas_rate,
        'daily_per_diem_rate': PER_DIEM_RATE,
        'daily_adjustment_rate': daily_adjustment,
        'monthly_breakdown': monthly_breakdown,
        'total_days': total_days,
        'grand_total': round(grand_total, 2)
    }

def format_currency(amount):
    """Format number as currency"""
    return f"${amount:,.2f}"

def get_available_grades():
    """Return list of available military grades"""
    enlisted_grades = [f'E-{i}' for i in range(1, 10)]
    warrant_grades = [f'W-{i}' for i in range(1, 6)]
    officer_grades = ['O-1', 'O1E', 'O-2', 'O2E', 'O-3', 'O3E', 'O-4', 'O-5', 'O-6']
    return enlisted_grades + warrant_grades + officer_grades