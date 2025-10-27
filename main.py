import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
import json
import os
import sys
import argparse
import requests
from datetime import date
from dotenv import load_dotenv


load_dotenv()

VOTE_ACCOUNT = Pubkey.from_string("Vote111111111111111111111111111111111111111")
STAKE_ACCOUNT = Pubkey.from_string("Stake11111111111111111111111111111111111111")
RPC_URL = os.getenv("RPC_URL")
VALIDATORS_APP_API_KEY = os.getenv("VALIDATORS_APP_API_KEY")


def get_validators_app_data(network="mainnet"):
    url = f"https://www.validators.app/api/v1/validators/{network}.json?order=stake"
    r = requests.get(url, headers={"Token": VALIDATORS_APP_API_KEY})
    return r.json()


def save_validators_app_data(network="mainnet"):
    validators_app_data = get_validators_app_data(network)
    today = date.today().strftime("%d-%m-%y")
    filename = f"validators-app-data-{today}.json"
    with open(filename, "w") as f:
        json.dump(validators_app_data, f, indent=None)


async def get_epoch_info():
    async with AsyncClient(RPC_URL) as client:
        res = await client.get_epoch_info()

    return res.value


async def get_block_time(slot_number):
    async with AsyncClient(RPC_URL) as client:
        res = await client.get_block_time(slot_number)

    return res.value


async def get_vote_account():
    async with AsyncClient(RPC_URL, timeout=50000) as client:
        res = await client.is_connected()
        # Vote accounts are limited (~3-4K), so json_parsed should work
        res = await client.get_program_accounts_json_parsed(VOTE_ACCOUNT)
    return res.value


async def get_stake_account():
    async with AsyncClient(RPC_URL, timeout=50000) as client:
        res = await client.is_connected()
        # Filter for delegated stake accounts (200 bytes) to reduce scan size
        # This filters out other types and makes the request more manageable
        res = await client.get_program_accounts_json_parsed(STAKE_ACCOUNT)
    return res.value
    


def save_vote_data(vote_results, epoch_id):

    vote_results_filename = f"vote_account_epoch_{epoch_id}.json"
    # Convert solders objects to JSON-serializable format
    serializable_results = [json.loads(result.to_json()) for result in vote_results]
    with open(vote_results_filename, "w") as f:
        json.dump(serializable_results, f, indent=None)

    print(f"Wrote to file {vote_results_filename}")
   

def save_stake_data(stake_results, epoch_id):
    stake_results_filename = f"stake_account_epoch_{epoch_id}.json"
    # Convert solders objects to JSON-serializable format
    serializable_results = [json.loads(result.to_json()) for result in stake_results]
    with open(stake_results_filename, "w") as f:
        json.dump(serializable_results, f, indent=None)

    print(f"Wrote to file {stake_results_filename}")
   

async def main(options):

    if options.vote_only and options.stake_only:
        print("ERROR: cannot use --stake-only and --vote-only flags at the same time")
        sys.exit(1)

    if options.save_validator_app_data:
        save_validators_app_data()
        sys.exit(1)

    epoch_info = await get_epoch_info()

    epoch_id = epoch_info.epoch

    print(f"Saving json data to file for epoch {epoch_id}")

    if not options.stake_only:
        print('trying to get vote account')
        vote_results = await get_vote_account()
        print(f"Vote account results len: {len(vote_results)}")

        save_vote_data(vote_results, epoch_id)

    if not options.vote_only:
        print('trying to get stake account......')
        stake_results = await get_stake_account()
        print(f"Stake account results len: {len(stake_results)}")

        save_stake_data(stake_results, epoch_id)


def parseArguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-vo", "--vote-only",
        help="Only download and store the vote account data",
        action="store_true"
    )
    parser.add_argument(
        "-so", "--stake-only",
        help="Only download and store the stake account data",
        action="store_true"
    )
    parser.add_argument(
        "-sva", "--save-validator-app-data",
        help="Save the validator app data locally",
        action="store_true"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parseArguments()
    asyncio.run(main(args))

"""
Example of vote account and stake account result
{
    "account": {
        "data": {
            "parsed": {
                "info": {
                    "authorizedVoters": [
                        {
                            "authorizedVoter": "6poikjtKFzySv2zrfEJCQorTDJWmoqCLPbSXeNLHyvL3",
                            "epoch": 318
                        }
                    ],
                    "authorizedWithdrawer": "4Zk3cLQdPiJuyFXgfaPvUZ2tXL6TVSmwswJGws8wN5Xi",
                    "commission": 10,
                    "epochCredits": [
                        {
                            "credits": "35110439",
                            "epoch": 255,
                            "previousCredits": "34741063"
                        },
                        {
                            "credits": "35477104",
                            "epoch": 256,
                            "previousCredits": "35110439"
                        },
                        {
                            "credits": "35821422",
                            "epoch": 257,
                            "previousCredits": "35477104"
                        },
                        {
                            "credits": "36199690",
                            "epoch": 258,
                            "previousCredits": "35821422"
                        },
                        {
                            "credits": "36585878",
                            "epoch": 259,
                            "previousCredits": "36199690"
                        },
                        {
                            "credits": "36960341",
                            "epoch": 260,
                            "previousCredits": "36585878"
                        },
                        {
                            "credits": "37349945",
                            "epoch": 261,
                            "previousCredits": "36960341"
                        },
                        {
                            "credits": "37748114",
                            "epoch": 262,
                            "previousCredits": "37349945"
                        },
                        {
                            "credits": "38115207",
                            "epoch": 263,
                            "previousCredits": "37748114"
                        },
                        {
                            "credits": "38497674",
                            "epoch": 264,
                            "previousCredits": "38115207"
                        },
                        {
                            "credits": "38865780",
                            "epoch": 265,
                            "previousCredits": "38497674"
                        },
                        {
                            "credits": "39193656",
                            "epoch": 266,
                            "previousCredits": "38865780"
                        },
                        {
                            "credits": "39541007",
                            "epoch": 267,
                            "previousCredits": "39193656"
                        },
                        {
                            "credits": "39912315",
                            "epoch": 268,
                            "previousCredits": "39541007"
                        },
                        {
                            "credits": "40280845",
                            "epoch": 269,
                            "previousCredits": "39912315"
                        },
                        {
                            "credits": "40620138",
                            "epoch": 270,
                            "previousCredits": "40280845"
                        },
                        {
                            "credits": "40862310",
                            "epoch": 271,
                            "previousCredits": "40620138"
                        },
                        {
                            "credits": "41244054",
                            "epoch": 272,
                            "previousCredits": "40862310"
                        },
                        {
                            "credits": "41622056",
                            "epoch": 273,
                            "previousCredits": "41244054"
                        },
                        {
                            "credits": "42005283",
                            "epoch": 274,
                            "previousCredits": "41622056"
                        },
                        {
                            "credits": "42376073",
                            "epoch": 275,
                            "previousCredits": "42005283"
                        },
                        {
                            "credits": "42757669",
                            "epoch": 276,
                            "previousCredits": "42376073"
                        },
                        {
                            "credits": "43124323",
                            "epoch": 277,
                            "previousCredits": "42757669"
                        },
                        {
                            "credits": "43490733",
                            "epoch": 278,
                            "previousCredits": "43124323"
                        },
                        {
                            "credits": "43861402",
                            "epoch": 279,
                            "previousCredits": "43490733"
                        },
                        {
                            "credits": "44221565",
                            "epoch": 280,
                            "previousCredits": "43861402"
                        },
                        {
                            "credits": "44577768",
                            "epoch": 281,
                            "previousCredits": "44221565"
                        },
                        {
                            "credits": "44926212",
                            "epoch": 282,
                            "previousCredits": "44577768"
                        },
                        {
                            "credits": "45272665",
                            "epoch": 283,
                            "previousCredits": "44926212"
                        },
                        {
                            "credits": "45623174",
                            "epoch": 284,
                            "previousCredits": "45272665"
                        },
                        {
                            "credits": "45967423",
                            "epoch": 285,
                            "previousCredits": "45623174"
                        },
                        {
                            "credits": "46323144",
                            "epoch": 286,
                            "previousCredits": "45967423"
                        },
                        {
                            "credits": "46664568",
                            "epoch": 287,
                            "previousCredits": "46323144"
                        },
                        {
                            "credits": "47029907",
                            "epoch": 288,
                            "previousCredits": "46664568"
                        },
                        {
                            "credits": "47387219",
                            "epoch": 289,
                            "previousCredits": "47029907"
                        },
                        {
                            "credits": "47781040",
                            "epoch": 290,
                            "previousCredits": "47387219"
                        },
                        {
                            "credits": "48172328",
                            "epoch": 291,
                            "previousCredits": "47781040"
                        },
                        {
                            "credits": "48574286",
                            "epoch": 292,
                            "previousCredits": "48172328"
                        },
                        {
                            "credits": "48972336",
                            "epoch": 293,
                            "previousCredits": "48574286"
                        },
                        {
                            "credits": "49377963",
                            "epoch": 294,
                            "previousCredits": "48972336"
                        },
                        {
                            "credits": "49762507",
                            "epoch": 295,
                            "previousCredits": "49377963"
                        },
                        {
                            "credits": "50111475",
                            "epoch": 296,
                            "previousCredits": "49762507"
                        },
                        {
                            "credits": "50429598",
                            "epoch": 297,
                            "previousCredits": "50111475"
                        },
                        {
                            "credits": "50700636",
                            "epoch": 298,
                            "previousCredits": "50429598"
                        },
                        {
                            "credits": "51034027",
                            "epoch": 299,
                            "previousCredits": "50700636"
                        },
                        {
                            "credits": "51414344",
                            "epoch": 300,
                            "previousCredits": "51034027"
                        },
                        {
                            "credits": "51767999",
                            "epoch": 301,
                            "previousCredits": "51414344"
                        },
                        {
                            "credits": "52143038",
                            "epoch": 302,
                            "previousCredits": "51767999"
                        },
                        {
                            "credits": "52504612",
                            "epoch": 303,
                            "previousCredits": "52143038"
                        },
                        {
                            "credits": "52833419",
                            "epoch": 304,
                            "previousCredits": "52504612"
                        },
                        {
                            "credits": "53139852",
                            "epoch": 305,
                            "previousCredits": "52833419"
                        },
                        {
                            "credits": "53501254",
                            "epoch": 306,
                            "previousCredits": "53139852"
                        },
                        {
                            "credits": "53824203",
                            "epoch": 307,
                            "previousCredits": "53501254"
                        },
                        {
                            "credits": "54122701",
                            "epoch": 308,
                            "previousCredits": "53824203"
                        },
                        {
                            "credits": "54415510",
                            "epoch": 309,
                            "previousCredits": "54122701"
                        },
                        {
                            "credits": "54713420",
                            "epoch": 310,
                            "previousCredits": "54415510"
                        },
                        {
                            "credits": "55000017",
                            "epoch": 311,
                            "previousCredits": "54713420"
                        },
                        {
                            "credits": "55272105",
                            "epoch": 312,
                            "previousCredits": "55000017"
                        },
                        {
                            "credits": "55507598",
                            "epoch": 313,
                            "previousCredits": "55272105"
                        },
                        {
                            "credits": "55759987",
                            "epoch": 314,
                            "previousCredits": "55507598"
                        },
                        {
                            "credits": "56059477",
                            "epoch": 315,
                            "previousCredits": "55759987"
                        },
                        {
                            "credits": "56328514",
                            "epoch": 316,
                            "previousCredits": "56059477"
                        },
                        {
                            "credits": "56599971",
                            "epoch": 317,
                            "previousCredits": "56328514"
                        },
                        {
                            "credits": "56624188",
                            "epoch": 318,
                            "previousCredits": "56599971"
                        }
                    ],
                    "lastTimestamp": {
                        "slot": 137427657,
                        "timestamp": 1655142240
                    },
                    "nodePubkey": "6poikjtKFzySv2zrfEJCQorTDJWmoqCLPbSXeNLHyvL3",
                    "priorVoters": [],
                    "rootSlot": 137427602,
                    "votes": [
                        {
                            "confirmationCount": 31,
                            "slot": 137427603
                        },
                        {
                            "confirmationCount": 30,
                            "slot": 137427604
                        },
                        {
                            "confirmationCount": 29,
                            "slot": 137427605
                        },
                        {
                            "confirmationCount": 28,
                            "slot": 137427606
                        },
                        {
                            "confirmationCount": 27,
                            "slot": 137427607
                        },
                        {
                            "confirmationCount": 26,
                            "slot": 137427608
                        },
                        {
                            "confirmationCount": 25,
                            "slot": 137427609
                        },
                        {
                            "confirmationCount": 24,
                            "slot": 137427610
                        },
                        {
                            "confirmationCount": 23,
                            "slot": 137427611
                        },
                        {
                            "confirmationCount": 22,
                            "slot": 137427612
                        },
                        {
                            "confirmationCount": 21,
                            "slot": 137427613
                        },
                        {
                            "confirmationCount": 20,
                            "slot": 137427614
                        },
                        {
                            "confirmationCount": 19,
                            "slot": 137427615
                        },
                        {
                            "confirmationCount": 18,
                            "slot": 137427616
                        },
                        {
                            "confirmationCount": 17,
                            "slot": 137427618
                        },
                        {
                            "confirmationCount": 16,
                            "slot": 137427619
                        },
                        {
                            "confirmationCount": 15,
                            "slot": 137427620
                        },
                        {
                            "confirmationCount": 14,
                            "slot": 137427621
                        },
                        {
                            "confirmationCount": 13,
                            "slot": 137427622
                        },
                        {
                            "confirmationCount": 12,
                            "slot": 137427623
                        },
                        {
                            "confirmationCount": 11,
                            "slot": 137427625
                        },
                        {
                            "confirmationCount": 10,
                            "slot": 137427626
                        },
                        {
                            "confirmationCount": 9,
                            "slot": 137427627
                        },
                        {
                            "confirmationCount": 8,
                            "slot": 137427640
                        },
                        {
                            "confirmationCount": 7,
                            "slot": 137427641
                        },
                        {
                            "confirmationCount": 6,
                            "slot": 137427642
                        },
                        {
                            "confirmationCount": 5,
                            "slot": 137427652
                        },
                        {
                            "confirmationCount": 4,
                            "slot": 137427653
                        },
                        {
                            "confirmationCount": 3,
                            "slot": 137427654
                        },
                        {
                            "confirmationCount": 2,
                            "slot": 137427655
                        },
                        {
                            "confirmationCount": 1,
                            "slot": 137427657
                        }
                    ]
                },
                "type": "vote"
            },
            "program": "vote",
            "space": 3731
        },
        "executable": false,
        "lamports": 26371632207,
        "owner": "Vote111111111111111111111111111111111111111",
        "rentEpoch": 318
    },
    "pubkey": "B2vsqPPAiLMBZqhuqQdvx24ghg4AxMw76pp6V9kNTVms"
}
{
    "account": {
        "data": {
            "parsed": {
                "info": {
                    "meta": {
                        "authorized": {
                            "staker": "447YEohqKbW9S2WjeaJtcCHLx8RhsgWRktcpnr5Dsp5A",
                            "withdrawer": "EhYXq3ANp5nAerUpbSgd7VK2RRcxK1zNuSQ755G5Mtxx"
                        },
                        "lockup": {
                            "custodian": "3XdBZcURF5nKg3oTZAcfQZg8XEc5eKsx6vK8r3BdGGxg",
                            "epoch": 0,
                            "unixTimestamp": 1767744000
                        },
                        "rentExemptReserve": "2282880"
                    },
                    "stake": {
                        "creditsObserved": 21464248,
                        "delegation": {
                            "activationEpoch": "261",
                            "deactivationEpoch": "18446744073709551615",
                            "stake": "1023944272",
                            "voter": "8zCJw6dETsPGCCkre459fDoM4YjK6BCVqqfSyyhRXtaT",
                            "warmupCooldownRate": 0.25
                        }
                    }
                },
                "type": "delegated"
            },
            "program": "stake",
            "space": 200
        },
        "executable": false,
        "lamports": 1026227152,
        "owner": "Stake11111111111111111111111111111111111111",
        "rentEpoch": 317
    },
    "pubkey": "BY8yWGqFhjpUuzJytaqnBMrqFPZ6cH6muaA2PkpKcpJE"
}
"""
