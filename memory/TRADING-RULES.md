# Trading Rules for Trading Bot from THE WALLSTREET FINANCIAL Channel

This document compiles and organizes trading rules from 4 video clips of THE WALLSTREET FINANCIAL channel to serve as a guideline for developing a Trading Bot, focusing on Price Action and Support & Resistance principles.

## 1. Support & Resistance Identification

### 1.1 Support & Resistance from "Twin Candles" [1], [2]
*   **Definition:** Two candlesticks with High or Low prices at the same or very close levels.
*   **Support:** Twin candles appearing below the price.
*   **Resistance:** Twin candles appearing above the price.
*   **Strength:** If there are multiple twin candles in close proximity, it is considered a very strong Support/Resistance zone.

### 1.2 Support & Resistance from "Closed Price" of a Larger Timeframe [3]
*   **Principle:** Use the Close, High, or Low price of a candlestick in a larger Timeframe (e.g., M30 or H1) as a reference point to find strong Support-Resistance for smaller Timeframes (M1, M5).
*   **Price Setting:** When a candlestick in a larger Timeframe closes, the price at that point is "set" as a significant Support or Resistance for the next candle.

### 1.3 "Unused Level" Support & Resistance [4]
*   **Rejection of SBR/RBS Theory:** Broken support does not become resistance, and broken resistance does not become support.
*   **Destroyed Level:** If a candlestick (body or wick) passes through or "overlaps" a drawn Support/Resistance line, that level is immediately considered invalid and should be removed from the chart.
*   **Finding Entry Points:** Look for the next Support or Resistance level that the price has not yet reached (Unused Level). When the price reaches this level, there is a high probability of a bounce or reversal.

## 2. Trend Analysis

### 2.1 Defining the Market "Scope" [1]
*   **Principle:** Focus on the current market scope (Current Universe) by limiting the view to the last 50-100 candles or as appropriate for the Timeframe.
*   **Trend Identification:**
    *   **Uptrend:** Price makes Higher Highs/Higher Lows within the current Scope.
    *   **Downtrend:** Price makes Lower Lows/Lower Highs within the current Scope.
*   **Rule:** Trade with the trend in the current Scope, even if the larger trend differs.

### 2.2 Timeframe Hierarchy [2]
*   **Monthly (M1):** Determines the long-term overall direction.
*   **Weekly (W1):** Determines the medium-term direction.
*   **Daily (D1) & 4-Hour (H4):** Used to determine the current trading direction (Current Market Master).
*   **Important Rule:** The program should prioritize the current Timeframe (e.g., Daily or H4) for finding short-to-medium term entry opportunities.

### 2.3 Relationship between Support & Resistance and Trend [2]
*   **In an Uptrend:** Support levels are more significant and stronger than resistance levels.
*   **In a Downtrend:** Resistance levels are more significant and stronger than support levels.

## 3. Entry Conditions

### 3.1 Trend Following Entry [1]
*   **Buy Side (in Uptrend):**
    1.  Identify the "twin candles" that form the nearest support to the current price.
    2.  Place a Buy Limit order or wait for the price to test that twin candle level.
    3.  If new twin candles form at a higher level (Higher Support), adjust the entry point accordingly.
*   **Sell Side (in Downtrend):**
    1.  Identify the "twin candles" that form the nearest resistance to the current price.
    2.  Place a Sell Limit order or wait for the price to test that twin candle level.
    3.  If new twin candles form at a lower level (Lower Resistance), adjust the selling point accordingly.

### 3.2 Price Confirmation [2]
*   **Do not enter immediately on a breakout:** The chart often shows overlaps or false breakouts.
*   **Buy Condition:** When the price breaks above a significant resistance, wait for the next candlestick to close **"green"** above that level for confirmation.
*   **Sell Condition:** When the price breaks below a significant support, wait for the next candlestick to close **"red"** below that level for confirmation.
*   **Waiting for Pullback/Retest:** The program should look for entry opportunities when the price pulls back to test a significant support in an uptrend, or bounces up to test a significant resistance in a downtrend, to get a more favorable price.

