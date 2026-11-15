"""Phase 2b: choose the best set of parcels for ONE trip with 0/1 knapsack dynamic programming.

dp[i][w] = best total value using only the first i parcels with capacity w.
    dp[i][w] = dp[i-1][w]                                   if weight_i > w
             = max(dp[i-1][w], dp[i-1][w-weight_i] + value_i) otherwise
Time O(n*W), space O(n*W) (full table kept so the chosen parcels can be traced back).
"""


def knapsack(parcels, capacity):
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = parcels[i - 1].weight, parcels[i - 1].value
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if wt <= w and dp[i - 1][w - wt] + val > dp[i][w]:
                dp[i][w] = dp[i - 1][w - wt] + val
    # Trace back which parcels were taken.
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(parcels[i - 1])
            w -= parcels[i - 1].weight
    chosen.reverse()
    return dp[n][capacity], chosen, dp
