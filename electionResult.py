import json

# 讀取投票結果資料
with open("voting_results.json", "r", encoding="utf-8") as file:
    voting_results = json.load(file)

# 以縣市為迭代單位，計算各政黨得票數
votes = {}
parties = {"dpp", "kmt", "tpp"}
for city in voting_results["district_total"]:
    party_votes = {party: voting_results[party][city] for party in parties}
    votes[city] = party_votes

percenatges = {}
# 計算各縣市各政黨的得票率
for city, total_votes in voting_results["district_total"].items():
    party_percentages = {
        party: (votes[city][party] / total_votes)*100 for party in parties}
    percenatges.update({city: party_percentages})

# 找到各縣市獲勝者、最大得票差距
max_vote_difference = 0
max_vote_difference_city = ""
winners_and_difference = {}
for city in percenatges:
    percenatges_list = list(percenatges[city].items())
    sorted_percentages = sorted(
        percenatges_list, key=lambda x: x[1], reverse=True)
    winner = sorted_percentages[0][0]
    vote_difference = sorted_percentages[0][1]-sorted_percentages[1][1]

    winners_and_difference[city] = {"winner": winner, " vote_difference": vote_difference}

    if vote_difference > max_vote_difference:
        max_vote_difference = vote_difference
        max_vote_difference_city = city
    print(f"{city}:獲勝者{winner} 得票率為{sorted_percentages[0][1]:.2f}%")
    
# print(
#     f"得票率差距最大的縣市為『{max_vote_difference_city}』, 差距為{max_vote_difference:.2f}%")

for city in winners_and_difference:
    print(f"{city} : 獲勝者:{winners_and_difference[city]["winner"]}, 與第二名得票差距：{winners_and_difference[city]["vote_difference"]}")
    
    winner = winners_and_difference[city]["winner"]
    ratio = winners_and_difference[city]["vote_difference"]/max_vote_difference
    
    if winner == "tpp":
        H, S, L = (177, 61, int(75 - 40 * ratio))
    elif winner == "kmt":
        H, S, L = (212, 100, int(85 - 40 * ratio))
    elif winner == "dpp":
        H, S, L = (130, 60, int(75 - 40 * ratio))
        
    HSL_str = f"HSL: hsl({H}%, {S}%, {L}%)"
    
    print(HSL_str)
    