### 3.3 Scalping in Small Timeframes (M1, M5) [3]
*   **Higher TF (Reference TF):** Use M30 or H1 to find Support-Resistance.
*   **Lower TF (Entry TF):** Use M1 or M5 to find entry points.
*   **Entry Rules:**
    1.  The program must always wait for the candlestick in the **Higher TF to close first**.
    2.  When the Higher TF candlestick closes, record its Close, High, or Low price as a reference level.
    3.  In the next candlestick (currently forming), if the price in the **Lower TF** tests (Touches) the recorded reference level, consider opening an order:
        *   If it hits the upper resistance (High/Close of the previous candle) -> **Open a Sell order**.
        *   If it hits the lower support (Low/Close of the previous candle) -> **Open a Buy order**.
    4.  Do not open an order if the Higher TF candlestick has not yet finished its time (has not closed).

### 3.4 "Effect" Phenomenon for Scalping [4]
*   When the price breaks through a strong resistance (or support) for the first time, that level is destroyed, but some "energy" remains.
*   **Technique:** The candlestick immediately after the price has just broken a significant level often has a high chance of being the opposite color (e.g., breaking resistance with a green candle, the next candle has a high chance of being red), which can be used for short-term scalping.

## 4. Order Management

### 4.1 Setting Stop Loss and Take Profit (Exit Strategy) [1], [2], [3]
*   **Risk-Reward Ratio (RR):** Use a fixed ratio, such as 1:1, 1:2, or 1:3, as appropriate, or according to the nature of scalping.
*   **Stop Loss (SL):**
    *   Place slightly below the twin candle support (for Buy) or above the twin candle resistance (for Sell) [1].
    *   Place behind a "significant support" (for Buy) or "significant resistance" (for Sell) to allow those levels to protect against risk [2].
*   **Take Profit (TP):** Set according to the defined RR distance or at the next resistance/support found within the Scope [1].

## 5. Cautions and Recommendations for the Program (Developer Notes)

*   **"Twin Candles" Logic:** Programmatically, twin candles can be defined as two candlesticks with very similar Close or High/Low prices (with a small deviation or Pips difference) or candlesticks that show a reversal at the same point [1].
*   **Universe/Scope:** The program should calculate based on a specified number of candlesticks (Lookback Period) to find the current trend. It should not use too much historical data [1].
*   **PCf Concept:** Emphasize "Current" to predict "future" [1].
*   **Spread:** Trading M1/M5 is highly sensitive. The program must also account for the broker's spread. If the spread is too high, it may not be worthwhile to enter a trade [3].
*   **Slippage:** During news events or volatile markets, the price may overshoot reference levels. A volatility filter function should be included [3].
*   **Integration with FVG (Fair Value Gap):** FVG becomes more effective when it is "behind" a significant, unbroken support or resistance level [4].
*   **Timeframe for Observation Practice:** H4 is recommended to reduce noise [4].
*   **Backtesting:** Self-backtesting should be performed to observe price behavior [4].

## References

[1] เทรด Forex ดูจบเทรดเป็นภายใน 15 นาที: [https://youtu.be/S4lrKv_zKAI](https://youtu.be/S4lrKv_zKAI)
[2] เทคนิคลับ เทรดทอง+เนื้อหาหลักแสน: [https://youtu.be/upqtwQ2rUEE](https://youtu.be/upqtwQ2rUEE)
[3] เทรดสั้นความลับ M1 M5: [https://youtu.be/jmcdTo7Phkc](https://youtu.be/jmcdTo7Phkc)
[4] แนวรับแนวต้าน ที่แท้จริง: [https://youtu.be/aM-UG5W4Y1E](https://youtu.be/aM-UG5W4Y1E)
