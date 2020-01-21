
# modelop.score
def action(x):
	if x['DAClaimRequestPayload']['EventName'] == "RentersThirdPartyLiability":
		print("RentersThirdPartyLiability")
		yield(x, 1)
	elif x['DAClaimRequestPayload']['EventName'] == "HomeownersContentsOnly":
		print("RentersThirdPartyLiability")
		yield(x, 3)
	else:
		print ("Danger Mr. Robertson: EventName not found")
		yield("error")