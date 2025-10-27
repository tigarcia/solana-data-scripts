source venv/bin/activate
EPOCH=$(solana -um epoch-info | grep Epoch: | awk '{print $2}')
LAST_EPOCH=$((EPOCH-1))
echo $LAST_EPOCH
echo "Epoch: $EPOCH"
python main.py -vo
python main.py -so
echo "Saving Validator App Data"
python main.py -sva
echo "Getting solana -um validators"
solana -um validators --keep-unstaked-delinquents --output json-compact > mb-validators-epoch-${EPOCH}.json
echo "Getting solana -um gossip"
solana -um gossip --output json-compact > mb-gossip-epoch-${EPOCH}.json
echo "Getting solana -um leader-schedule"
solana -um leader-schedule --epoch $EPOCH --output json-compact > mb-leader-schedule-epoch-${EPOCH}.json
echo "Getting solana -um block-production epoch $LAST_EPOCH"
solana -um block-production --epoch $LAST_EPOCH --output json-compact > mb-block-production-epoch-${LAST_EPOCH}.json
DATE_AND_TIME=$(date -u +"%Y-%m-%dT%H-%M")
echo "Getting stakewiz output for epoch $EPOCH"
curl -H "Accept: application/json" https://api.stakewiz.com/validators > stake-wiz-epoch-${EPOCH}-${DATE_AND_TIME}.json
