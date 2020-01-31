# fastscore.slot.0: in-use
# fastscore.slot.1: in-use

import requests

TPL_engine = 'engine-2'
HOCO_engine = 'engine-3'
urlendpoint = "/2/active/model/roundtrip/0/1"

def action(x):
	try:
		yield(handleInput(x))
	except Exception as e:
		print(e, flush=True)
		yield("an error occurred")

def handleInput(x):
	claimNumber = x['DAClaimRequestPayload']['Claim']['ClaimNumber']
	eventName = x['DAClaimRequestPayload']['EventName']
	lossDesc = x['DAClaimRequestPayload']['Claim']['Description']
	payload = dict(ClaimNumber=claimNumber, EventName=eventName, LossDescription=lossDesc)

	if eventName == "RentersThirdPartyLiability":
		#print("RentersThirdPartyLiability", flush=True)
		response = callEngine(TPL_engine, payload)
		return(response)

	elif eventName == "HomeownersContentsOnly":
		#print("HOCO", flush=True)
		response = callEngine(HOCO_engine, payload)
		return(response)
	else:
		print("Danger Mr. Robertson: EventName: " + eventName + " not found", flush=True)
		return("error")

def callEngine(engine_name, payload):
	url = "http://" + engine_name + ":8003" + urlendpoint + "?timeout=2000"
	#print("URL: " + url, flush=True)
	response = requests.post(url, json=payload)
	#print(response, flush=True)
	#print(response.content, flush=True)
	if response.status_code == 200:
		return(response.content.decode('ascii'))
	else:
		return("WHAT WHAT")
